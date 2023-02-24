
from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
import traceback
import json
import subprocess
from urllib import request
import fc2
import oss2
import os
import logging
import time

hostName = "0.0.0.0"
serverPort = 9000

# headers
fcRequestID = "x-fc-request-id"
fcAccessKeyID = "x-fc-access-key-id"
fcAccessKeySecret = "x-fc-access-key-secret"
fcSecurityToken = "x-fc-security-token"
fcRegion = "x-fc-region"
fcAccountID = "x-fc-account-id"


class CustomHandler(BaseHTTPRequestHandler):
    def gen_report_html(self, serviceName, functionName):
        access_key_id = self.headers.get(fcAccessKeyID)
        access_key_secret = self.headers.get(fcAccessKeySecret)
        security_token = self.headers.get(fcSecurityToken)
        region = self.headers.get(fcRegion)
        accountId = self.headers.get(fcAccountID)
        endpoint = "http://{}.{}-internal.fc.aliyuncs.com".format(
            accountId, region)
        client = fc2.Client(
            endpoint=endpoint,
            accessKeyID=access_key_id,
            accessKeySecret=access_key_secret,
            securityToken=security_token,
            Timeout=120,
        )
        start = time.time()
        r = client.get_function_code(serviceName, functionName)
        data = r.data
        url = data['url']
        li = url.split(".")
        li[0] = li[0].replace("https", "http")
        li[1] = li[1] + "-internal"
        code_url = ".".join(li)

        filename, _ = request.urlretrieve(
            code_url, "/tmp/{}_{}.zip".format(serviceName, functionName))
        print("code_zip filename = {}".format(filename))
        print("download function code_zip time = {} seconds" .format(
            time.time() - start))
        start = time.time()
        report_html = "/tmp/{}_{}.html".format(serviceName, functionName)
        try:
            subprocess.check_call(
                "dependency-check.sh -s {} -o {}".format(filename, report_html), shell=True)

            print(
                "dependency-check time = {} seconds".format(time.time() - start))
            start = time.time()

            auth = oss2.StsAuth(
                access_key_id, access_key_secret, security_token)
            bucket = oss2.Bucket(
                auth, "http://oss-{}-internal.aliyuncs.com".format(region), os.environ["BUCKET"])
            bucket.put_object_from_file(
                "dependency-check/{}/{}/{}.html".format(serviceName, functionName, time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())), report_html)

            print("upload report html time = {} seconds".format(
                time.time() - start))
            report_location = "https://oss.console.aliyun.com/bucket/oss-{}/{}/object?path=dependency-check/{}/{}/".format(
                region, os.environ["BUCKET"], serviceName, functionName)
            print(report_location)
            return report_location

        except Exception as e:
            raise e
        finally:
            if os.path.exists(filename):
                os.remove(filename)
            if os.path.exists(report_html):
                os.remove(report_html)

    def do_POST(self):
        rid = self.headers.get(fcRequestID)
        print("FC Invoke Start RequestId: " + rid)
        try:
            req_datas = self.rfile.read(
                int(self.headers["content-length"]))
            evt = json.loads(req_datas)
            serviceName = evt["serviceName"]
            functionName = evt["functionName"]
            report_url = self.gen_report_html(serviceName, functionName)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(report_url.encode())
            print("FC Invoke End RequestId: " + rid)
        except Exception as e:
            exc_info = sys.exc_info()
            trace = traceback.format_tb(exc_info[2])
            errRet = {
                "message": str(e),
                "stack": trace
            }
            print(errRet)
            print("FC Invoke End RequestId: " + rid +
                  ", Error: Unhandled function error")
            self.send_response(404)
            self.send_header("x-fc-status", "404")
            self.end_headers()
            self.wfile.write(json.dumps(errRet))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), CustomHandler)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

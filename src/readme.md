> 注：当前项目为 Serverless Devs 应用，由于应用中会存在需要初始化才可运行的变量（例如应用部署地区、服务名、函数名等等），所以**不推荐**直接 Clone 本仓库到本地进行部署或直接复制 s.yaml 使用，**强烈推荐**通过 `s init ` 的方法或应用中心进行初始化，详情可参考[部署 & 体验](#部署--体验) 。

# start-dependency-check-fc 帮助文档

<p align="center" class="flex justify-center">
    <a href="https://www.serverless-devs.com" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=start-dependency-check-fc&type=packageType">
  </a>
  <a href="http://www.devsapp.cn/details.html?name=start-dependency-check-fc" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=start-dependency-check-fc&type=packageVersion">
  </a>
  <a href="http://www.devsapp.cn/details.html?name=start-dependency-check-fc" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=start-dependency-check-fc&type=packageDownload">
  </a>
</p>

<description>

快速部署一个对函数代码包进行安全扫描的应用到阿里云函数计算

</description>

<codeUrl>

- [:smiley_cat: 代码](https://github.com/devsapp/start-dependency-check-fc/tree/main/src)

</codeUrl>
<preview>

</preview>

## 前期准备

使用该项目，您需要有开通以下服务：

<service>

| 服务                 | 备注                                                                                                  |
| -------------------- | ----------------------------------------------------------------------------------------------------- |
| 函数计算 FC          | 安全扫描的逻辑函数需要部署到函数计算                                                                  |
| 对象存储 OSS         | 安全扫描后的 html 报告保存到对象存储                                                                  |
| 事件总线 EventBridge | 监听函数代码包变化，自动触发安全扫描函数的运行，注意：EventBridge 开通以后， 需要在控制台完成一键授权 |
| 文件存储 NAS         | 安全扫描的漏洞库离线持久化存储， 防止每次都在线请求下载最新的漏洞库                                   |

</service>

推荐您拥有以下的产品权限 / 策略：
<auth>

| 服务/业务   | 权限                        | 备注                                                           |
| ----------- | --------------------------- | -------------------------------------------------------------- |
| 函数计算    | AliyunFCFullAccess          | 安全扫描的逻辑函数需要部署到函数计算                           |
| 硬盘挂载    | AliyunNASFullAccess         | 安全扫描的漏洞库离线持久化存储                                 |
| VPC         | AliyunVPCFullAccess         | NAS 挂载点需要有 VPC                                           |
| EventBridge | AliyunEventBridgeFullAccess | 函数计算操作审计将函数代码包变更事件通过 EB 触发器触发函数执行 |
| 其它        | AliyunECSFullAccess         | 函数计算挂载 NAS 需要有安全组                                  |

</auth>

<remark>

</remark>

<disclaimers>

</disclaimers>

## 部署 & 体验

<appcenter>
   
- :fire: 通过 [Serverless 应用中心](https://fcnext.console.aliyun.com/applications/create?template=start-dependency-check-fc) ，
  [![Deploy with Severless Devs](https://img.alicdn.com/imgextra/i1/O1CN01w5RFbX1v45s8TIXPz_!!6000000006118-55-tps-95-28.svg)](https://fcnext.console.aliyun.com/applications/create?template=start-dependency-check-fc) 该应用。
   
</appcenter>
<deploy>
    
- 通过 [Serverless Devs Cli](https://www.serverless-devs.com/serverless-devs/install) 进行部署：
  - [安装 Serverless Devs Cli 开发者工具](https://www.serverless-devs.com/serverless-devs/install) ，并进行[授权信息配置](https://docs.serverless-devs.com/fc/config) ；
  - 初始化项目：`s init start-dependency-check-fc -d start-dependency-check-fc `
  - 进入项目，并进行项目部署：`cd start-dependency-check-fc && s deploy - y`
   
</deploy>

## 应用详情

<appdetail id="flushContent">

## 注意

EventBridge 开通以后， 请记得一定在 EventBridge 控制台完成一键授权

![](http://image.editor.devsapp.cn/alibaba/1ZskrcBFExw9Fuuadhwz.png)

## 测试

项目部署完成后， 可以通过`invoke`命令(或者在函数计算控制台)进行触发/测试：

```bash
# 调用
$ s invoke -e '{"serviceName":"xiliu-test", "functionName":"test-java8"}'
```

函数调用成功后，会返回生成的 html 报告文件在对象存储 OSS 上的地址， 比如：

```
https://oss.console.aliyun.com/bucket/oss-cn-hangzhou/ali-nangua/object?path=dependency-check/xiliu-test/test-java8/
```

点击进入后， 会看到以时间戳命名的 html 报告：

![](http://image.editor.devsapp.cn/alibaba/vjcduwe85hE2dAwS4kvA.png)

下载 html 报告， 示例如下：

![](http://image.editor.devsapp.cn/alibaba/3d79E3vxge69EqFwB8Ek.png)

</appdetail>

## 使用文档

<usedetail id="flushContent">

当您在该检测函数同 region 进行创建函数或者更新函数的时候， 函数计算操作审计事件会将 fc:Function:CreateSuccess 和 fc:Function:UpdateSuccess 事件通过 EventBridge 触发检测函数的执行

</usedetail>

<devgroup>

## 开发者社区

您如果有关于错误的反馈或者未来的期待，您可以在 [Serverless Devs repo Issues](https://github.com/serverless-devs/serverless-devs/issues) 中进行反馈和交流。如果您想要加入我们的讨论组或者了解 FC 组件的最新动态，您可以通过以下渠道进行：

<p align="center">

| <img src="https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1635407298906_20211028074819117230.png" width="130px" > | <img src="https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1635407044136_20211028074404326599.png" width="130px" > | <img src="https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1635407252200_20211028074732517533.png" width="130px" > |
| --------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| <center>微信公众号：`serverless`</center>                                                                                         | <center>微信小助手：`xiaojiangwh`</center>                                                                                        | <center>钉钉交流群：`33947367`</center>                                                                                           |

</p>
</devgroup>

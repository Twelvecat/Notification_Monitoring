# Notification_Monitoring

基于 DNSPod 用户 API 实现的纯 Shell 动态域名客户端，优先适配网卡地址，无法获得合法外网地址则使用外部接口获取 IP 地址

# 使用方法

- 编辑`ddnspod.sh`，分别修改`/your_real_path/ardnspod`、`arToken`和`arDdnsCheck`为真实信息

- 运行`ddnspod.sh`，开启循环更新任务；建议将此脚本支持添加到计划任务；

- 成功运行后，结果如下所示：

```
Fetching Host Ip
> Host Ip: 11.22.33.55
> Record Type: A
Fetching Ids of test.rehi.org
> Domain Ids: 84982658 766956386
Checking Record for test.rehi.org
> Last Ip: 11.22.33.77
Updating Record for test.rehi.org
> arDdnsUpdate - success
```

### 小提示

- 如需单文件运行，参考`ddnspod.sh`中的配置项，添加到`ardnspod`底部，直接运行`ardnspod`即可

```
echo "arToken=12345,7676f344eaeaea9074c123451234512d" >> ./ardnspod
echo "arDdnsCheck test.org subdomain" >> ./ardnspod
```

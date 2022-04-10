# Notification_Monitoring

用于监测 CUG 各学院网站最新通知，可以选用邮件或微信及时推送。如果需要监测其他学校或单位，可能需要修改 `Notification_Monitoring.py` 中的 `parse_data` 函数。

## 使用方法
 
1. 下载代码
   
```
git clone git@github.com:Twelvecat/Notification_Monitoring.git
```

如果国内网络条件不好也可以使用下面的地址下载：

```
git clone git@gitee.com:twelvecat/notification_-monitoring.git
```

2. 修改配置文件

配置文件为 `config.ini`,首次使用需要根据自身环境和需求修改配置。配置文件的修改请不要增加额外的单引号 `'` 或双引号 `"`,除文件内给出的配置项暂不支持其他配置。

此处的路径建议使用绝对路径，经过测试在 Windows 和 Linux 下均能正常工作。、

```ini
[csv]
path = ./UrlList.csv
```

开启邮件通知需要将 `flag_email= False` 修改为 `flag_email= True`，并添加发送方和接收方的信息，**请注意，部分邮箱的密码并不是登陆密码，而是单独申请的授权码**。

开启微信通知需要将 `flag_wechat = False` 修改为 `flag_wechat= True`，并添加对应的 api 和 key。目前支持 [server酱](https://sct.ftqq.com/) 和 [push plus](http://pushplus.hxtrip.com/)，但都需自行注册账户并修改对应信息。

3. 添加监测网站

支持添加多个监测网站，只需在 `UrlList.csv` 中添加对应的网站即可。由于编码问题，建议使用 **VSCode** 编辑该文件，同时注意 **最后一行不要留空**。

由于需要解析 csv 文件，请按照如下格式添加：

```csv
num,url,0,0,0
```

其中 `num` 为序号，从0索引，按顺序添加。后面 3 个 `0` 分别表示 `当前最新通知`、`网站名称` 和 `网站链接`,写 `0` 后程序会根据访问结果自行添加。  **请不要删除或修改首行标题栏**

举例：

```csv
2,https://au.cug.edu.cn/syyjsjy.htm,0,0,0
```

4. 安装必要的库

如果运行报错说明缺少一些必要的库，请参阅 `Notification_Monitoring.py` 文件的头部进行添加。

目前确定需要单独添加如下库，其余依据个人设备不同自行添加：

```bash
pip install pandas
pip install beautifulsoup4
pip install requests
```

5. 运行程序
   
在文件目录内，运行如下指令即可开启程序，程序会每分钟定时访问 `UrlList.csv` 中添加的网站。并根据配置进行信息推送。

```bash
python Notification_Monitoring.py
```

## 小提示

- 可以取消文件内的死循环，采用定时执行脚本的方式执行
- 建议阅读代码逻辑，根据需要修改至其他网站监测
- 对于不同网站的监测也可以通过识别序列号 `self.urlid` 进行特殊处理和解析
- 若有 bug 可以在 issue 中提交，也可以修复后发起 pull requests

## 参考资料
本项目参考了 [spider-of-CNIC-notice](https://github.com/tianming123/spider-of-CNIC-notice/tree/master)，此处表示感谢。

根据实际需求增加了如下功能：

- 支持多网站监测
- 引入了配置文件
- 增加了微信推送
- 舍弃了通过文章日期来检测是否为最新通知的方法
- 增加了通过文章标题来检测是否为最新通知
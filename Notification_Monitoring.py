import requests
from bs4 import BeautifulSoup
import time
import smtplib
import re
import csv
import pandas as pd
from email.mime.text import MIMEText
from email.header import Header
import configparser

class newNotice(object):
    def __init__(self):
        self.url = ''
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
        }
        self.notice=''
        self.newurl=''
        self.urltitle=''
        self.urlid=''

        self.csvpath=''

        self.flag_email= 'False'
        self.from_addr=''
        self.password=''
        self.smtp_server=''
        self.to_addr=''

        self.flag_wechat= 'False'
        self.server_api_url=''
        self.server_api_key=''


    def get_response(self, url):
        try:
            requests.packages.urllib3.disable_warnings()
            response = requests.get(url, headers=self.headers, verify=False)
            data = response.content
            response.close()
        except requests.exceptions.RequestException as e:
            print("[\terror]", end="")
            print(e)
            temp = "网页请求失败，链接为："+ self.url
            self.send_wechat(temp)
            return -1
        return data

    def data_save(self,data):
        with open('C.html','wb') as file:
            file.write(data)

    def parse_data(self,data):
        soup = BeautifulSoup(data, 'html.parser', from_encoding='gb18030')
        self.urltitle = soup.title.string
        # all = soup.find('div',class_="text_list") #如果是类型则用 class_
        if self.urlid == 13 or self.urlid == 14:
            all = soup.find(id=re.compile(r"^line.*2$"))#正则表达式，此处是基于CUG的通知进行解析，搜寻第一个line开头的id
        else:
            all = soup.find(id=re.compile(r"^line"))#正则表达式，此处是基于CUG的通知进行解析，搜寻第一个line开头的id
        if all == None:   
            print("[\terror]网页解析失败，网页标题：" , self.urltitle)
            temp = "网页请求失败，链接为："+ self.url
            self.send_wechat(temp)
            return -1    
        new_url = self.url +"/../"+ all.a['href']
        self.newurl=new_url
        # print(all.a.text)
        self.notice = all.a.text
        # print(new_url)
        return new_url

    def verify_notification(self):
        data = pd.read_csv(self.csvpath, encoding='utf-8',index_col=0)
        noticeremp = data.loc[self.urlid, '当前最新通知']
        if noticeremp == '0' or noticeremp == 0:
            data.loc[self.urlid, '当前最新通知'] = self.notice
            data.loc[self.urlid, '网站链接'] = self.newurl
            data.loc[self.urlid, '网站名称'] = self.urltitle
            data.to_csv(self.csvpath, encoding='utf-8')
            localtime = time.asctime( time.localtime(time.time()) )
            print("[\ttime]" , localtime)
            print("[\tinfo]网页序号：",self.urlid ," ;网页标题：" , self.urltitle)
            print("[\tinfo]首次访问该网页，已记录最新通知：" , self.notice)
        else:
            if noticeremp != self.notice:
                data.loc[self.urlid, '当前最新通知'] = self.notice
                data.loc[self.urlid, '网站链接'] = self.newurl
                data.loc[self.urlid, '网站名称'] = self.urltitle
                data.to_csv(self.csvpath, encoding='utf-8')
                send_notice = self.notice+"\r\n 网页链接为:"+self.newurl
                localtime = time.asctime( time.localtime(time.time()) )
                print("[\ttime]" , localtime)
                print("[\tinfo]网页序号：",self.urlid ," ;网页标题：" , self.urltitle)
                print("[\tinfo]已发布最新通知：" , self.notice)
                self.send_email(send_notice,self.to_addr)
                self.send_wechat(send_notice)


    def send_email(self,email_body,to_emil):
        if self.flag_email == 'True':
            from_addr = self.from_addr
            password = self.password

            # 收信方邮箱
            to_addr = to_emil
            # 发信服务器
            smtp_server = self.smtp_server

            # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
            msg = MIMEText(email_body, 'plain', 'utf-8')

            # 邮件头信息
            msg['From'] = Header(from_addr)
            msg['To'] = Header(to_addr)
            msg['Subject'] = Header('[通知]'+self.urltitle)

            # 开启发信服务，这里使用的是加密传输
            server = smtplib.SMTP_SSL(smtp_server)
            server.connect(smtp_server, 465)
            # 登录发信邮箱
            server.login(from_addr, password)
            # 发送邮件
            server.sendmail(from_addr, to_addr, msg.as_string())
            # 关闭服务器
            server.quit()
            print("[\tinfo]已发送邮件至：" , self.to_addr)

    def send_wechat(self,res):
        if self.flag_wechat == 'True':
            server_api_key = self.server_api_key
            server_api_url = self.server_api_url
            server_api = server_api_url + server_api_key + ".send"
            data={
                "title": '[通知]'+self.urltitle,
                "desp": res
            }
            header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36'}
            try:
                server_send_ip = requests.get(server_api, params=data, headers=header, timeout=60)
                server_send_ip.close()
            except requests.exceptions.RequestException as e:
                print("[\terror]", end="")
                print(e)     
            print("[\tinfo]已完成微信推送")

    def get_url(self,csvid):
        self.urlid = csvid
        data = pd.read_csv(self.csvpath, encoding='utf-8',index_col=0)
        self.url = data.loc[self.urlid, '监控的网页']

    def run(self,csvid):
        self.get_url(csvid)
        data = self.get_response(self.url)
        if data == -1:
            return
        new_url = self.parse_data(data)
        if new_url == -1:
            return
        self.verify_notification()




conf = configparser.ConfigParser()
conf.read('./config.ini',encoding='utf-8')
Notice = newNotice()
Notice.csvpath = conf.get("csv","path")
Notice.flag_email = conf.get("email","flag_email")
Notice.from_addr = conf.get("email","from_addr")
Notice.password = conf.get("email","password")
Notice.smtp_server = conf.get("email","smtp_server")
Notice.to_addr = conf.get("email","to_addr")
Notice.flag_wechat = conf.get("wechat","flag_wechat")
Notice.server_api_key = conf.get("wechat","server_api_key")
Notice.server_api_url = conf.get("wechat","server_api_url")
last_count = 0

while 1>0:
    count = 0
    with open(Notice.csvpath, 'r',encoding='utf-8') as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            count += 1
    if(count != last_count):
        print("[\tinfo]当前需要监控", count-1 ,"个网页")
        last_count = count
    for i in range(count-1):
        Notice.run(i)
    localtime = time.asctime( time.localtime(time.time()) )
    print("[\ttime]最新更新时间:" , localtime, end='\r')
    time.sleep(60)
    print("                                                      ", end='\r')

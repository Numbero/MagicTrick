#!/usr/bin/python3
#coding=utf-8

import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 文本信息
MAIL_TEXT = '实验室电脑的内网IP是'

# 发送邮件函数
def sendMail():
    # 配置第三方 SMTP 服务
    mail_host="XXX"     # 邮件发件服务器（这里填的是腾讯企业邮箱的smtp服务器）
    mail_user="XXX"  # 用户名(你的邮件地址）
    mail_pass="XXX"          # 邮箱密码
    # 配置邮箱账号
    sender = mail_user                  # 和上面的用户名一致
    receivers = ['XXX']    # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    # 生成邮件
    message = MIMEText(MAIL_TEXT + ip, 'plain', 'utf-8')    # 正文
    message['From'] = Header("IP自动上报", 'utf-8')     # 发件人显示的名字
    message['To'] =  Header("Numbero", 'utf-8')     # 接收人显示的名字
    message['Subject'] = Header('内网IP通知', 'utf-8')  # 标题

    # 发送邮件
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print ("邮件发送成功")
    except smtplib.SMTPException:
        print ("Error: 无法发送邮件")

# 查询当前IP
ip = [a for a in os.popen('route print').readlines() if ' 0.0.0.0 ' in a][0].split()[-2]
print("IP: ",ip)

# 读取历史IP
if os.path.isfile("ip_history"):
    print('发现历史IP记录')
    with open('./ip_history', 'r') as f:
        ip_old = f.read()
    if ip != ip_old:
        print('IP已经发生改变')
        with open('./ip_history', 'w') as f:
            f.write(ip)
        sendMail()
    else:
        print('IP未发生改变')
else:
    print('没有发现历史IP记录')
    with open('./ip_history', 'w') as f:
        f.write(ip)
    sendMail()



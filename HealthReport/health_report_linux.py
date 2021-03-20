from selenium import webdriver
from email.mime.text import MIMEText
from email.header import Header
import os
import sys
import socket
import smtplib
import time

# 常量定义
DRIVE_PATH = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
SLEEP_TIME = 2
MAIL_RECEIVER = 'XXX'

# 发送邮件函数
def sendMail(mailText):
    # 配置第三方 SMTP 服务
    mail_host="XXX"     # 邮件发件服务器（这里填的是腾讯企业邮箱的smtp服务器）
    mail_user="XXX"  # 用户名(你的邮件地址）
    mail_pass="XXX"          # 邮箱密码
    # 配置邮箱账号
    sender = mail_user                  # 和上面的用户名一致
    receivers = MAIL_RECEIVER    # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    # 生成邮件
    message = MIMEText(mailText, 'plain', 'utf-8')    # 正文
    message['From'] = Header('Lab-WorkStation', 'utf-8')     # 发件人显示的名字
    message['To'] =  Header("Numbero", 'utf-8')     # 接收人显示的名字
    message['Subject'] = Header("每日健康填报结果通知", 'utf-8')  # 标题

    # 发送邮件
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print ("邮件发送成功")
    except smtplib.SMTPException:
        print ("Error: 无法发送邮件")

# Linux下使用
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
browser = webdriver.Chrome(chrome_options=chrome_options)

# 打开浏览器
browser.get("http://ehall.seu.edu.cn/new/index.html")

# 用户登录
login = browser.find_element_by_id('ampHasNoLogin')
login.click()
print('- 跳转到登录页面')

username = browser.find_element_by_id("username")
password = browser.find_element_by_id("password")
username.send_keys("XXX")
password.send_keys("XXX")

submit = browser.find_element_by_id("xsfw")
submit.click()
print('- 正在使用用户信息进行登陆')
time.sleep(SLEEP_TIME*2)

# 进入健康填报
health_app = browser.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div/div/div/div/div[3]/div[2]/a[1]')
health_app.click()
print('- 正在进入健康信息填报app')
time.sleep(SLEEP_TIME)

# 进行页面切换
health_window = browser.switch_to.window(browser.window_handles[1])#切换到第二个窗口
print('- 正在切换健康信息填报页面')
time.sleep(SLEEP_TIME)

# 进行健康填报
try:
    add_item = browser.find_element_by_xpath('/html/body/main/article/section/div[2]/div[1]')
except:
    print('- 填报页面还未加载完成')
    time.sleep(SLEEP_TIME*3)
    add_item = browser.find_element_by_xpath('/html/body/main/article/section/div[2]/div[1]')
add_item.click()
print('- 正在进行条目添加')
time.sleep(SLEEP_TIME)
try:
    body_temperature = browser.find_element_by_name("DZ_JSDTCJTW")
    body_temperature.send_keys("36.1")
    save = browser.find_element_by_id("save")
    save.click()
    time.sleep(SLEEP_TIME)
except:
    print('- 已存在填写记录')
    sendMail('今日已进行或错过填报，请手动查看')
else:
    print('- 正在进行今日申报')
    sendMail('今日填报已完成')
ok = browser.find_element_by_class_name('bh-dialog-btn')
ok.click()
time.sleep(SLEEP_TIME)

# 关闭浏览器
browser.quit()
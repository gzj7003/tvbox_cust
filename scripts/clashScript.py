import os
import re
import datetime
import requests
import argparse
import base64
import smtplib
import warnings
from email.mime.text import MIMEText
from email.utils import formataddr

# 禁用 SSL 警告
warnings.filterwarnings('ignore')

# 时间
year = datetime.datetime.today().strftime("%Y") # 指令中间不加#号就自动补零
month = datetime.datetime.today().strftime("%m") # 指令中间不加#号就自动补零
day = datetime.datetime.today().strftime("%d") # 指令中间不加#号就自动补零
date = datetime.datetime.today().strftime("%Y%m%d") # 指令中间不加#号就自动补零

def download_clash():
    # 创建文件夹
    if not os.path.exists("clash"):
        os.mkdir("clash")

    def httpGetText(url):
        try:
            # 禁用 SSL 验证
            req = requests.get(url, verify=False, timeout=30)
            if req.status_code == 200:
                return req.text
        except Exception as e:
            print(f'httpGetText failed: {e}')
        return None

    # 免费节点
    result = httpGetText('https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/clash.yml')
    if result:
        fp = open("clash/Clash.yml", "w+", encoding='utf-8')
        fp.write(result)
        fp.close()
        print("下载 Clash.yml 成功")
        
    # 免费节点1
    result = httpGetText('https://raw.githubusercontent.com/anaer/Sub/main/clash.yaml')
    if result:
        fp = open("clash/Clash1.yml", "w+", encoding='utf-8')
        fp.write(result)
        fp.close()
        print("下载 Clash1.yml 成功")

    # 免费节点2
    result = httpGetText('https://raw.githubusercontent.com/ripaojiedian/freenode/main/clash')
    if result:
        fp = open("clash/Clash2.yml", "w+", encoding='utf-8')
        fp.write(result)
        fp.close()
        print("下载 Clash2.yml 成功")

    # 免费节点3
    result = httpGetText(f"https://clashnode.com/wp-content/uploads/{year}/{month}/{date}.yaml")
    if result:
        fp = open("clash/Clash3.yml", "w+", encoding='utf-8')
        fp.write(result)
        fp.close()
        print("下载 Clash3.yml 成功")
        
    # 免费节点4
    result = httpGetText("https://raw.githubusercontent.com/ssrsub/ssr/master/Clash.yml")
    if result:
        fp = open("clash/Clash4.yml", "w+", encoding='utf-8')
        fp.write(result)
        fp.close()
        print("下载 Clash4.yml 成功")

    # 免费节点5
    result = httpGetText('https://raw.githubusercontent.com/aiboboxx/clashfree/main/clash.yml')
    if result:
        fp = open("clash/Clash5.yml", "w+", encoding='utf-8')
        fp.write(result)
        fp.close()
        print("下载 Clash5.yml 成功")

    # 免费节点6
    result = httpGetText('https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub')
    if result:
        fp = open("clash/Clash6.yml", "w+", encoding='utf-8')
        fp.write(result)
        fp.close()
        print("下载 Clash6.yml 成功")
        
    # 免费节点7
    result = httpGetText('https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/clash.yml')
    if result:
        fp = open("clash/Clash7.yml", "w+", encoding='utf-8')
        fp.write(result)
        fp.close()
        print("下载 Clash7.yml 成功")

# 发送邮件消息
def sendEmail(title, errorMsg):
    ret=True
    try:
        msg=MIMEText(errorMsg,'plain','utf-8')
        msg['From']=formataddr(["GithubAction",my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To']=formataddr(["Bruce",my_user])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject']=title                # 邮件的主题，也可以说是标题
 
        server=smtplib.SMTP_SSL("smtp.163.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender,[my_user,],msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
        print("邮件发送成功")
    except Exception as e:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        print(f"邮件发送失败: {str(e)}")
        ret=False
    return ret


# 给telegram机器人发送消息
def sendTelegramBot(errorMsg):
    ret=True
    try:
        r = requests.post(f'https://api.telegram.org/bot{telegram_bot_token}/sendMessage', 
                         json={"chat_id": telegram_bot_id, "text": errorMsg},
                         timeout=30)
        if r.status_code == 200:
            print("Telegram 消息发送成功")
            ret=True
        else:
            print(f"Telegram 发送失败，状态码: {r.status_code}")
            ret=False
        return ret
    except Exception as e:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        print(f"Telegram 发送异常: {str(e)}")
        ret=False
    return ret

if __name__ == "__main__":
    # 读取github环境变量值
    parser = argparse.ArgumentParser(description='读取secrets')
    parser.add_argument('--telegram_bot_token', type=str, help='telegram_bot_token')
    parser.add_argument('--telegram_bot_id', type=str, help='telegram_bot_id')
    parser.add_argument('--email_sender', type=str, help='email_sender')
    parser.add_argument('--email_pass', type=str, help='email_pass')
    parser.add_argument('--email_receive', type=str, help='email_receive')
    
    # 设置默认值为环境变量，这样在 GitHub Actions 中可以直接使用 secrets
    # 同时允许参数为空，这样脚本可以单独运行下载功能
    args = parser.parse_args()
    
    # 从参数获取值，如果参数为空则尝试从环境变量获取
    my_sender = args.email_sender or os.getenv('EMAIL_SENDER', '')
    my_pass = args.email_pass or os.getenv('EMAIL_PASS', '')
    my_user = args.email_receive or os.getenv('EMAIL_RECEIVE', '')
    telegram_bot_token = args.telegram_bot_token or os.getenv('TELEGRAM_BOT_TOKEN', '')
    telegram_bot_id = args.telegram_bot_id or os.getenv('TELEGRAM_BOT_ID', '')
    
    print("开始下载 Clash 配置文件...")
    
    try:
        # 下载文件
        download_clash()
        print("Clash 配置文件下载完成")
        
        # 如果提供了 Telegram 信息，发送通知
        if telegram_bot_token and telegram_bot_id:
            sendTelegramBot(f"Clash 配置文件下载完成 - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 如果提供了邮箱信息，发送邮件通知
        if my_sender and my_pass and my_user:
            sendEmail("Clash 下载完成", f"Clash 配置文件已成功下载，时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
    except Exception as e:
        error_msg = f"Clash 下载失败: {str(e)}"
        print(error_msg)
        
        # 如果提供了 Telegram 信息，发送错误通知
        if telegram_bot_token and telegram_bot_id:
            sendTelegramBot(error_msg)
        
        # 如果提供了邮箱信息，发送错误邮件
        if my_sender and my_pass and my_user:
            sendEmail("Clash 下载失败", error_msg)

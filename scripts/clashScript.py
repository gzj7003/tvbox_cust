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

    urls = [
        ('https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/clash.yml', 'Clash.yml'),
        ('https://raw.githubusercontent.com/anaer/Sub/main/clash.yaml', 'Clash1.yml'),
        ('https://raw.githubusercontent.com/ripaojiedian/freenode/main/clash', 'Clash2.yml'),
        (f'https://clashnode.com/wp-content/uploads/{year}/{month}/{date}.yaml', 'Clash3.yml'),
        ('https://raw.githubusercontent.com/ssrsub/ssr/master/Clash.yml', 'Clash4.yml'),
        ('https://raw.githubusercontent.com/aiboboxx/clashfree/main/clash.yml', 'Clash5.yml'),
        ('https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub', 'Clash6.yml'),
        ('https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/clash.yml', 'Clash7.yml')
    ]
    
    for url, filename in urls:
        result = httpGetText(url)
        if result:
            filepath = os.path.join("clash", filename)
            with open(filepath, "w+", encoding='utf-8') as fp:
                fp.write(result)
            print(f"下载 {filename} 成功")

# 发送邮件消息
def sendEmail(title, errorMsg):
    try:
        msg=MIMEText(errorMsg,'plain','utf-8')
        msg['From']=formataddr(["GithubAction",my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To']=formataddr(["Bruce",my_user])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject']=title                # 邮件的主题，也可以说是标题
 
        server=smtplib.SMTP_SSL("smtp.163.com", 465)
        server.login(my_sender, my_pass)
        server.sendmail(my_sender,[my_user,],msg.as_string())
        server.quit()
        print("邮件发送成功")
        return True
    except Exception as e:
        print(f"邮件发送失败: {str(e)}")
        return False


# 给telegram机器人发送消息
def sendTelegramBot(errorMsg):
    try:
        r = requests.post(f'https://api.telegram.org/bot{telegram_bot_token}/sendMessage', 
                         json={"chat_id": telegram_bot_id, "text": errorMsg},
                         timeout=30)
        if r.status_code == 200:
            print("Telegram 消息发送成功")
            return True
        else:
            print(f"Telegram 发送失败，状态码: {r.status_code}")
            return False
    except Exception as e:
        print(f"Telegram 发送异常: {str(e)}")
        return False

if __name__ == "__main__":
    # 主要从环境变量读取配置，也支持命令行参数
    parser = argparse.ArgumentParser(description='读取secrets')
    parser.add_argument('--telegram_bot_token', type=str, default="", help='telegram_bot_token')
    parser.add_argument('--telegram_bot_id', type=str, default="", help='telegram_bot_id')
    parser.add_argument('--email_sender', type=str, default="", help='email_sender')
    parser.add_argument('--email_pass', type=str, default="", help='email_pass')
    parser.add_argument('--email_receive', type=str, default="", help='email_receive')
    
    args = parser.parse_args()
    
    # 优先使用环境变量，如果环境变量没有设置则使用命令行参数
    # 这样在 GitHub Actions 中可以使用 env 设置，命令行运行也可以传参
    my_sender = os.getenv('EMAIL_SENDER') or args.email_sender or ''
    my_pass = os.getenv('EMAIL_PASS') or args.email_pass or ''
    my_user = os.getenv('EMAIL_RECEIVE') or args.email_receive or ''
    telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN') or args.telegram_bot_token or ''
    telegram_bot_id = os.getenv('TELEGRAM_BOT_ID') or args.telegram_bot_id or ''
    
    print("开始下载 Clash 配置文件...")
    print(f"当前时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # 下载文件
        download_clash()
        print("Clash 配置文件下载完成")
        
        success_msg = f"Clash 配置文件下载完成 - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        # 如果提供了 Telegram 信息，发送通知
        if telegram_bot_token and telegram_bot_id:
            sendTelegramBot(success_msg)
        else:
            print("未提供 Telegram 配置，跳过发送通知")
        
        # 如果提供了邮箱信息，发送邮件通知
        if my_sender and my_pass and my_user:
            sendEmail("Clash 下载完成", success_msg)
        else:
            print("未提供邮箱配置，跳过发送邮件")
            
    except Exception as e:
        error_msg = f"Clash 下载失败: {str(e)}"
        print(error_msg)
        
        # 如果提供了 Telegram 信息，发送错误通知
        if telegram_bot_token and telegram_bot_id:
            sendTelegramBot(error_msg)
        
        # 如果提供了邮箱信息，发送错误邮件
        if my_sender and my_pass and my_user:
            sendEmail("Clash 下载失败", error_msg)

import sys
import imaplib
import smtplib
import email
import redis
import requests
import json
import apps.login.email_setting as eset

from random import Random
from email.header import Header
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from apps.login.connect_redis import r as conn_redis


# 生成随机字符串
def random_str(randomlength=6):
    """
    随机字符串
    :param randomlength: 字符串长度
    :return: String 类型字符串
    """
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def send_email_by_qq(veri_email,veri_code):
    # 设置总的邮件体对象，对象类型为mixed
    msg_root = MIMEMultipart('mixed')
    # 邮件添加的头尾信息等
    msg_root['From'] = eset.EMAIL_FROM
    msg_root['To'] = veri_email
    # 邮件的主题，显示在接收邮件的预览页面
    subject = 'Register Email Verification'
    msg_root['subject'] = Header(subject, 'utf-8')
   
    mail_msg = '''
<div class = 'title'>
<h3><p>Register Email Verification:</p></h3>
</div>
<p>{}</p>
<div class = 'title'>
'''.format(veri_code)
    msg_root.attach(MIMEText(mail_msg, 'html', 'utf-8'))
    return msg_root

def conn_emial(veri_email,veri_code):
    email_user = eset.EMAIL_HOST_USER
    email_password = eset.EMAIL_HOST_PASSWORD
    try:
        sftp_conn =smtplib.SMTP_SSL(eset.EMAIL_HOST, eset.EMAIL_PORT)
        sftp_conn.login(email_user, email_password)
        msg_root = send_email_by_qq(veri_email,veri_code)
        sftp_conn.sendmail(email_user, veri_email, msg_root.as_string())
        sftp_conn.quit()
        print('sendemail successful!')
        return True
    except Exception as e:
        print('sendemail failed next is the reason')
        print(e)
        return False

def Send_email(veri_email,Username):
	if not conn_redis.get(veri_email):
		veri_code = random_str()
		conn_redis.set(veri_email,veri_code,ex=1800)
	else:
		veri_code = conn_redis.get(veri_email)

	url = 'http://10.225.5.11:8080/Bioinfo/mail.shtml'
	content = """\nThank you for registering at Stereomics. \nYour login is as follows: {} \nVerification code: {}\nThe verification code is valid for 30 minutes,please verify in time.\n\nKind regards,\nThe Stereomics Team""".format(Username,veri_code)
	
	r = requests.post(
	                        url,
	                        data = {
	                                'user' : 'mailEmail',
	                                'passwd' : 'please.Mail.Email',
	                                'receiver': veri_email,
	                                'title': 'Register Email Verification',
	                                'content': content,
	                                'sender': 'zhouliangliang@genomics.cn',  #发件人邮箱
	                                'auth': 'L4L4HfsW6vHxeP9', ##发件人密码
	                        },
	                        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
	                        #headers = {'Content-Type': 'application/json'}
	)
	return eval(r.text)
import sys
import imaplib
import smtplib
import email
import redis
import requests
import json

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
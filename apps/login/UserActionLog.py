import flask
import functools
import datetime
import time
import json
from apps.login.token_verification import veri_token

def logit(Operation=None,logfile='AcationLog.log'):
    def logging_decorator(func):
        @functools.wraps(func)
        def wrapped_function(*args, **kwargs):
            loginName,isTrue = veri_token()
            ip = flask.request.remote_addr
            headers={k:v for k, v in flask.request.headers}
            Url = headers["Referer"]
            if not loginName:
                loginName = 'Not Login'

            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            if not Operation:
                log_string = ']-['.join(['['+ ip, current_time, loginName, Url +"]"])
            else:
                log_string = ']-['.join(['['+ ip, current_time, loginName, Operation +"]"])
            with open(logfile, 'a') as opened_file:
                opened_file.write(log_string + '\n')
            return func(*args, **kwargs)
        return wrapped_function
    return logging_decorator

def logit_detail(Operation=None,order_id='',status='',logfile='AcationLog.log'):
    loginName,isTrue = veri_token()
    ip = flask.request.remote_addr
    headers={k:v for k, v in flask.request.headers}
    Url = headers["Referer"]
    if not loginName:
        loginName = 'Not Login'

    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if 'order' in Operation and 'status' not in Operation:
        log_string = ']-['.join(['['+ ip, current_time, loginName, Operation + order_id +"]"])
    elif 'order' in Operation and 'status' in Operation:
        log_string = ']-['.join(['['+ ip, current_time, loginName, f'Change the order {order_id} status to {status}'+"]"])
    else:
        log_string = ']-['.join(['['+ ip, current_time, loginName, Operation +"]"])
    with open(logfile, 'a') as opened_file:
        opened_file.write(log_string + '\n')

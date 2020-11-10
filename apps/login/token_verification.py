import jwt
import flask
import hashlib
import time

from datetime import datetime,timedelta
from jwt import exceptions

from apps.db.tableService.Users import Users
from apps.login.connect_redis import r


def veri_token():
    user_id = None
    user_name = None
    T = flask.request.cookies.get('T')
    if T:
        token = r.get(T)
        payload,recode = validate_token(token)
        if recode==200:
            user_id = payload['user_id']
            user_name = Users(userid=user_id).getName()
            return user_name,True
        else:
            return user_name,False
    else:
        return user_name,False


def get_payload(user_id='',org='',login_flag='logined'):
    payload = {
                'user_id':user_id,
                'organization':org,
                login_flag:True,
            }
    
    return payload

def validate_token(token):
    '''校验token的函数，校验通过则返回解码信息'''
    SECRET_KEY = '123asgfddasdasdasgerher'
    payload = None
    code = 200
    try:
        payload = jwt.decode(token, SECRET_KEY, True, algorithm='HS256')
        # jwt有效、合法性校验
    except exceptions.ExpiredSignatureError:
        code = 404
    except jwt.DecodeError:
        code = 404
    except jwt.InvalidTokenError:
        code = 404
    return (payload, code)

def create_token(payload,exp_time = None):
    '''基于jwt创建token的函数'''
    if exp_time:
        payload['exp'] = datetime.utcnow() + timedelta(seconds=exp_time)
    SECRET_KEY = '123asgfddasdasdasgerher'
    token = jwt.encode(payload=payload, key=SECRET_KEY, algorithm='HS256')
    # 返回生成的token
    return token
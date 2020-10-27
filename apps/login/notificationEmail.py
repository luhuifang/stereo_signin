import requests
from apps.db.tableService.OrderForm import Orders
from apps.db.tableService.OrderStatus import OrderStatus

def Send_email(order_id):
    # statusDict = {8:'',1:'Check pending',2:'Verified',3:'Unpaid',4:'Paid',5:'Wait for production',6:'In production',7:'assigned',-1:'end'}
    order = Orders()
    order_info = order.getDataByOrderID(order_id)
    statusDict = {}
    orderstatus = OrderStatus()
    allstatus = orderstatus.getAllStatus()
    for eachstatus in allstatus.iloc:
        statusDict[eachstatus['OrderStatusID']] = eachstatus['OrderStatusName']
    notify_email = order_info.iloc[0]['Email']
    order_stutus = statusDict[order_info.iloc[0]['CurrentStatus']]
    notify_objects = {
        'Check pending':['manager_email'],
        'Verified':['customer_email'],
        'Unpaid':['customer_email'],
        'Paid':['manager_email'],
        'Wait for production':['chip_maker_email'],
        'In production':['customer_email'],
        'assigned':['manager_email','customer_email'],
        'end':['manager_email','customer_email']
    }
    email={
    'manager_email':'995287902@qq.com',
    'customer_email':notify_email,
    'chip_maker_email':'995287902@qq.com',
    }
    url = 'http://10.225.5.11:8080/Bioinfo/mail.shtml'
    for each_notify_object in notify_objects[order_stutus]:
        content ='''Order{} has entered '{}' status, Please go to the background for details!\n\n
        Kind regards,\nThe Stereomics Team '''.format(order_id,order_stutus)
        r = requests.post(
                            url,
                            data = {
                                    'user' : 'mailEmail',
                                    'passwd' : 'please.Mail.Email',
                                    'receiver': email[each_notify_object],
                                    'title': 'Notification of order status change',
                                    'content': content,
                                    'sender': 'zhouliangliang@genomics.cn',  #发件人邮箱
                                    'auth': 'Zhou2633658', ##发件人密码
                            },
                            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                            #headers = {'Content-Type': 'application/json'}
        )
        print(r.text)
    # return eval(r.text)
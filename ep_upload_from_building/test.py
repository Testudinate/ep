#/usr/bin/env python
#encoding:utf-8

from mail import send_mail
#from datetime import *  
import datetime

addr=('yangjiaohui@pkpm.com.cn','569538130@qq.com','')
#send_mail('subject','content',addr)

 
email_enable=False 
while 1:
    if datetime.datetime.now().strftime('%H')=='11' : 
        if email_enable==False: 
            subject='Heart beat'
            content='This is from the building.'
            print content
            send_mail(subject,content,addr)
            print 'OK'
            email_enable=True
    else:
        email_enable=False    

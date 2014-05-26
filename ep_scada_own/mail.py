#!/usr/bin/python
#encoding=utf-8 

import smtplib
import sys
import email

from email.mime.text import MIMEText
#========================================
#需要配置
send_mail_host="smtp.163.com"      # 发送的smtp
send_mail_user="ouyangjiaohui@163.com"
send_mail_user_name="ouyangjiaohui"
send_mail_pswd="9yaoyao"
send_mail_postfix="163.com"  #发邮件的域名
 
 
def send_mail(sub,content,to_address):
    '''
    sub:主题
    content:内容
    send_mail("xxxxx@xxx.xxx","主题","内容")
    '''
    if not to_address or len(to_address)==0:
        return False
    send_mail_address=send_mail_user_name+"<"+send_mail_user+">"
    msg=email.mime.text.MIMEText(content)
    msg['Subject']=sub
    msg['From']=send_mail_address 
    try:
        stp = smtplib.SMTP()
        stp.connect(send_mail_host)
        stp.login(send_mail_user,send_mail_pswd)
        for addr in to_address:
            if addr: 
                stp.sendmail(send_mail_address, addr, msg.as_string())
        stp.close()
        return True
    except Exception, e:
        print str(e)
        return False


if __name__ == '__main__':  
    a=('yangjiaohui@pkpm.com.cn','ouyangjiaohui@gmail.com')
    if send_mail(sys.argv[1],sys.argv[2],a):
        print "OK"
    else:
        print 'FAIL'

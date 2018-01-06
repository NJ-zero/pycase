#coding=utf-8
#author='Shichao-Dong'

import os
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.header import Header
from email.mime.multipart import MIMEMultipart

report_dir='D:\\Ptest\zentao\Report'
lists=os.listdir(report_dir)
lists.sort(key=lambda fn:os.path.getmtime(report_dir+"\\"+fn))
file_new=os.path.join(report_dir,lists[-1])
print file_new
#定义发件箱收件箱
smtpsever='smtp.exmail.qq.com'
user='publicer@waiqin365.com'
password='FHuma025'
sender='publicer@waiqin365.com'
receiver='dongshichao@waiqin365.com'
#定义文本
msg=MIMEMultipart()
msg['Subject']=Header('本周上线分析报告','utf-8')
# msg['from']=Header('auto','utf-8')
msg['from']=sender
msg['to']=receiver
#文字部分
part=MIMEText(" Dear all:\n\n"
              "         Attachment is weekly version release details.\n"
              "         Please check it.\n"
              "         Auto sent by jenkins. No reply.\n"
              "         Any questions, please contact zhouhaifeng@waiqin365.com ."
              "\n\n"
              " Best Regards\n"
              " Thanks")
msg.attach(part)
#附件部分
# part=MIMEApplication(open(file_new,'rb').read())
# part.add_header('Content-Disposition', 'attachment', filename="weekly-release-report.xlsx")
# msg.attach(part)
d=datetime.date.today()
filename=str(d)+'-report.xlsx'
att=MIMEText(open(file_new,'rb').read(),'base64','utf-8') #添加附件
att["Content-Type"] = 'application/octet-stream'
att["Content-Disposition"] = 'attachment; filename="%s"'%filename
msg.attach(att)

#发送邮件
smtp=smtplib.SMTP()
smtp.connect(smtpsever)
smtp.login(user,password)
smtp.sendmail(sender,receiver.split(','),msg.as_string())
smtp.quit()
print(u'邮件发送成功')


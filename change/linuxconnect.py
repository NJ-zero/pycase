#coding=utf-8
#author='Shichao-Dong'

import paramiko
import os
import time
report_dir='D:\\Ptest\Report'
lists=os.listdir(report_dir)
lists.sort(key=lambda fn:os.path.getmtime(report_dir+"\\"+fn))
file_new=os.path.join(report_dir,lists[-1])
print file_new

filename = 'index.html'
path = '/home/iorder_appsvr/iorder_appsvr/web/app/visit/h5/report/'
remotepath = path + filename
localpath = r'D:/file/index.html'
bak = filename + str(time.strftime("%y%m%d")) + 'bak'
print remotepath,bak
#执行linux命令
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect('172.31.3.233',22,'root','ZKwaiqin123')
# cmd = "cd '%s';mv '%s' '%s';ls"%(path,filename,bak)
# stdin, stdout, stderr = ssh_client.exec_command(cmd,get_pty=True)
# for line in stdout:
#     print line.strip('\n')

# print u'停掉appsvr进程并重启服务'
# cmd = "cd /home/iorder_appsvr/iorder_appsvr/apache-tomcat-7.0.27/bin;pgrep -f  appsvr;kill  -9  `pgrep -f  appsvr`"
# stdin, stdout, stderr = ssh_client.exec_command(cmd,get_pty=True)
# for line in stdout:
#     print line.strip('\n')
# time.sleep(30)
# cmd = "cd /home/iorder_appsvr/iorder_appsvr/apache-tomcat-7.0.27/bin;ls;./startup.sh "
#执行linux命令

cmd = 'cd /home/iorder ;ls;pwd'
stdin, stdout, stderr = ssh_client.exec_command(cmd,get_pty=True)
for line in stdout:
    print line.strip('\n')
time.sleep(3)




ssh_client.close()

# #传输文件
filename = 'index.html'
path = '/home/iorder_appsvr/iorder_appsvr/web/app/visit/h5/report/'
remotepath = path + filename
localpath = r'D:/file/index.html'
trans = paramiko.Transport(('172.31.3.233',22))
trans.connect(username='root',password='ZKwaiqin123')
sftp = paramiko.SFTPClient.from_transport(trans)
sftp.put(localpath,remotepath)
# # sftp.get(remotepath,localpath)
trans.close()

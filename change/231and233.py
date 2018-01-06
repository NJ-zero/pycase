#coding=utf-8
#author='Shichao-Dong'

import paramiko
import time
import os,os.path

def trans_connect(host,username,password):
    try:
        trans = paramiko.Transport((host,22))
        trans.connect(username=username,password=password)
    except Exception,e:
        print e
    return trans

def trans_web(trans,remotepath,localpath):
    sftp = paramiko.SFTPClient.from_transport(trans)
    sftp.put(localpath,remotepath)
    trans.close()

def ssh_connect(host,username,password):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(host,22,username,password)
    except Exception ,e:
        print e
    return ssh_client

def ssh_exec_cmd(ssh_client,cmd,arg):
    return ssh_client.exec_command(cmd,arg)

def ssh_close(ssh_client):
    ssh_client.close()

def main():
    host = '172.31.3.231'                           #---------依次部署231/233------------
    username = 'root'
    password = 'ZKwaiqin123'
    remotepath = '/opt/web/web.zip'
    localpath = r'D:/file/web.zip'                  #--------地址请按实际情况修改------------
    #删除并创建新的web文件夹
    print u'开始删除opt下web，并创建新web\n'
    cmd = 'cd /opt;rm -rf web;mkdir web;ls'
    arg = 'get_pty=True'
    ssh_client=ssh_connect(host,username,password)
    stdin, stdout, stderr = ssh_exec_cmd(ssh_client,cmd,arg)
    for line in stdout:
        print line.strip('\n')
    ssh_close(ssh_client)

    #上传文件
    print u'开始上传文件\n'
    trans = trans_connect(host,username=username,password=password)
    trans_web(trans,remotepath=remotepath,localpath=localpath)

    #解压并删除压缩包
    print u'解压并删除压缩包\n'
    cmd = 'cd /opt/web;ls;unzip web.zip;rm -rf web.zip;ls'
    ssh_client=ssh_connect(host,username,password)
    stdin, stdout, stderr = ssh_exec_cmd(ssh_client,cmd,arg)
    for line in stdout:
        print line.strip('\n')
    ssh_close(ssh_client)

    #备份需要替换的文件
    print u'开始备份需要替换的文件'
    path=r'D:\\file\\web'
    fns=[os.path.join(root,fn) for root,dirs,files in os.walk(path) for fn in files]
    for f in fns:
        oldfile = '/home/iorder_appsvr/iorder_appsvr'+ str(f[9:].replace('\\','/'))
        newfile = oldfile +  str(time.strftime("%y%m%d")) + 'bak'
        cmd = "mv %s  %s"%(oldfile,newfile)
        ssh_client=ssh_connect(host,username,password)
        stdin, stdout, stderr = ssh_exec_cmd(ssh_client,cmd,arg)
        for line in stdout:
            print line.strip('\n')
        ssh_close(ssh_client)
        time.sleep(1)
    print(u'总计：'+ str(len(fns)) +u'个   备份完成')

    #复制文件至appsvr
    ssh_client=ssh_connect(host,username,password)
    cmd = '\cp -Rf /opt/web/   /home/iorder_appsvr/iorder_appsvr/'
    stdin, stdout, stderr = ssh_exec_cmd(ssh_client,cmd,arg)
    for line in stdout:
        print line.strip('\n')
    time.sleep(4)

    #重启服务
    print u"是否需要重启服务器，是请输入1，否请输入0"
    result = raw_input(u'是否需要重启服务器：')
    result = int(result)
    if result == 1:
        cmd = 'service  tomcat_iorder_appsvr  restart'
        arg = 'get_pty=False'
        ssh_client=ssh_connect(host,username,password)
        stdin, stdout, stderr = ssh_exec_cmd(ssh_client,cmd,arg)
        for line in stdout:
            print line.strip('\n')
        time.sleep(2)
        ssh_close(ssh_client)
    else:
        ssh_close(ssh_client)

if __name__ == "__main__":
    main()
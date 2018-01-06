#coding=utf-8
#author='Shichao-Dong'

import time
import paramiko


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
    host = '172.31.3.233'  # ---------依次部署231/233------------
    username = 'root'
    password = 'ZKwaiqin123'
    filename = 'FlowExe.class'  # ------请手动填写------
    path = '/home/iorder_appsvr/iorder_appsvr/web/WEB-INF/classes/com/fh/iasp/platform/app/vo/'  # -----请手动填写-----
    remotepath = path + filename
    localpath = 'D:/file/' + filename
    bak = filename + str(time.strftime("%y%m%d")) + 'bak'
    print remotepath, bak
    # 备份替换文件
    print u'备份替换文件\n'
    cmd = "cd '%s';mv '%s' '%s';ls" % (path, filename, bak)
    arg = 'get_pty=True'
    ssh_client = ssh_connect(host, username, password)
    stdin, stdout, stderr = ssh_exec_cmd(ssh_client, cmd, arg)
    for line in stdout:
        print line.strip('\n')
    time.sleep(2)
    ssh_close(ssh_client)
    # 上传文件
    print u'开始上传替换文件\n'
    trans = trans_connect(host, username=username, password=password)
    trans_web(trans, remotepath=remotepath, localpath=localpath)
    time.sleep(3)
    # 重启服务
    print u"是否需要重启服务器，是请输入1，否请输入0"
    result = raw_input(u'是否需要重启服务器：')
    result = int(result)
    if result == 1:
        cmd = 'service  tomcat_iorder_appsvr  restart'
        arg = 'get_pty=False'
        ssh_client = ssh_connect(host, username, password)
        stdin, stdout, stderr = ssh_exec_cmd(ssh_client, cmd, arg)
        for line in stdout:
            print line.strip('\n')
        time.sleep(3)
        ssh_close(ssh_client)
    else:
        ssh_close(ssh_client)

if __name__ == "__main__":
    main()

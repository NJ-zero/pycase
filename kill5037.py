#coding=utf-8
#author='Shichao-Dong'

import os
import subprocess

def kill():
    result = subprocess.Popen('netstat -ano | findstr "5037"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.readlines()
    print result[0].split()
    if 'LISTENING' in result[0].split():
        print result[0].split()[4]
        kill = 'taskkill /F /PID '+''.join(str(result[0].split()[4]))
        print kill
        result = subprocess.Popen(kill, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.readlines()
        print result
    else:
        print '5037端口未被占用没有'



kill()
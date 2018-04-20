# coding=utf-8
# author='Shichao-Dong'
# create time 2018/4/17

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import json

def read(path):
    try:
        f = open(path)
        lines = f.readlines()
        f.close()
        return lines
    except:
        print('无法找到文件')

def writejson(txt,newfile):
    lines = read(txt)
    newjson = {}
    for line in lines:
        print(line.split()[1].decode('utf-8'))
        value = line.split()[1].decode('utf-8')
        newjson[line.split()[0]] = value

    jsonobj = json.dumps(newjson).decode('unicode-escape')
    print(jsonobj)

    f =  open(newfile,'w')
    f.write(jsonobj)
    f.close()
    print('生成文件成功')



writejson('str.txt','json.txt')
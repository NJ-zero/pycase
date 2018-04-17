# coding=utf-8
# author='Shichao-Dong'
# create time 2018/4/17

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
        newjson[line.split()[0]] = line.split()[1]
    jsonobj = json.dumps(newjson)
    try:
        f =  open(newfile,'w')
        f.write(jsonobj)
        f.close()
        print('生成文件成功')
    except:
        print('转化失败')

writejson('str.txt','json.txt')
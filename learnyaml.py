#coding=utf-8
#author='Shichao-Dong'

# ----------------
# yaml语法学习
# ----------------
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import yaml
import codecs

#
# with codecs.open('data.yaml','r','utf-8') as f:
#     for data in  yaml.load_all(f):
#         print data
#     f.close()

f=open('data.yaml')
for data in yaml.load_all(f):
    print repr(data).decode('unicode-escape')
#
# f=open('data.yaml',)
# data = yaml.load(f)
# print data
# print (repr(data).decode('unicode-escape'))
# print data['cus'][0].decode('utf-8')
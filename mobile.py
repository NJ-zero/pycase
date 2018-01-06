#coding=utf-8
#author='Shichao-Dong'

import random
from datetime import datetime,timedelta

path = 'D:\Ptest\Testcase\districtcode.txt'
def mobile():
    list=['130','131','132','133','134','135','138','139','150','151','152','154','156','157','158','159','187','188','189']
    num1 = random.choice(list)
    # mobile = num1 + ''.join(random.choice("0123456789") for i in range(8))
    num2=[]
    num3=''
    num4='0123456789'
    for i in range(8):
        num2.append(random.choice(num4))
        num3=''.join(num2)
    print num1+num3
    return mobile

path = 'D:\Ptest\Testcase\districtcode.txt'

#获取地区code即前6位
def dist():
    distcode = []
    with open(path) as file:
        dicts = file.read()
        dict = dicts.split('\n')
    for code in dict :
        if code != '':
            distcode.append(code[0:6])
    print distcode
    return distcode

#生成身份证号码即地区code+生日+后4位
def credit():
    code = dist()
    code = str(random.choice(code))
    year = str(random.randint(1950,2000))
    month = (datetime.today() + timedelta(days = (random.randint(0,365)))).strftime('%m%d')
    id = str(random.randint(100,299))
    creditnum = code + year + month + id
    print creditnum
    #权重位计算
    i= 0
    count = 0
    weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2] #权重项
    checkcode ={'0':'1','1':'0','2':'X','3':'9','4':'8','5':'7','6':'6','7':'5','8':'5','9':'3','10':'2'} #校验码映射
    for i in range(0,len(creditnum)):
        count = count + int(creditnum[i]*weight[i])

    last = str(count%11)
    lastcode = checkcode[last]
    credit = creditnum + ''.join(lastcode)
    print credit
    return credit

if __name__=="__main__":
    mobile()
    credit()
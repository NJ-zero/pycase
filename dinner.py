# coding=utf-8
# author='Shichao-Dong'
# create time: 2018/6/25 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from random import randint

print('-----开始摇奖-----')
print('\t  .\n\t  .\n\t  .\n结果出来啦，如下：')
staff = ['龚晖','张瑶','董时超','任波','田贞彪','张家胜','施帅钢','汪超']
lenstaff = len(staff)
def rand():
    '''
    随机数生成，set去重
    :return: 随机数
    '''
    try:
        num = [randint(0, 100) for i in range(lenstaff)]
        print(num)
        if len(set(num)) == len(num):
            return num
        else:
            return None
    except:
        print('请再试一次')

def select():
    '''
    选出数字最小的同学
    :return:
    '''
    num = rand()
    if num is not None:
        dinner = dict(zip(staff, num))
        dinner = sorted(dinner.items(), key=lambda x: x[1])
        print(dinner)
        print('{}最小，今天拿饭卡'.format(staff[num.index(min(num))]))
    else:
        print('有重复随机数，请再试一次')

select()
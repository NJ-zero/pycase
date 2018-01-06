#coding=utf-8
#author='Shichao-Dong'

from PIL import Image
import math
import operator

def compare(pic1,pic2):
    '''
    :param pic1: 图片1路径
    :param pic2: 图片2路径
    :return: 返回对比的结果
    '''
    image1 = Image.open(pic1)
    image2 = Image.open(pic2)

    histogram1 = image1.histogram()
    print histogram1
    histogram2 = image2.histogram()
    print histogram2

    differ = math.sqrt(reduce(operator.add, list(map(lambda a,b: (a-b)**2,histogram1, histogram2)))/len(histogram1))

    print list(map(lambda a,b: (a-b)**2,histogram1, histogram2))
    print reduce(operator.add, list(map(lambda a,b: (a-b)**2,histogram1, histogram2)))
    print differ
    return differ


compare(r'D:\Ptest\Testcase\11.jpg',r'D:\Ptest\Testcase\22.jpg')
# coding=utf-8
# author='Shichao-Dong'
# create time: 2018/10/15

import os
import jieba
import copy

def remove_list(file="E:\分词&相似度\政府工作报告\stopwords.txt"):
    '''
    创建停用词list
    :return:
    '''
    remove_list = [line.strip() for line in open(file, 'r').readlines()]
    return remove_list

def get_localfiles(path):
    '''
    获取文件夹下所有报告地址, list返回
    :param path: 文件夹地址
    :return:
    '''
    #path="E:\分词&相似度\政府工作报告\安徽省"
    local_files = []
    for parent,dirnames,filename_lists in os.walk(path):
        for file in filename_lists:
            file = os.path.join(parent,file)
            # print(file)
            local_files.append(file)
    print(local_files)
    return local_files

def comparefile(file_1,file_2):
    '''
    比较两个文件年份是否相同
    :return:
    '''
    if file_1[-8:] == file_2[-8:] :
        return True
    else:
        return False

def jieba_result(file):
    '''
    读取文件并 获取jieba分词结果，并去掉中文符号
    :param file:
    :return: 返回 分词结果 list
    '''
    try:
        f = open(file)
        all=f.read()
        f.close()

        res = jieba.lcut(all)
        for i in remove_list():
            while i in res:
                res.remove(i)
        return res
    except:
        print(file,"未找到")

def top_n(res,n=1000):
    '''
    获得分词的TOP n
    :param res: jieba_result返回的结果
    :param n:
    :return:
    '''
    dic={}
    for item in res:
        if item in dic:
            dic[item] += 1
        else:
            dic[item] = 1

    sort_res= sorted(dic.items(), key=lambda x: x[1], reverse=True) #排序

    top_n = sort_res[:n]  #获取Top n
    top_n_res=[ i[0] for i in top_n]
    return top_n_res

def res_all(res_gwy,res_anhui):
    '''
    合并并去重
    :return:
    '''
    new_res = copy.deepcopy(res_gwy)
    for i in res_anhui:
        new_res.append(i)
    res_all=list(set(new_res))
    return res_all

def get_list(jieba_res,res_all):
    '''
    获取anhui 和  gwy 的向量
    :param res_1:
    :param res_all:
    :return:
    '''
    dic={}
    for i in res_all:
        if i not in jieba_res:
            dic[i] = 0
        else:
            dic[i] = jieba_res.count(i)

    sort_dic = sorted(dic.items(),key=lambda x:x[0] ) #排序，确保key相同
    getlist = []
    for i in sort_dic:
        getlist.append(i[1])
    return getlist   #得出词频向量


def CalculateCos(gwyList, subList):
    '''
    根据两个词频向量，算出cos值
    :param gwyList:
    :param subList:
    :return:
    '''
    gwyLen = 0
    for gwynum in gwyList:
        gwyLen = gwyLen + gwynum ** 2
    gwyLen = gwyLen ** 0.5
    subLen = 0
    for sub in subList:
        subLen = subLen + sub ** 2
    subLen = subLen ** 0.5
    # return subLen
    totalLen = len(gwyList)
    fenmu = 0
    for i in range(0,totalLen):
        fenmu = fenmu + subList[i] * gwyList[i]
    print(fenmu / (subLen * gwyLen))
    return fenmu / (subLen * gwyLen)


anhui_path="E:\分词&相似度\政府工作报告\安徽省"
anhui_files = get_localfiles(anhui_path)
gwy_path="E:\分词&相似度\政府工作报告\国务院\国务院"
gwy_files = get_localfiles(gwy_path)

len_anhui = len(anhui_files)
len_gwy = len(gwy_files)

for i in range(len_anhui):
    for j in range(len_gwy):
        if comparefile(anhui_files[i],gwy_files[j]):   #对比文件，保证年份相同
            anhui_jieba = jieba_result(anhui_files[i])
            gwy_jieba = jieba_result(gwy_files[j])

            anhui_top = top_n(anhui_jieba,1000)
            gwy_top = top_n(gwy_jieba,1000)
            anhui_gwy_all = res_all(anhui_top,gwy_top)

            anhuilist = get_list(anhui_jieba,anhui_gwy_all)
            gwylist = get_list(gwy_jieba,anhui_gwy_all)

            cosres = CalculateCos(gwylist,anhuilist)
            ss = "\n" + str(anhui_files[i].split("\\")[-1]) + "  " + str(cosres)
            try:
                f = open('result.txt', 'a')
                f.write(str(ss))
                f.close()
            except:
                print("write result fail")
            print("==" + str(i) + "===" + str(j) + "===")
            break






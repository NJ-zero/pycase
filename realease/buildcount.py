#coding=utf-8
#author='Shichao-Dong'

import psycopg2
import time
import datetime
import xlsxwriter

#连接数据库
conn=psycopg2.connect(database='iorder_master',user='postgres',password='FHuma025',host='172.31.3.232',port='5432')
cur=conn.cursor()
date_from='2017-07-06'
date_to=str(datetime.date.today()+datetime.timedelta(days=1))
#新建表格
today=time.strftime("%y-%m-%d")
filename='D:/Ptest/zentao/'+today+'buildcount.xlsx'
workbook = xlsxwriter.Workbook(filename)
worksheet = workbook.add_worksheet('detail')
#设置格式
format_center=workbook.add_format({'bold': True, 'bg_color': 'blue','align':'center','valign':'vcenter','font_size':'16','border':1})
format1=workbook.add_format({'bold':True,'align':'center','valign':'vcenter','border':1})
format2=workbook.add_format({'bold':True,'border':1,'align':'vjustify'})
worksheet.set_column("A:A",60)
worksheet.set_column("B:B",60)
worksheet.set_column("C:C",10)
worksheet.set_column("D:D",10)
worksheet.set_column("E:E",30)
i=1
while i<2000:
    for j in range(5):
        worksheet.set_row(i,20)
        worksheet.write(i,j,'',format1)
    i=i+1
#写入表头
worksheet.merge_range('A1:E1',u'全部build汇总',format_center)
worksheet.write('A2',u'build名称',format1)
worksheet.write('B2',u'build地址',format1)
worksheet.write('C2',u'版本号',format1)
worksheet.write('D2',u'build号',format1)
worksheet.write('E2',u'创建时间',format1)
#查询并写入数据
sql="SELECT app_name,app_url,version,build,create_time FROM svr_deployment WHERE create_time < '%s' AND create_time > '%s';"%(date_to,date_from)
cur.execute(sql)
results = cur.fetchall()
rows = len(results)
for i in range(rows):
    worksheet.write(i+2,0,str(results[i][0]),format2)
for i in range(rows):
    worksheet.write(i+2,1,str(results[i][1]),format2)
for i in range(rows):
    worksheet.write(i+2,2,str(results[i][2]),format2)
for i in range(rows):
    worksheet.write(i+2,3,str(results[i][3]),format2)
for i in range(rows):
    worksheet.write(i+2,4,str(results[i][4]),format2)
#关闭数据库和表格
conn.close()
workbook.close()
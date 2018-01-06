#coding=utf-8
#author='Shichao-Dong'
#=======================
#仅用于禅道报告产出
#=======================

import xlsxwriter
import time,datetime,calendar
import MySQLdb
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
#连接数据库
db=MySQLdb.connect('172.31.3.109','root','111111','zentao')
cursor = db.cursor()
cursor.execute('SET NAMES UTF8')
#定义开始时间结束时间
d=datetime.date.today()

#本周
weekday=d.isoweekday()
before=weekday-1
dayfrom=d - datetime.timedelta(days=before)
sixdays = datetime.timedelta(days=6)
dayto = dayfrom + sixdays
date_from = datetime.datetime(dayfrom.year, dayfrom.month, dayfrom.day, 0, 0, 0)
date_to = datetime.datetime(dayto.year, dayto.month, dayto.day, 23, 59, 59)
#本月
'''
year = d.year
month = d.month
day = d.day
firstday,monthrange=calendar.monthrange(year,month)
dayfrom = datetime.date(year=year, month=month, day=1)
dayto = datetime.date(year=year, month=month, day=monthrange)
date_from = datetime.datetime(dayfrom.year, dayfrom.month, dayfrom.day, 0, 0, 0)
date_to = datetime.datetime(dayto.year, dayto.month, dayto.day, 23, 59, 59)
'''
#新增报告
filename='D:/Ptest/zentao/Report/'+str(d)+'-report.xlsx'
workbook = xlsxwriter.Workbook(filename)
worksheet = workbook.add_worksheet('weeklysummary')
worksheet2 = workbook.add_worksheet('productdetail')
#设置格式
format_center=workbook.add_format({'bold': True, 'bg_color': '#008000','align':'center','valign':'vcenter','font_size':'16','border':1})
format1=workbook.add_format({'bold':True,'align':'center','valign':'vcenter','border':1})
format2=workbook.add_format({'bold':True,'border':1,'align':'vjustify'})
format3=workbook.add_format({'bold':True,'align':'center','valign':'vcenter','border':1,'bg_color':'#B0C4DE'})
worksheet.set_row(0,30)
worksheet.set_column("A:A",15)
worksheet.set_column("B:B",10)
worksheet.set_column("C:C",14)
worksheet.set_column("D:L",13)

i=2
while i<100:
    worksheet.set_row(i,20)
    i=i+1
worksheet.merge_range('A1:L1',u'本周上线总结',format_center)
i=15
while i<100:
    worksheet.set_row(i,25)
    worksheet.merge_range(i,4,i,7,'',format2)
    worksheet.merge_range(i,8,i,11,'',format2)
    i=i+1
#查询上线类型次数 749：标准版本 748：替换文件
sql = "SELECT COUNT(*) FROM zt_doc WHERE module = '749' and deleted= '0' and addedDate >'%s' and  addedDate < '%s'"%(date_from,date_to)
cursor.execute(sql)
results1=cursor.fetchall()
for result1 in results1:
    print u'标准版本：'+str(result1[0])
sql="SELECT COUNT(*) FROM zt_doc WHERE module = '748' and deleted= '0' and addedDate >'%s' and  addedDate < '%s'"%(date_from,date_to)
cursor.execute(sql)
results2=cursor.fetchall()
for result2 in results2:
    print u'替换文件：'+str(result2[0])
sql="SELECT COUNT(*) FROM zt_doc WHERE  deleted= '0' and addedDate >'%s' and  addedDate < '%s'"%(date_from,date_to)
cursor.execute(sql)
results3=cursor.fetchall()
for result3 in results3:
    print u'总次数：'+str(result3[0])

worksheet.write('A3',u'上线类型',format1)
worksheet.write('B3',u'次数',format1)
worksheet.write('A4',u'替换文件',format1)
worksheet.write('B4',result2[0],format1)
worksheet.write('A5',u'标准版本',format1)
worksheet.write('B5',result1[0],format1)
worksheet.write('A6',u'合计',format1)
worksheet.write('B6',result3[0],format1)

#新建图表
chart1=workbook.add_chart({'type':'column'})
chart1.add_series({
    'name':u'次数',
    'categories':'=weeklysummary!$A$4:$A$5',
    'values':'=weeklysummary!$B$4:$B$5',
    'fill': {'color':'#FF9900'},
})
chart1.set_x_axis({
    'name':u'上线类型',
    'name_font':{'size':12},
})
chart1.set_y_axis({
    'name':u'上线次数',
    'name_font':{'size':12,'bold':True},
    'num_font':{'italic':True},
})
chart1.set_title({'name': u'本周上线类型分析'})
chart1.set_style(3)
worksheet.insert_chart('E3',chart1)

#设置上线详情格式
i=15
while i<100:
    for j in range(9):
        worksheet.write(i,j,'',format2)
    i=i+1
worksheet.merge_range('E15:H15',u'上线标题',format3)
worksheet.merge_range('I15:L15',u'上线内容',format3)
worksheet.write('A15',u'上线时间',format3)
worksheet.write('B15',u'上线类型',format3)
worksheet.write('C15',u'负责人',format3)
worksheet.write('D15',u'所属模块',format3)
'''
worksheet.merge_range('A10:B10',u'上线类型说明',format1)
worksheet.write('A11',u'标准版本：',format1)
worksheet.write('A12',u'替换文件：',format1)
worksheet.write('B10','',format1)
worksheet.write('B11',u'749',format1)
worksheet.write('B12',u'748',format1)
'''
#写入上线时间
sql ="SELECT * FROM zt_doc WHERE  deleted= '0' and addedDate >'%s' and  addedDate < '%s'  ORDER BY addedDate;"%(date_from,date_to)
cursor.execute(sql)
results4=cursor.fetchall()
time=[]
for result4 in results4:
    time.append(str(result4[13])[0:10])
rows=len(time)
for i in range(rows):
    worksheet.write(i+15,0,str(time[i]),format2)
#写入上线类型
sql="SELECT module FROM zt_doc WHERE  deleted= '0' and addedDate >'%s' and  addedDate < '%s'  ORDER BY addedDate;"%(date_from,date_to)
cursor.execute(sql)
results5=cursor.fetchall()
rows2=len(results5)
for i in range(rows2):
    worksheet.write(i+15,1,str(results5[i])[2:-3].replace('748',u'替换文件').replace('749',u'标准版本'),format2)
#写入上线负责人
sql = "SELECT addedBy FROM zt_doc WHERE  deleted= '0' and addedDate >'%s' and  addedDate < '%s'  ORDER BY addedDate;"%(date_from,date_to)
cursor.execute(sql)
results6=cursor.fetchall()
rows3=len(results6)
for i in range(rows3):
    worksheet.write(i+15,2,str(results6[i])[2:-3],format2)
#写入上线标题
cursor.execute('SET NAMES UTF8')
sql = "SELECT * FROM zt_doc WHERE deleted = '0' and addedDate >'%s' and  addedDate < '%s'  ORDER BY addedDate;"%(date_from,date_to)
cursor.execute(sql)
results=cursor.fetchall()
title=[]
for result in results:
    #print (result[5][0:])
    result55=str(result[5])
    title.append(result55)
row4=len(title)
for i in range(row4):
    # print str(a[i]).decode('utf-8').encode('gbk')
    worksheet.write_string(i+15,4,str(title[i]),format2)
#写入上线内容
cursor.execute('SET NAMES UTF8')
sql = "SELECT * FROM zt_doc WHERE deleted = '0' and addedDate >'%s' and  addedDate < '%s'  ORDER BY addedDate;"%(date_from,date_to)
cursor.execute(sql)
results=cursor.fetchall()
content=[]
for result in results:
    result66=str(result[9])
    content.append(result66)
row6=len(content)
for i in range(row6):
    worksheet.write_string(i+15,8,str(content[i]).replace('<p>','').replace('</p>','').replace('<br />',''),format2)
#写入所属模块
sql1="SELECT product FROM zt_doc WHERE  deleted= '0' and addedDate >'%s' and  addedDate < '%s'  ORDER BY addedDate;"%(date_from,date_to)
cursor.execute(sql1)
results4=cursor.fetchall()
product1=[]
for result4 in results4:
    product1.append(str(result4[0]))
product2=[]
for i in range(len(product1)):
    cursor.execute('SET NAMES UTF8')
    sql="SELECT * FROM `zt_product` WHERE id = %s"%(product1[i])
    cursor.execute(sql)
    results4=cursor.fetchall()
    for result in results4:
        product2.append(result[1])
    worksheet.write_string(i+15,3,product2[i],format2)

'''
第二个sheet
'''
#各模块之前对比
worksheet2.set_row(0,30)
worksheet2.set_column("A:A",16)
worksheet2.set_column("B:D",10)
worksheet2.set_column("E:I",14)
i=2
while i<50:
    worksheet2.set_row(i,20)
    i=i+1
worksheet2.merge_range('A1:I1',u'模块及产品线上线详情',format_center)
worksheet2.write('A3',u'所属模块',format1)
worksheet2.write('B3',u'标准版本',format1)
worksheet2.write('C3',u'替换文件',format1)

#查询上线模块
sql="SELECT * FROM `zt_product` WHERE id in (SELECT product FROM zt_doc WHERE  deleted= '0' and addedDate >'%s' and  addedDate < '%s'  ORDER BY addedDate) ORDER BY id;"%(date_from,date_to)
cursor.execute(sql)
results7=cursor.fetchall()
product3=[]
for result in results7:
    product3.append(result[1])
for i in range(len(product3)):
    worksheet2.write(i+3,0,str(product3[i]),format1)

#查询分别查询各模块
sql1="SELECT DISTINCT product FROM zt_doc WHERE  deleted= '0' and addedDate >'%s' and  addedDate < '%s'  ORDER BY product;"%(date_from,date_to)
cursor.execute(sql1)
results4=cursor.fetchall()
product1=[]
for result4 in results4:
    product1.append(str(result4[0]))

#查询替换文件
for i in range(len(product1)):
    sql = "SELECT COUNT(*) FROM zt_doc WHERE  module = '748' and deleted= '0'  and product ='%s' and addedDate >'%s' and  addedDate < '%s'  ORDER BY addedDate"%(product1[i],date_from,date_to)
    cursor.execute(sql)
    results7=cursor.fetchall()
    total=[]
    for result in results7:
        total.append(str(result[0]))
    worksheet2.write(i+3,2,int(total[0]),format1)

#查询标准版本
for i in range(len(product1)):
    sql = "SELECT COUNT(*) FROM zt_doc WHERE  module = '749' and deleted= '0'  and product ='%s' and addedDate >'%s' and  addedDate < '%s'  ORDER BY addedDate"%(product1[i],date_from,date_to)
    cursor.execute(sql)
    results7=cursor.fetchall()
    total2=[]
    for result in results7:
        total2.append(str(result[0]))
    worksheet2.write(i+3,1,int(total2[0]),format1)

#新建图表
chart2=workbook.add_chart({'type':'column'})
chart2.add_series({
    'name':u'标准版本',
    'categories':'=productdetail!$A$4:$A$13',
    'values':'=productdetail!$B$4:$B$13',
    'fill': {'color':'#AB82FF'},
})
chart2.add_series({
    'name':u'替换文件',
    'categories':'=productdetail!$A$4:$A$13',
    'values':'=productdetail!$C$4:$C$13',
    'fill': {'color':'#9AFF9A'},
})
chart2.set_x_axis({
    'name':u'所属模块',
    'name_font':{'size':12},
})
chart2.set_y_axis({
    'name':u'上线次数',
    'name_font':{'size':12,'bold':True},
    'num_font':{'italic':True},
})
chart2.set_title({'name': u'模块上线类型对比'})
chart2.set_style(3)
worksheet2.insert_chart('E3',chart2)

#产品之间对比
dingzhi=['16']
DMS=['10','12','13','19','26','27','33','30','31','32']
PAAS=['1','3','11','18','35']
SFA=['2','4','5','8','9','14','15','24','17','20','21','22','25','28','29','34','36']

worksheet2.write('A20',u'所属产品线',format1)
worksheet2.write('B20',u'标准版本',format1)
worksheet2.write('C20',u'替换文件',format1)
worksheet2.write('A21',u'SFA',format1)
worksheet2.write('A22',u'PAAS',format1)
worksheet2.write('A23',u'进销存',format1)
worksheet2.write('A24',u'定制项目',format1)

#写入每个产品线上线数据
#SFA
sql = "SELECT COUNT(*) FROM zt_doc WHERE  module = '749' and deleted= '0'  and product in ('2','4','5','8','9','14','15','24','17','20','21','22','25','28','29','34','36') and addedDate >'%s' and  addedDate < '%s'  ORDER BY addedDate"%(date_from,date_to)
cursor.execute(sql)
result=cursor.fetchall()
worksheet2.write('B21',int(result[0][0]),format1)
sql = "SELECT COUNT(*) FROM zt_doc WHERE  module = '748' and deleted= '0'  and product in ('2','4','5','8','9','14','15','24','17','20','21','22','25','28','29','34','36') and addedDate >'%s' and  addedDate < '%s'  ORDER BY addedDate"%(date_from,date_to)
cursor.execute(sql)
result=cursor.fetchall()
worksheet2.write('C21',int(result[0][0]),format1)
#PAAS
sql = "SELECT COUNT(*) FROM zt_doc WHERE  module = '749' and deleted= '0'  and product in ('1','3','11','18','35') and addedDate >'%s' and  addedDate < '%s'  ORDER BY addedDate"%(date_from,date_to)
cursor.execute(sql)
result=cursor.fetchall()
worksheet2.write('B22',int(result[0][0]),format1)
sql = "SELECT COUNT(*) FROM zt_doc WHERE  module = '748' and deleted= '0'  and product in ('1','3','11','18','35') and addedDate >'%s' and  addedDate < '%s'  ORDER BY addedDate"%(date_from,date_to)
cursor.execute(sql)
result=cursor.fetchall()
worksheet2.write('C22',int(result[0][0]),format1)
#进销存
sql = "SELECT COUNT(*) FROM zt_doc WHERE  module = '749' and deleted= '0'  and product in ('10','12','13','19','26','27','33','30','31','32') and addedDate >'%s' and  addedDate < '%s'  ORDER BY addedDate"%(date_from,date_to)
cursor.execute(sql)
result=cursor.fetchall()
worksheet2.write('B23',int(result[0][0]),format1)
sql = "SELECT COUNT(*) FROM zt_doc WHERE  module = '748' and deleted= '0'  and product in ('10','12','13','19','26','27','33','30','31','32') and addedDate >'%s' and  addedDate < '%s'  ORDER BY addedDate"%(date_from,date_to)
cursor.execute(sql)
result=cursor.fetchall()
worksheet2.write('C23',int(result[0][0]),format1)
#定制
sql = "SELECT COUNT(*) FROM zt_doc WHERE  module = '749' and deleted= '0'  and product ='16' and addedDate >'%s' and  addedDate < '%s'  ORDER BY addedDate"%(date_from,date_to)
cursor.execute(sql)
result=cursor.fetchall()
worksheet2.write('B24',int(result[0][0]),format1)
sql = "SELECT COUNT(*) FROM zt_doc WHERE  module = '748' and deleted= '0'  and product ='16' and addedDate >'%s' and  addedDate < '%s'  ORDER BY addedDate"%(date_from,date_to)
cursor.execute(sql)
result=cursor.fetchall()
worksheet2.write('C24',int(result[0][0]),format1)
#插入表格
chart3=workbook.add_chart({'type':'column'})
chart3.add_series({
    'name':u'标准版本',
    'categories':'=productdetail!$A$21:$A$24',
    'values':'=productdetail!$B$21:$B$24',
    'fill': {'color':'#AB82FF'},
})
chart3.add_series({
    'name':u'替换文件',
    'categories':'=productdetail!$A$21:$A$24',
    'values':'=productdetail!$C$21:$C$24',
    'fill': {'color':'#9AFF9A'},
})
chart3.set_x_axis({
    'name':u'所属产品线',
    'name_font':{'size':12},
})
chart3.set_y_axis({
    'name':u'上线次数',
    'name_font':{'size':12,'bold':True},
    'num_font':{'italic':True},
})
chart3.set_title({'name': u'产品线上线类型对比'})
chart3.set_style(3)
worksheet2.insert_chart('E20',chart3)

db.close()
workbook.close()
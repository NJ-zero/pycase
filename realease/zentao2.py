#coding=utf-8
#author='Shichao-Dong'

import unittest
import xlsxwriter
import time,datetime,calendar
import MySQLdb
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

class zentao(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_1definetime(self):
        global d,date_from,date_to,worksheet,worksheet2,format_center,format1,format2,format3,workbook,cursor,db
        d=datetime.date.today()
        #本周
        weekday=d.isoweekday()
        before=weekday-1
        dayfrom=d - datetime.timedelta(days=before)
        sixdays = datetime.timedelta(days=6)
        dayto = dayfrom + sixdays
        self.date_from = datetime.datetime(dayfrom.year, dayfrom.month, dayfrom.day, 0, 0, 0)
        self.date_to = datetime.datetime(dayto.year, dayto.month, dayto.day, 23, 59, 59)


    def test_2addworkbook(self):
        filename='D:/Ptest/zentao/Report/'+str(d)+'-report.xlsx'
        self.workbook = xlsxwriter.Workbook(filename)
        self.worksheet = workbook.add_worksheet('weeklysummary')
        self.worksheet2 = workbook.add_worksheet('productdetail')
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

    def test_3writeversion(self):
        db=MySQLdb.connect('172.31.3.110','dsc','123456','zentao')
        cursor = db.cursor()
        cursor.execute('SET NAMES UTF8')
        #查询上线类型次数 749：标准版本 748：替换文件
        date_from=self.date_from
        date_to=self.date_to
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
        #插入图表
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

    def test_4writedetail(self):
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
            result55=str(result[5])
            title.append(result55)
        row4=len(title)
        for i in range(row4):
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




    def test_9end(self):
        db.close()
        workbook.close()

if __name__=="__main__":
    unittest.main()
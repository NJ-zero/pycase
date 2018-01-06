#coding=utf-8
#author='Shichao-Dong'

'''
统计jira数据
'''


from jira import JIRA
import re
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def issue_search():
    jira = JIRA('http://172.31.3.252',basic_auth=('dongshichao','waiqin123'))
    issues = jira.search_issues('project = "TEST" and created >= "-10d"',maxResults=10,fields='summary,description,comment')
    return issues

#print issue summary
def get_issue():
    for issue in issue_search():
        issue =  str(issue) + issue.fields.summary.encode('utf-8')
        print issue
    return issue

#print build
def get_comment():
    for issue in issue_search():
        comments = issue.raw['fields']['comment']['comments']
        i = 0
        while i < len(comments):
            comment = comments[i]['body'].encode('utf-8')
            pattern = re.search(r"http://172.31.3.252:8082(.*?)gz",comment)
            if pattern != None:
                print pattern.group()
            i = i+1
    return comments

#print summary and comment
def get_issueandcomment():
    for issue in issue_search():
        issue_get =  str(issue) + issue.fields.summary.encode('utf-8')
        print issue_get
        comments = issue.raw['fields']['comment']['comments']
        i = 0
        while i < len(comments):
            comment = comments[i]['body'].encode('utf-8')
            pattern = re.search(r"http://172.31.3.252:8082(.*?)gz",comment)
            if pattern != None:
                print pattern.group()
            i = i+1

#write data
def write(filename):
    workbook = xlsxwriter.Workbook(filename)
    worksheet_test = workbook.add_worksheet('Test')
    worksheet_build = workbook.add_worksheet('build_count')
    format1 = workbook.add_format({'bold':True,'align':'left','valign':'vcenter','border':1})
    worksheet_test.set_column("A:A",100)
    worksheet_build.set_column("A:A",120)
    #read and write summary
    issues = issue_search()
    for i in range(len(issues)):
        issue_write = str(str(issues[i]).encode('utf-8') + issues[i].fields.summary.encode('utf-8'))
        print issue_write
        worksheet_test.write_string(i,0,issue_write,format1)

    #read and write build
    sum = 0
    for i in range(len(issues)):
        for issue in issues:
            comments = issue.raw['fields']['comment']['comments']
            des = issue.fields.description
            print issue
            print des
            for n in range(len(comments)):
                sum = 1 + sum
                comment = comments[n]['body'].encode('utf-8')
                pattern = re.search(r"http://172.31.3.252:8082(.*?)gz",comment)

                if pattern != None:
                    print pattern.group()
                    worksheet_build.write(sum-1,0,pattern.group(),format1)
                else:
                    sum = sum-1


    workbook.close()
    return workbook

if __name__ == "__main__":
    # write('D:/file/build.xlsx')
    get_issue()

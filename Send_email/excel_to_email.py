#_*_ coding:utf-8_*_
import os,sys
import xlwt
import smtplib  
from email.mime.multipart import MIMEMultipart  
from email.mime.text import MIMEText

#image包可以发送图片形式的附件  
# from email.mime.image import MIMEImage  
  
# 可以查询文件对应的'Content-Type'  
# import mimetypes  
# mimetypes.guess_type('c:\\users\\adminstrator\\desktop\\ceshi.xls')

def sendmail(excel_name):     
    asender = 'xxxx@qq.com'  
    #多个收件人用逗号隔开  
    areceiver = 'xxxx@qq.com, xxxx@qq.com；'  
    acc = 'xxxx@qq.com, xxxx@qq.com'
    asubject = u'邮件主题'
  
    #smtp服务器  
    asmtpserver = 'smtp.exmail.qq.com'
    ausername = 'xxxx@qq.com'
    apassword = '*******'

    #下面的to\cc\from最好写上，不然只在sendmail中，可以发送成功，但看不到发件人、收件人信息  
    msgroot = MIMEMultipart('related')  
    msgroot['Subject'] = asubject  
    msgroot['to'] = areceiver  
    msgroot['Cc'] = acc  
    msgroot['from'] = asender  
  
    # MIMEText有三个参数，第一个对应文本内容，第二个对应文本的格式，第三个对应文本编码  
    thebody = MIMEText(u'Please check the attachment, thanks!', 'plain', 'utf-8')  
    msgroot.attach(thebody)  
  
    # 读取xls文件作为附件，open()要带参数'rb'，使文件变成二进制格式,从而使'base64'编码产生作用，否则附件打开乱码  
    att = MIMEText(open(excel_name, 'rb').read(), 'base64', 'GB2312')  
    att['Content-Type'] = 'application/vnd.ms-excel'
    att['Content-Disposition'] = 'attachment; filename ='+excel_name.replace("excel/","")

    # 读取xlsx文件作为附件，open()要带参数'rb'，使文件变成二进制格式,从而使'base64'编码产生作用，否则附件打开乱码  
    #att = MIMEText(open(u'C:\\ceshi.xlsx', 'rb').read(), 'base64', 'utf-8')  
    #att['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'  
    #下面的filename 等号(=)后面好像不能有空格  
    #attname ='attachment; filename ="123.xlsx"'  
    #att['Content-Disposition'] = attname

    msgroot.attach(att)   
    asmtp = smtplib.SMTP()  
    asmtp.connect(asmtpserver)  
    asmtp.login(ausername, apassword)

    #发送给多人时，收件人应该以列表形式，areceiver.split把上面的字符串转换成列表  
    #只要在sendmail中写好发件人、收件人，就可以发送成功  
    # asmtp.sendmail(asender, areceiver.split(','), msgroot.as_string())  
  
    #发送给多人、同时抄送给多人，发送人和抄送人放在同一个列表中  
    asmtp.sendmail(asender, areceiver.split(',') + acc.split(','), msgroot.as_string())  
    asmtp.quit()  

files = os.listdir('/root/check_log/')
os.chdir('/root/check_log')
for f in files:
    if os.path.splitext(f)[1] == '.log':
        if os.path.getsize(f)!=0:
            #新建表格
            workbook = xlwt.Workbook()
            sheet1 = workbook.add_sheet('sheet1', cell_overwrite_ok=True)
            style = xlwt.easyxf('align: wrap on, vert centre, horiz centre;borders:top thin, bottom thin, left thin,right thin')  # 自动换行、居中、边框
            style1 = xlwt.easyxf( 'pattern: pattern solid, fore_color gray25;align: wrap on, vert centre, horiz centre;font:bold on;borders:left double, right double')  # 添加灰色固体

            #写入首行列名
            sheet1.write(0, 0, '告警时间'.decode('gb2312'), style1)
            sheet1.write(0, 1, '客户名称'.decode('gb2312'), style1)
            sheet1.write(0, 2, '攻击源IP'.decode('gb2312'), style1)
            sheet1.write(0, 3, '攻击目的IP'.decode('gb2312'), style1)
            sheet1.write(0, 4, '攻击流量（bytes）'.decode('gb2312'), style1)
            sheet1.write(0, 5, '攻击开始时间'.decode('gb2312'), style1)
            row = 1

            f_open = open(f,'r')
            lines = f_open.readlines()[1:]
            for line in lines:
                line = line.decode('gb2312')
                line_list = line.split(' ')
                alarm_time = line_list[0]
                start_time = line_list[1]
                ObjectName = line_list[2]
                s_ip = line_list[3]
                d_ip = line_list[4]
                Attack_Traffic = line_list[5]

                sheet1.write(row, 0, alarm_time, style)
                sheet1.write(row, 1, ObjectName, style)
                sheet1.write(row, 2, s_ip, style)
                sheet1.write(row, 3, d_ip, style)
                sheet1.write(row, 4, Attack_Traffic, style)
                sheet1.write(row, 5, start_time, style)
                row = row+1
            f_open.close()

            #判断该log的表格是否已存在
            excel_name = 'excel/结果表_201710'+f.replace('.log','')+'.xls'
            if os.path.exists(excel_name)==True:
                continue
            else:
                # 保存该excel文件
                workbook.save(excel_name)
                print('send new email')
                sendmail(excel_name)
        else:
            pass
print("It is done")

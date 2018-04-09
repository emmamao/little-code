#_*_ coding:utf-8_*_
from IPy import IP
import xlrd,xlwt
from xlutils.copy import copy

# 向sheet页中写入数据，copy模版样式
oldWb = xlrd.open_workbook('input.xls',formatting_info=True)
wb = copy(oldWb)
oldsheet = oldWb.sheets()[0]
sheet1 = wb.get_sheet(0)
nrows = oldsheet.nrows
for i in range(1, nrows):
    ip_net = oldsheet.cell_value(i, 0)
    try:
        ip = IP(ip_net)
    except:
        continue
    ips = ''
    for x in ip:
        ips = ips+str(x)+'\n'
    sheet1.write(i, 1, ips.strip())
wb.save('output.xls')
print("It is done!")

'''ip = IP('36.111.89.0/24')
f = open('1','w')
for x in ip:
    #print(x)
    f.write(str(x)+'\n')
print('over')'''

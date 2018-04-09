# -*- coding: utf-8 -*-
import requests
import json
import xlwt
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def get_info(keyword,count,cookies,token):
    s = requests.session()
    header = {
        'Cookie': cookies,
        'origin': 'http://find.qq.com/',
        'user-agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.8',
        'accept-encoding': 'gzip, deflate',
        'referer': 'http://find.qq.com/',
        'connection': 'keep-alive',
        'host': 'qun.qq.com',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    total_sum =0
    page = 0
    result = []
    while total_sum< count:
        data = {'k': '交友', 'n': 8, 'st': 1, 'iso': '1', 'src': 1, 'v': 4903, 'bkn': token, 'isRecommend': 'false',
                 'city_id': 0, 'from': 1, 'keyword': keyword, 'sort': 0, 'wantnum': 24, 'page': page,
                 'ldw': token}  # 'newSearch': 'true',
        agentlist = s.post('http://qun.qq.com/cgi-bin/group_search/pc_group_search', data=data, headers=header)
        agent_offline_json = json.loads(agentlist.text)
        try:
            total_list = agent_offline_json['group_list']
            for item in total_list:
                code = item['code']
                name = item['name']
                member_num = item['member_num']
                memo = item['richfingermemo']
                owner_uin = item['owner_uin']
                temp_qaddr = item['qaddr']
                qaddr = ''.join(temp_qaddr)
                result.append((name, code, member_num, memo, qaddr, owner_uin))
                total_sum = total_sum + 1
                if total_sum >= count:
                    break
            page = page + 1
        except Exception as e:
            print(e)
            return result
    return result

def output_excel(keyword,count,result):
    # 新建表格
    workbook = xlwt.Workbook()
    sheet1 = workbook.add_sheet('sheet1', cell_overwrite_ok=True)
    style = xlwt.easyxf('align: wrap on, vert centre, horiz centre;borders:top thin, bottom thin, left thin,right thin')  # 自动换行、居中、边框
    style1 = xlwt.easyxf('pattern: pattern solid, fore_color gray25;align: wrap on, vert centre, horiz centre;font:bold on;borders:left double, right double')  # 添加灰色固体
    # 设定固定列宽
    col_1 = sheet1.col(0)
    col_2 = sheet1.col(1)
    col_3 = sheet1.col(2)
    col_4 = sheet1.col(3)
    col_5 = sheet1.col(4)
    col_6 = sheet1.col(5)
    col_1.width = col_2.width = col_3.width = col_4.width = col_5.width = col_6.width = 256 * 24

    # 写入首行列名
    # 如果在linux上运行，需添加.decode('utf-8')
    sheet1.write(0, 0, '查询关键字', style1)
    sheet1.write(0, 2, '查询个数', style1)
    sheet1.write(1, 0, '群名', style1)
    sheet1.write(1, 1, '群号', style1)
    sheet1.write(1, 2, '群人数', style1)
    sheet1.write(1, 3, '群介绍', style1)
    sheet1.write(1, 4, '城市', style1)
    sheet1.write(1, 5, '群主号', style1)
    sheet1.write(0, 1, keyword, style)
    sheet1.write(0, 3, count, style)
    row = 2
    for dict in result:
        sheet1.write(row, 0, dict[0], style)
        sheet1.write(row, 1, dict[1], style)
        sheet1.write(row, 2, dict[2], style)
        sheet1.write(row, 3, dict[3], style)
        sheet1.write(row, 4, dict[4], style)
        sheet1.write(row, 5, dict[5], style)
        row = row + 1
    excel_name = 'QQ群查找_' + keyword + '.xls'
    workbook.save(excel_name)

if __name__ == "__main__":
    print('QQ自动登录暂未实现，请在www.qq.com已登录的情况下，访问 http://find.qq.com，任意查询某关键字，F12--Network--F5,点击pc_group_search的请求，复制requests header里的cookies，复制Form data里的bkn!')
    # 手工登录信息
    #token = int(input('请输入复制的bkn:'))
    #cookies = input('请输入复制的cookies:')
    #count = int(input('查询个数:'))
    #keyword = input('查询关键字:')
    #读取参数文件
    lines = open('参数.txt','r').readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].split('：')[1].replace('\n','')
    token = int(lines[1])
    cookies = str(lines[2])
    count = int(lines[3])
    keyword = lines[4]
    print('开始查询')
    try:
        #提取信息（群号码，群名，人数，建群时间，群说明，群主号码，管理员）
        result = get_info(keyword, count, cookies, token)
        output_excel(keyword,count,result)
        print('完成')
    except Exception as e:
        print('程序异常中止，请注意登录信息cookies是否过期')
        print(e)
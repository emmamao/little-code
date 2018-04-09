#_*_ coding:utf-8_*_
import re,requests
import time
from lxml import etree

keyword = '关键字'
#keyword = str(input('输入查询关键字：'))

#result=[]
header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'accept-language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'accept-encoding': 'gzip, deflate, sdch, br',
        'referer': 'https://www.oschina.net/search?q=%E5%AE%89%E5%85%A8',
        'connection': 'keep-alive',
        'content-type': 'application/x-www-form-urlencoded'
    }
f=open('result.txt','w')
for i in range(1,105):
    url='https://www.oschina.net/search?scope=project&q='+keyword+'&p='+str(i)
    try:
        html = requests.get(url,headers=header)
    except:
        print('第 %s 页需要sleep'%str(i))
        time.sleep(6)
        html = requests.get(url,headers=header)
    content = (html.content).decode('utf-8','ignore')
    tool_url =  etree.HTML(content).xpath('//ul[@id="results"]//li[@class="obj_type_1"]//h3//a/@href')
    title = []
    tree = etree.HTML(content)
    property_list_reg = '//ul[@id="results"]//li[@class="obj_type_1"]//h3//a'
    property_lst = tree.xpath(property_list_reg)
    for e in property_lst:
        title.append(e.xpath('string(.)'))
    if len(title)!=len(tool_url):
        print('第 %s 页出现问题'%str(i))
        continue
    for j in range(0,len(title)):
        try:
            f.write(title[j]+';;;'+tool_url[j]+'\n')
        except:
            print(title[j])
            f.write(';;;'+tool_url[j]+'\n')
        f.flush()
    if i % 10 ==0:
        #print('normal')
        time.sleep(3)
f.close()
print('OVER')


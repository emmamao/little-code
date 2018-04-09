# -*- coding: utf-8 -*-
import requests
import re
from requests import Request, Session

input_file = open('input.txt','r')
line = input_file.readlines()
input_file.close()

for i in line:
    i = i.replace('\n','')
    s=requests.Session()
    try:
        response= requests.get(i, verify=False,timeout=1)
        print(response.status_code)
        content = response.text
            
        if re.search('title',content)!=None:
            title = re.findall(r'<title>(.*?)</title>',content,re.S)[0]
        else:
            title = content.replace('\n','')
        print(response.status_code,title)
    except:
        http_code = '0'
        title = ''
        print('eeee')
        continue        

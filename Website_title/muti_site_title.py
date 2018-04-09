# -*- coding: utf-8 -*-
import requests
from requests import Request, Session
import threading
import time,re
import warnings
warnings.filterwarnings('ignore')

start = time.clock()

thread_count = input('输入线程数(默认5)：')
if thread_count == '':
    thread_count = 5
else:
    thread_count = int(thread_count)
input_file = open('input.txt','r')
line = input_file.readlines()
one_part = len(line)//thread_count
input_file.close()
output_file = open('output.txt','w')
f = open('temp_exception.txt','w')
    
def check_https(line_part):
    for i in line_part:
        i = i.replace('\n','')
        s=requests.Session()
        try:
            response= s.get(i, verify=False,timeout=60)
            http_code = str(response.status_code)
            content = response.text
            if re.search('title',content,re.IGNORECASE)!=None:
                title = re.findall(r'<title>(.*?)</title>',content,re.S)[0]
            else:
                if response.status_code==200 or response.status_code==302:
                    title = 'index'
                else:
                    title = content.replace('\n','')
                
            #if response.status_code==200 or response.status_code==302:
            #    content = 'index'
            #else:
            #    content = response.text
            #    content = content.replace('\n','')
            print(http_code,title)
        except:
            http_code = '0'
            title = ''
            f.write(i+'\n')
        output_file.write(i+'|'+http_code+'|'+title+'\n')

threads =[]
for j in range(thread_count):
    s_num = one_part*j
    e_num = s_num + one_part
    if j != thread_count:
        line_part = line[s_num:e_num]
    else:
        line_part = line[s_num:]
    try:
        thread = threading.Thread(target=check_https,args=(line_part,))
        thread.start()
        threads.append(thread)
    except Exception as e:
        print('write output.txt fail,',str(e))

for t in threads:
    t.join()
    
output_file.flush()
output_file.close()
f.flush()
f.close()
end = time.clock()
print("over time: %f s" % (end - start))

    

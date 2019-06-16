# -*- coding: UTF-8 -*-
from urllib.parse import urljoin,urlencode
from bs4 import BeautifulSoup as bsp
import random
from urllib import request, parse
import re
import random
import pandas as pd
import numpy as np
import os
import threading
import requests
import datetime

total_request_num = 0
fialed_num = 0
root = 'E:\\大三下\\移动互联网\\project\\pictures'
repeatLimit = 500

f = open('ip_origin.txt','r')
iplist = f.readlines()
lenOfIP = len(iplist)
for i in range(lenOfIP):
    iplist[i] = iplist[i][:-1]
f.close()

dataset = np.load('author_list.npy')
author_list = pd.read_csv('author_list.csv', header=0, index_col=None)
author_list = author_list.values

def get_proxy():
    ip = random.choice(iplist)
    proxy = {"http": "http://"+ip, "https": "http://"+ip}
    return request.ProxyHandler(proxy)

def getheaders():
    user_agent_list = [ \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
    UserAgent=random.choice(user_agent_list)
    headers = {'User-Agent': UserAgent}
    return headers

'''
def webopen(url):
    global total_request_num
    total_request_num += 1
    repeat = 0
    while(True):
        try:
            #print(repeat)
            proxy = get_proxy()
            opener = request.build_opener(proxy)
            request.install_opener(opener)
            response = opener.open(url, timeout= 3)
            return response.read(), response.geturl()
        except:
            repeat += 1
            if (repeat >= repeatLimit):
                print(url, 'connection failed')
                return None,None
            continue
'''

def webopen(url):
    global total_request_num, fialed_num
    total_request_num += 1
    try:
        headers = getheaders()
        req = request.Request(url=url, headers=headers)
        response = request.urlopen(req, timeout= 5)
        return response.read(), response.geturl()
    except:
        fialed_num += 1
        return None, None

def savePic(imgurl, index, imgname):
    name = author_list[index, 0]
    inst = author_list[index, 1]
    picdir = os.path.join(root, 'No.'+str(index)+'_'+name+'_'+inst)
    if (not os.path.exists(picdir)):
        os.mkdir(picdir)
    img, url = webopen(imgurl)
    if (img == None):
        print('save picture index--',index ,imgname,'failed')
        return
    f = open(os.path.join(picdir, imgname+'.png'),'wb')
    f.write(img)
    f.flush()
    f.close()
    print('save picture index--',index ,imgname,'success')

def getPicFromHomepage(index):
    url = dataset[index, 2]
    page, url = webopen(url)
    if (page == None):
        return
    soup = bsp(page,features="lxml")
    tags = soup.find_all('img')
    for i in range(len(tags)):
        try:
            imgurl = urljoin(url,tags[i]['src'])
            savePic(imgurl, index, 'homepage'+'_'+str(i))
        except:
            continue

def getPicFromBaidu(index):
    url = 'https://www.baidu.com/s?tn=80035161_2_dg&wd=' + dataset[index, 0] + '+' + dataset[index, 1]
    page, url = webopen(url)
    if (page == None):
        return
    soup = bsp(page,features="lxml")
    tags = soup.find_all('h3', attrs={'class':'t'})
    '''
    subthreads = []
    for i in range(len(tags)):
        link = tags[i].a['href']
        t = threading.Thread(target=getPicFromLink, args=(link, index, i))
        subthreads.append(t)
        #getPicFromLink(link, index, i)
    for s in subthreads: # 开启多线程爬取
        s.start()
    for e in subthreads: # 等待所有线程结束
        e.join()
    '''
    for i in range(len(tags)):
        link = tags[i].a['href']
        getPicFromLink(link, index, i)

def getPicFromBeing(index):
    dict = {'q' : author_list[index, 0] + ' ' + author_list[index, 1]}
    url = 'https://m2.cn.bing.com/search?' + urlencode(dict) +'&FORM=BESBTB&ensearch=1'
    #url = 'https://m2.cn.bing.com/search?q=' + dataset[index, 0] + '+' + dataset[index, 1] + '&FORM=BESBTB&ensearch=1'
    page, url = webopen(url)
    if (page == None):
        return
    soup = bsp(page,features="lxml")
    tags = soup.find_all('li', attrs={'class':'b_algo'})
    '''
    subthreads = []
    for i in range(len(tags)):
        link = tags[i].a['href']
        t = threading.Thread(target=getPicFromLink, args=(link, index, i))
        subthreads.append(t)
        #getPicFromLink(link, index, i)
    for s in subthreads: # 开启多线程爬取
        s.start()
    for e in subthreads: # 等待所有线程结束
        e.join()
    '''
    for i in range(len(tags)):
        link = tags[i].h2.a['href']
        getPicFromLink(link, index, i)

def getPicFromLink(url, index, pagenum):
    page, url = webopen(url)
    if (page == None):
        return
    soup = bsp(page,features="lxml")
    tags = soup.find_all('img')
    for i in range(len(tags)):
        try:
            imgurl = urljoin(url,tags[i]['src'])
            savePic(imgurl, index, 'search'+'_'+str(pagenum)+'_'+str(i))
        except:
            continue

def gettimediff(start,end):
    seconds = (end - start).seconds
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    diff = ("%02d:%02d:%02d" % (h, m, s))
    return diff

def work(start, end):
    for i in range(start, end):
        print('Crawling pictures: name--',author_list[i][0],'institude--', author_list[i][1])
        #print('From Homepage')
        #getPicFromHomepage(i)
        '''
        print('From Baidu')
        getPicFromBaidu(i)
        '''
        print('From Being')
        getPicFromBeing(i)


threadsnum = 100
start = 0
totalnum = 200 #dataset.shape[0]

indexlist = []
for i in range(threadsnum):
    worksPerThread = totalnum//threadsnum
    indexlist.append(start + i*worksPerThread)
indexlist.append(start + totalnum)

start = datetime.datetime.now() # 开始时间
threads=[]
for i in range(threadsnum):
    t=threading.Thread(target=work,args=(indexlist[i], indexlist[i+1]))
    threads.append(t)
for s in threads: # 开启多线程爬取
    s.start()
for e in threads: # 等待所有线程结束
    e.join()
end = datetime.datetime.now() # 结束时间
diff = gettimediff(start, end)  # 计算耗时

print('-----------------------------------------------')
print('共耗时:', diff, 'seconds',  '访问网站数：', total_request_num, '失败访问数：', fialed_num, '占比：', fialed_num/total_request_num)
#print('平均耗时：', (end - start).seconds/total_request_num, 'seconds')
print('爬取速度：', total_request_num*60/diff, 'requests/min')
print('-----------------------------------------------')

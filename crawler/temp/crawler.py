# -*- coding: UTF-8 -*-
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup as bsp
import random
import  urllib.request
import re
import random
import pandas as pd
import numpy as np
import os

root = 'E:\\大三下\\移动互联网\\project\\pictures'
repeatLimit = 100

f = open('ip0.txt','r')
iplist = f.readlines()
lenOfIP = len(iplist)
for i in range(lenOfIP):
    iplist[i] = iplist[i].split('\"')[-2] + '\n'
f.close()

f = open('ip.txt','w')
f.writelines(iplist)
f.close()

'''
f = open('ip.txt','r')
iplist = f.readlines()
lenOfIP = len(iplist)
for i in range(lenOfIP):
    iplist[i] = iplist[i][:-1]
f.close()
'''
'''
dataset = pd.read_csv('author_list.csv', header=0, index_col=None)
dataset = dataset.values
for i in range(dataset.shape[0]):
    dataset[i, 0] = '+'.join(dataset[i, 0].split())
    dataset[i, 1] = '+'.join(dataset[i, 1].split())
np.save('author_list.npy', dataset)
'''
dataset = np.load('author_list.npy')
author_list = pd.read_csv('author_list.csv', header=0, index_col=None)
author_list = author_list.values

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

def get_ip():
    ipindex = random.randint(0, lenOfIP-1)
    return iplist[ipindex]

def savePic(imgurl, index, id, isHome, proxies):
    name = author_list[index, 0]
    inst = author_list[index, 1]
    picdir = os.path.join(root, name+'+'+inst)
    if (not os.path.exists(picdir)):
        os.mkdir(picdir)
    headers =getheaders()  # 定 制请求头
    try:
        img = requests.get(imgurl, proxies=proxies,headers=headers,timeout=1)
    except:
        repeat = 0
        while(True):
            try:
                headers =getheaders()  # 定制请求头
                ip = get_ip()
                proxies = {"http": "http://"+ip, "https": "http://"+ip}  # 代理ip 
                #print('try')
                img = requests.get(imgurl, proxies=proxies,headers=headers,timeout=1)
                print('success')
            except:
                repeat += 1
                if (repeat>=repeatLimit):
                    print('error')
                    return proxies
                continue
            break
    if (isHome):
        x = 'home' + str(id)
    else:
        x = 'baidu' + str(id)
    
    f = open(os.path.join(picdir, '%s.jpg'%x),'ab') #存储图片，多媒体文件需要参数b（二进制文件）
    f.write(img.content) #多媒体存储content
    f.close()
    return proxies

def getPicFromHome(index):
    headers =getheaders()  # 定制请求头
    print(author_list[index, 0])
    url = dataset[index, 2]
    repeat = 0
    while(True):
        try:
            headers =getheaders()  # 定制请求头
            ip = get_ip()
            proxies = {"http": "http://"+ip, "https": "http://"+ip}  # 代理ip
            #print('try')     
            r = requests.get(url, proxies=proxies,headers=headers,timeout=1)
            print('success')
        except:
            repeat += 1
            if (repeat>=repeatLimit):
                print('error')
                return
            continue
        break
    soup = bsp(r.text,"html.parser")#,from_encoding="utf-8"
    tags = soup.find_all('img')
    id = 0
    for tag in tags:
        imgurl = urljoin(url,tag['src'])
        proxies = savePic(imgurl, index, id, 1, proxies)
        id += 1
        print(imgurl)

def getPicFromBaidu(index):
    url = 'https://www.baidu.com/s?tn=80035161_2_dg&wd=' + dataset[index, 0] + '+' + dataset[index, 1]
    repeat = 0
    while(True):
        try:
            headers =getheaders()  # 定制请求头
            ip = get_ip()
            proxies = {"http": "http://"+ip, "https": "http://"+ip}  # 代理ip
            #print('try')     
            r = requests.get(url, proxies=proxies,headers=headers,timeout=1)
            print('success')
        except:
            repeat += 1
            if (repeat>=repeatLimit):
                print('error')
                return
            continue
        break
    soup = bsp(r.text,"html.parser")#,from_encoding="utf-8"
    tags = soup.find_all('h3', attrs={'class':'t'})
    id = 0
    for tag in tags:
        homelink = tag.a['href']
        print(homelink)
        id = getPicFromLink(homelink, index, id)

def getPicFromLink(link, index, id):
    headers =getheaders()  # 定制请求头
    url = link
    repeat = 0
    while(True):
        try:
            headers =getheaders()  # 定制请求头
            ip = get_ip()
            proxies = {"http": "http://"+ip, "https": "http://"+ip}  # 代理ip
            #print('try')     
            r = requests.get(url, proxies=proxies,headers=headers,timeout=1)
            print('success')
        except:
            repeat += 1
            if (repeat>=repeatLimit):
                print('error')
                return id
            continue
        break
    soup = bsp(r.text,"html.parser")#,from_encoding="utf-8"
    tags = soup.find_all('img')
    print(tags)
    for tag in tags:
        imgurl = urljoin(r,tag['src'])
        print('------------------------------')
        print('downloading', id)
        print(tag['src'])
        print(imgurl)
        print('------------------------------')
        proxies = savePic(imgurl, index, id, 0, proxies)
        id += 1
    return id

'''
def get_scholar_links(name):
    headers =getheaders()  # 定制请求头
    ip = get_ip()
    proxies = {"http": "http://"+ip, "https": "http://"+ip}  # 代理ip
    url = 'https://scholar.google.com.hk/citations?hl=en&view_op=search_authors&mauthors=' + name + '&btnG='
    r = requests.get(url, proxies=proxies,headers=headers,timeout=5)
    soup = bsp(r.text,"html.parser",from_encoding="utf-8")
    links = soup.find_all('h3',attrs={'class':'gs_ai_name'})
    shomelinks = []
    for link in links:
        #print (link.name,link['href'], link.get_text())
        shomelinks.append(urljoin(url,link.a['href']))
        print(urljoin(url,link.a['href']))

    nexturltag = soup.find('button', attrs={'aria-label':'Next'})
    matchObj = re.match( r'window.location=\'(.*)\'', nexturltag['onclick'])
    print(urljoin(url, matchObj.group(1)))
    return shomelinks

def get_pictures(link, name, id):
    headers =getheaders()  # 定制请求头
    ip = get_ip()
    proxies = {"http": "http://"+ip, "https": "http://"+ip}  # 代理ip
    r = requests.get(link, proxies=proxies,headers=headers,timeout=5)
    soup = bsp(r.text,"html.parser",from_encoding="utf-8")
    tag = soup.find('div',attrs={'id':'gsc_prf_pua', 'class':'gs_rimg'})
    imgurl = urljoin(link, tag.img['src'])
    x = name + '+' + str(id)
    urllib.request.urlretrieve(imgurl,'%s.jpg' % x)
'''


'''
for i in range(dataset.shape[0]):
    getPicFromHome(i)
'''
#getPicFromBaidu(1)

'''
name = 'Bo+Yuan'
links = get_scholar_links(name)
for i in range(len(links)):
    get_pictures(links[i], name, i)'''


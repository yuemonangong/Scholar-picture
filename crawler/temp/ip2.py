#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests,threading,datetime
from bs4 import BeautifulSoup
import random

"""
1、抓取西刺代理网站的代理ip
2、并根据指定的目标url,对抓取到ip的有效性进行验证
3、最后存到指定的path
"""

# ------------------------------------------------------文档处理--------------------------------------------------------
# 写入文档
def write(path,text):
    with open(path,'a', encoding='utf-8') as f:
        f.writelines(text)
        f.write('\n')
# 清空文档
def truncatefile(path):
    with open(path, 'w', encoding='utf-8') as f:
        f.truncate()
# 读取文档
def read(path):
    with open(path, 'r', encoding='utf-8') as f:
        txt = []
        for s in f.readlines():
            txt.append(s.strip())
    return txt
# ----------------------------------------------------------------------------------------------------------------------
# 计算时间差,格式: 时分秒
def gettimediff(start,end):
    seconds = (end - start).seconds
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    diff = ("%02d:%02d:%02d" % (h, m, s))
    return diff
# ----------------------------------------------------------------------------------------------------------------------
# 返回一个随机的请求头 headers
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
# -----------------------------------------------------检查ip是否可用----------------------------------------------------
def checkip(targeturl,ip):
    headers =getheaders()  # 定制请求头
    proxies = {"http": "http://"+ip, "https": "http://"+ip}  # 代理ip
    try:
        response=requests.get(url=targeturl,proxies=proxies,headers=headers,timeout=5).status_code
        if response == 200 :
            return True
        else:
            return False
    except:
        return False

#-------------------------------------------------------获取代理方法----------------------------------------------------
# 免费代理 XiciDaili
def findip(iplist, start, end, targeturl, path): # ip类型,页码,目标url,存放ip的路径
    for i in range(start, end):
        ip = iplist[i]
        is_avail = checkip(targeturl,ip)
        print(ip,'checking')
        if is_avail == True:
            write(path=path,text=ip)
            print(ip, 'success')
        else:
            print(ip, 'fail')

#-----------------------------------------------------多线程抓取ip入口---------------------------------------------------
def getip(iplist, targeturl,path):
    truncatefile(path) # 爬取前清空文档
    start = datetime.datetime.now() # 开始时间
    threads=[]
    indexes = []
    for i in range(200):
        indexes.append(i*18)
    for i in range(199):
            t=threading.Thread(target=findip,args=(iplist, indexes[i], indexes[i+1], targeturl, path))
            #t=threading.Thread(target=findip,args=(4,pagenum+1,targeturl,path))
            threads.append(t)
    print('开始爬取代理ip')
    for s in threads: # 开启多线程爬取
        s.start()
    for e in threads: # 等待所有线程结束
        e.join()
    print('爬取完成')
    end = datetime.datetime.now() # 结束时间
    diff = gettimediff(start, end)  # 计算耗时
    ips = read(path)  # 读取爬到的ip数量
    print('一共爬取代理ip: %s 个,共耗时: %s \n' % (len(ips), diff))

#-------------------------------------------------------启动-----------------------------------------------------------
if __name__ == '__main__':
    f = open('ip0.txt','r')
    iplist = f.readlines()
    lenOfIP = len(iplist)
    for i in range(lenOfIP):
        iplist[i] = iplist[i].split('//')[-1][:-2]
    f.close()
    path = 'ip.txt' # 存放爬取ip的文档path
    targeturl = 'https://www.baidu.com/' # 验证ip有效性的指定urlhttps://scholar.google.com.hk/scholar?hl=zh-CN&as_sdt=0%2C5&q=XinbingWang&btnG=
    getip(iplist, targeturl,path)
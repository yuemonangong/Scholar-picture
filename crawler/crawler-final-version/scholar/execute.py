# coding=utf-8
from scrapy import cmdline
import os
import sys
import datetime

if __name__ == '__main__':
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    batchsize = 5
    startbatch = 0
    endbatch = 200
    for i in range(startbatch, endbatch):
        start = datetime.datetime.now() # 开始时间
        command = 'scrapy crawl baidu -a start_id='+str(i*batchsize)+' -a end_id='+str(i*batchsize+batchsize)
        print('-----------------------------------------------------')
        print(command)
        print('-----------------------------------------------------')
        #cmdline.execute(command.split())
        os.system(command)
        end = datetime.datetime.now() # 结束时间
        seconds = (end - start).seconds
        print('-----------------------------------------------------')
        print(seconds, 'seconds')
        print('-----------------------------------------------------')
    # cmdline.execute('scrapy crawl Spider2 -o items.csv -t csv'.split())

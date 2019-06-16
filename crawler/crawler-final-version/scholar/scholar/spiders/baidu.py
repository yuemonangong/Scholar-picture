# -*- coding: utf-8 -*-
import scrapy
import numpy as np
import pandas as pd
import os
from urllib.parse import urljoin, urlencode
from scholar.items import ScholarItem

class ScholarBaiduSpider(scrapy.Spider):
    name = "baidu"
    root = "E:\\code\\scholar_picture"
    def __init__(self, start_id=None,  end_id= None, *args, **kwargs):
        self.start_urls = []
        self.url_index = {}
        #self.dataset = np.load('author_list.npy')
        self.author_list = pd.read_csv('author_ground_truth.csv', header=0, index_col=None)
        self.author_list = self.author_list.values
        self.start_id = int(start_id)
        self.end_id = int(end_id)
        self.count = self.end_id - self.start_id
        for i in range(self.start_id, self.end_id):#dataset.shape[0]
            #start_urls.append(dataset[i][2]+'?scholar_id=%d'%i)
            dict = {'wd' : self.author_list[i, 0] + ' ' + self.author_list[i, 2]}#2->1
            url = 'http://www.baidu.com/s?tn=80035161_2_dg&' + urlencode(dict)
            print(url)
            self.start_urls.append(url)

    def start_requests(self):
        for i in range(len(self.start_urls)):
            yield scrapy.Request(url = self.start_urls[i], meta = {'scholar_id': self.start_id+i}, callback = self.parse)

    def parse(self, response):
        scholar_id = response.meta['scholar_id']
        webid = -1
        
        for tag in response.xpath('//h3[@class="t"]'):
            try:
                nexturl = tag.xpath('a/@href').extract()[0]
                webid += 1
                yield scrapy.Request(url = nexturl, meta= {'scholar_id': scholar_id, 'web_id': webid}, callback=self.parseLink)
            except:
                continue

        for tag in response.xpath('//h3[@class="t c-title-en"]'):
            try:
                nexturl = tag.xpath('a/@href').extract()[0]
                webid += 1
                yield scrapy.Request(url = nexturl, meta= {'scholar_id': scholar_id, 'web_id': webid}, callback=self.parseLink)
            except:
                continue

    def parseLink(self, response):
        scholar_id = response.meta['scholar_id']
        web_id = response.meta['web_id']
        imgid = 0
        for tag in response.xpath('//img'):
            try:
                imgurl = urljoin(response.url, tag.xpath('@src').extract()[0])
                dicname = 'No.' + str(scholar_id) + '_' + self.author_list[scholar_id][1] + '_' + self.author_list[scholar_id][3]
                filename = str(web_id)+'_'+str(imgid) + '.jpg'
                path = os.path.join(self.root, dicname)
                imgid += 1

                item = ScholarItem()
                item['img_path'] = path = os.path.join(path, 'baidu')
                item['img_name'] = filename
                item['img_url'] = imgurl
                yield item
            except:
                continue
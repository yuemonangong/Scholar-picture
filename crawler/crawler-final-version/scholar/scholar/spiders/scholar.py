# -*- coding: utf-8 -*-
import scrapy
import numpy as np
import pandas as pd
import os
from urllib.parse import urljoin
from scholar.items import ScholarItem

class ScholarSpider(scrapy.Spider):
    name = "scholar"
    root = "E:\\code\\scholar_picture"
    def __init__(self, start_id=None, end_id=None, *args, **kwargs):
        self.start_urls = []
        self.url_index = {}
        self.dataset = np.load('author_list.npy')
        self.author_list = pd.read_csv('author_list.csv', header=0, index_col=None)
        self.author_list = self.author_list.values
        self.start_id = int(start_id)
        self.end_id = int(end_id)
        self.count = self.end_id - self.start_id
        for i in range(self.start_id, self.end_id): #dataset.shape[0]
            #start_urls.append(dataset[i][2]+'?scholar_id=%d'%i)
            if (self.dataset[i][2][:4] != 'http'):
                self.dataset[i][2] = 'https://' + self.dataset[i][2]
            self.start_urls.append(self.dataset[i][2])

    def start_requests(self):
        for i in range(len(self.start_urls)):
            yield scrapy.Request(url = self.start_urls[i], meta = {'scholar_id': i+self.start_id}, callback = self.parse)

    def parse(self, response):
        scholar_id = response.meta['scholar_id']
        self.count -= 1
        print('-----------------------')
        print(self.count)
        print('-----------------------')
        imgid = 0
        for tag in response.xpath('//img'):
            imgurl = urljoin(response.url, tag.xpath('@src').extract()[0])
            dicname = 'No.' + str(scholar_id) + '_' + self.author_list[scholar_id][0] + '_' + self.author_list[scholar_id][1]
            filename = str(imgid) + '.jpg'
            path = os.path.join(self.root, dicname)
            imgid += 1

            item = ScholarItem()
            item['img_path'] = path = os.path.join(path, 'homepage')
            item['img_name'] = filename
            item['img_url'] = imgurl
            #print('img_path', item['img_path'])
            #print('img_name', item['img_name'])
            #print('img_url', item['img_url'])
            yield item
    

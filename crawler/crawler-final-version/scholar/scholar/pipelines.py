# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.utils.project import get_project_settings
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request
import os
import shutil
from scrapy.exceptions import IgnoreRequest

class ScholarPipeline(object):
    def process_item(self, item, spider):
        return item

class ImgDownloadPipeline(ImagesPipeline):
    img_store = get_project_settings().get('IMAGES_STORE')

    def get_media_requests(self, item, info):
        yield Request(item['img_url'])

    def item_completed(self, results, item, info):
        try:
            image_path = [x['path'] for ok, x in results if ok]
            img_path = item['img_path']
            if os.path.exists(img_path) == False:
                os.makedirs(img_path)
            if not image_path:
                raise DropItem('Item contains no images')
                #return item
            print('moving', item['img_name'])
            shutil.move(os.path.join(self.img_store, image_path[0]), os.path.join(img_path,item["img_name"]))
            return item
        except:
            return item
 
    def _handle_error(self, failue, item, spider):
        print('-------------------')
        print(failue)
        raise IgnoreRequest
        
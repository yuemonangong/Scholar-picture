# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ScholarItem(scrapy.Item):
    img_path = scrapy.Field()
    img_name = scrapy.Field()
    img_url = scrapy.Field()
    pass

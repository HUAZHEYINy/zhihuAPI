# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuapiItem(scrapy.Item):
    # define the fields for your item here like:
    # question url
    # question name
    question_name = scrapy.Field()
    question_url = scrapy.Field()

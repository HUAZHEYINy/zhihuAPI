# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuapiItem(scrapy.Item):
    #question name
    #question url
    #question answer for current question under the topic
    #question answer author who answer the current question
    #question answer author name
    question_name = scrapy.Field()
    question_url = scrapy.Field()
    question_answer = scrapy.Field()
    question_answer_author_profile = scrapy.Field()
    question_answer_author = scrapy.Field()

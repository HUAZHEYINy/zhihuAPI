# -*- coding: UTF-8 -*-
import scrapy
from scrapy.selector import Selector

class zhihuSpider(scrapy.Spider):
    name = "zhihu"

    def start_requests(self):
        urls = [
            'https://www.zhihu.com/topic/19609455/hot'
        ]
        yield scrapy.Request(url=urls[0], callback=self.parse)

    def parse(self, response):
        print ('hello')
        print (Selector(text=response.body).xpath('/html/head/title/text()').extract_first())


# -*- coding: UTF-8 -*-
import scrapy
from scrapy.selector import Selector
from zhihuAPI.zhihu.items import ZhihuapiItem

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
        question_block_list = response.xpath('/html/body/div[3]/div[1]/div/div/div[4]/div/div')

        # iterate the list of question div block.
        for question_block in question_block_list:
            question_name = question_block.xpath('div/div/h2/a/text()').extract_first()
            question_url = question_block.xpath('div/div/h2/a/@href').extract_first()
            yield ZhihuapiItem(question_name=question_name, question_url=question_url)
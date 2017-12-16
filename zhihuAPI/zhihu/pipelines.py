# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs

class ZhihuapiPipeline(object):
    def open_spider(self, spider):
        self.file = codecs.open('items.json', 'wb', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        print ('I am handleing item: {}'.format(item))
        if item['question_name']:
            item['question_name'] = item['question_name'].strip()
            item['question_url'] = item['question_url'].strip()
            item['question_answer'] = item['question_answer'].strip()
            item['question_answer_author_profile'] = item['question_answer_author_profile'].strip()
            item['question_answer_author'] = item['question_answer_author'].strip()

            line = json.dumps(dict(item)) + "\n"
            self.file.write(line.encode('ascii').decode('unicode-escape'))

            return item

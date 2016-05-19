# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import traceback
from pymongo import MongoClient


class FirstspiderPipeline(object):

    def __init__(self):
        self.port = 30000
        self.host = '172.16.2.243'
        try:
            self.client = MongoClient(self.host, self.port)
        except:
            traceback.print_exc()

    def process_item(self, item, spider):
        try:
            handler = self.client['test']['test']
            result = {'link': item.get('link'),
                      'jslink': item.get('jslink'),
                      'imglink': item.get('imglink')}
            handler.insert(result)
        except:
            traceback.print_exc()

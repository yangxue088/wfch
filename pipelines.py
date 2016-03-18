# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem

import  json

from pymongo import MongoClient

MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017

class WfchPipeline(object):

    def __init__(self, client):
        self.db = client.wish

    @classmethod
    def from_settings(cls, settings):
        host = settings.get('MONGO_HOST', MONGO_HOST)
        port = settings.get('MONGO_PORT', MONGO_PORT)

        client = MongoClient(host=host, port=port)
        db = client.wish
        return cls(db)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def process_item(self, item, spider):
        if item is None or item['json'] is None or item['json'] == '':
            raise DropItem("none item found.")
        else:
            self.db.products.insert_one(json.loads(item['json']))
            return item

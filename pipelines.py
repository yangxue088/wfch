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
MONGO_COLL = 'products'

class WfchPipeline(object):

    def __init__(self, client, coll):
        self.db = client.wish
        self.coll = coll

    @classmethod
    def from_settings(cls, settings):
        host = settings.get('MONGO_HOST', MONGO_HOST)
        port = settings.get('MONGO_PORT', MONGO_PORT)
        coll = settings.get('MONGO_COLL', MONGO_COLL)

        client = MongoClient(host=host, port=port)
        return cls(client, coll)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def process_item(self, item, spider):
        if item is None or item['json'] is None or item['json'] == '':
            raise DropItem("none item found.")
        else:
            data = json.loads(item['json'])
            data['_id'] = data['id']
            self.db[self.coll].insert_one(data)
            return item

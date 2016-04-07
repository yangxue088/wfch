# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

from pymongo import MongoClient
from scrapy.exceptions import DropItem

from items import ProductItem, RatingItem

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
        return cls(client)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def process_item(self, item, spider):
        if isinstance(item, ProductItem):
            data = json.loads(item['json'])
            data['_id'] = data['id']
            self.db['products'].insert_one(data)
            return item
        elif isinstance(item, RatingItem):
            data = dict()
            data['_id'] = item['id']
            data['rating'] = item['rating']
            self.db['ratings'].insert_one(data)
            return item

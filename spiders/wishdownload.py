# -*- coding: utf-8 -*-

import logging

import re
from scrapy_redis.spiders import RedisSpider

from items import WfchItem


class WishdownloadSpider(RedisSpider):
    name = "wishdownload"
    allowed_domains = ["wish.com"]
    start_urls = (
        'http://www.wish.com/',
    )

    def __init__(self, redis_key='products'):
        self.redis_key = redis_key

    def parse(self, response):
        self.log('crawl page: {}'.format(response.url), logging.INFO)

        match = re.search("\['mainContestObj'\] = ({.*?});\n", response.body)
        if match:
            item = WfchItem()
            item['json'] = match.group(1)
            return item

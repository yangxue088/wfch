# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider

from ..items import WfchItem

import re

class WishdownloadSpider(RedisSpider):
    name = "wishdownload"
    allowed_domains = ["wish.com"]

    redis_key = 'products'

    def parse(self, response):
        match = re.search("\['mainContestObj'\] = ({.*?});\n", response.body)
        if match:
            item = WfchItem()
            item['json'] = match.group(1)
            return item

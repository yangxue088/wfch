# -*- coding: utf-8 -*-

import re
from scrapy_redis.spiders import RedisSpider

from ..items import WfchItem


class WishdownloadSpider(RedisSpider):
    name = "wishdownload"
    allowed_domains = ["wish.com"]

    def __init__(self, redis_key='products'):
        super(WishdownloadSpider, self).__init__(name, **kwargs)
        self.redis_key = redis_key

    def parse(self, response):
        match = re.search("\['mainContestObj'\] = ({.*?});\n", response.body)
        if match:
            item = WfchItem()
            item['json'] = match.group(1)
            return item

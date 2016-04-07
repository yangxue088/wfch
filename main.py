# -*- coding: utf-8 -*-

import sys

from scrapy.crawler import CrawlerProcess

from spiders.wish_rating import WishRatingSpider

if __name__ == '__main__':

    from scrapy import optional_features
    optional_features.remove('boto')

    username = sys.argv[1]
    password = sys.argv[2]
    num_spider = int(sys.argv[3])
    redis_key = sys.argv[4]

    process = CrawlerProcess({'ITEM_PIPELINES': {
        'pipelines.WfchPipeline': 300,
    }, 'LOG_LEVEL': 'INFO', 'LOG_FILE': 'target/log.rating'})

    for i in xrange(num_spider):
        process.crawl(WishRatingSpider, username=username, password=password, redis_key=redis_key)

    process.start()

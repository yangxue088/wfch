# -*- coding: utf-8 -*-

import sys

from scrapy.crawler import CrawlerProcess

from spiders.wishdownload import WishdownloadSpider

if __name__ == '__main__':

    from scrapy import optional_features
    optional_features.remove('boto')

    num_spider = int(sys.argv[1])
    redis_key = sys.argv[2]

    process = CrawlerProcess({'ITEM_PIPELINES': {
        'pipelines.WfchPipeline': 300,
    }, 'LOG_LEVEL': 'INFO', 'LOG_FILE': 'target/log.wfch'})

    for i in xrange(num_spider):
        process.crawl(WishdownloadSpider, redis_key=redis_key)

    process.start()

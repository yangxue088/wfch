# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    json = scrapy.Field()


class RatingItem(scrapy.Item):
    id = scrapy.Field()

    rating = scrapy.Field()
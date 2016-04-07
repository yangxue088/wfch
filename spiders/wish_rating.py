# -*- coding: utf-8 -*-

import json
import logging
from collections import defaultdict
from datetime import datetime
from urllib import urlencode, quote

import re
import scrapy
from scrapy_redis.spiders import RedisSpider

from items import RatingItem


class WishRatingSpider(RedisSpider):
    name = "wishrating"
    allowed_domains = ["wish.com"]
    start_urls = (
        'https://www.wish.com/',
    )

    start_time = datetime(2015, 10, 1)

    def __init__(self, username, password, redis_key):
        self.username = username
        self.password = password
        self.redis_key = redis_key
        self.logon = False
        self.xsrf = ''

        self.dicts = defaultdict(list)

    def start_requests(self):
        yield scrapy.Request('https://www.wish.com/', callback=self.login, priority=100)

    def login(self, response):
        match = re.compile(r'.*_xsrf=(.*?);').match(str(response.headers))

        if match:
            self.xsrf = match.group(1)
            self.log('rating spider before login', logging.INFO)
            yield scrapy.Request(
                'https://www.wish.com/api/email-login?email={}&password={}&_buckets=&_experiments='.format(
                    quote(self.username), quote(self.password)),
                method='POST',
                headers={
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Content-Type': ' application/x-www-form-urlencoded; charset=UTF-8',
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-XSRFToken': self.xsrf,
                },
                callback=self.after_login, priority=80)

    def after_login(self, response):
        self.log('spider login success', logging.INFO)
        self.logon = True

        while not self.logon:
            yield

        yield self.next_request()

    def parse(self, response):
        product_id = response.url.split('/')[-1]

        self.log('crawl product: {}'.format(product_id), logging.INFO)

        return self.feed_rating_ajax(product_id)

    def feed_rating_ajax(self, product_id, offset=0):
        data = {
            'product_id': product_id,
            'count': '30',
            'start': str(offset),
            '_buckets': '',
            '_experiments': '',
        }

        return scrapy.Request(
            'https://www.wish.com/api/product-ratings/get',
            method='POST', body=urlencode(data),
            headers={
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Content-Type': ' application/x-www-form-urlencoded; charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest',
                'X-XSRFToken': self.xsrf,
            },
            meta={
                'product_id': product_id,
            },
            callback=self.parse_feed_ajax)

    def parse_feed_ajax(self, response):
        json_data = json.loads(response.body)
        data = json_data.get('data', None)
        if data is not None:
            next_offset = data.get('next_offset')
            no_more_ratings = data.get('no_more_ratings', True)

            product_id = response.meta['product_id']

            for result in data.get('results'):
                time = datetime.strptime(result['time'], '%Y-%m-%dT%H:%M:%S+00:00')

                if time < self.start_time:
                    no_more_ratings = True
                    break

                self.dicts[product_id].append({'time': time, 'rating': result['rating']})

            if not no_more_ratings:
                return self.feed_rating_ajax(product_id, next_offset)
            else:
                item = RatingItem()
                item['id'] = product_id
                item['rating'] = self.dicts.pop(product_id, [])

                self.log('crawl product: {}, ratings: {}'.format(item['id'], len(item['rating'])), logging.INFO)
                return item

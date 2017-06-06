# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlappItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    uuid = scrapy.Field()
    classify = scrapy.Field()
    create_date = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    web_time = scrapy.Field()
    content = scrapy.Field()
    # browse = scrapy.Field()
    # love = scrapy.Field()

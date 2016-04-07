# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YelpItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    stars = scrapy.Field()
    top_item = scrapy.Field()
    street_address1 = scrapy.Field()
    street_address2 = scrapy.Field()
    reviews = scrapy.Field()

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Ed2000Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    tags = scrapy.Field()
    name = scrapy.Field()
    size = scrapy.Field()
    image_urls = scrapy.Field()
    image_paths = scrapy.Field()
    magnet_uri = scrapy.Field()
    ed2k_uris = scrapy.Field()

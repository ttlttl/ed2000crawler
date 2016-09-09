# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy import log, Request


class DuplicatePipeline(object):

    def __init__(self):
        self.seen = set()

    def process_item(self, item, spieder):
        if False:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.seen.add(item)
            return item


class ValidatePipeline(object):

    def process_item(self, item ,spider):
        return item


class GetImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        url = item['image_url']
        yield Request(url)

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        if not image_path:
            raise DropItem("Item contains no images")
        item['image_path'] = image_path
        return item


class MongoDBPipeline(object):
    def __init__(self):
        connection=pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db=connection[settings['MONGODB_DB']]
        self.collection=db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem('Missing{0}!'.format(data))
        if valid:
            self.collection.insert(dict(item))
            log.msg('Item added to Mongodb!', level=log.DEBUG, spider=spider)
        return item
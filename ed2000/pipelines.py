# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy import log, Request


#验证，去除空项
class ValidatePipeline(object):

    def process_item(self, item ,spider):
        if not item.get('name') or not (item.get('magnet_uri') or item.get('ed2k_uris')):
            raise DropItem('Drop %s' % item['name'])
        return item


#下载简介图片
class GetImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for url in item['image_urls']:
            yield Request(url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item


#存储
class MongoDBPipeline(object):

    def __init__(self):
        connection=pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db=connection[settings['MONGODB_DB']]
        self.collection=db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        log.msg('Item added to Mongodb!', level=log.DEBUG, spider=spider)
        return item

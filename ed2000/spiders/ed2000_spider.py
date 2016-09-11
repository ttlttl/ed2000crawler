#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
@author: ttlttl
@contact: wangmingape@gmail.com
@site: https://github.com/ttlttl
@file: ed2000_spider
@time: 9/8/2016 5:14 PM
"""


from scrapy import Spider, log, Request
from ed2000.items import Ed2000Item
import re


class Ed2000Spder(Spider):
    name = 'ed2000'
    allowed_domains = ['www.ed2000.com']
    #电影
    start_urls = [
        "http://www.ed2000.com/Type/%E7%94%B5%E5%BD%B1"
    ]
    #去重，存放提取过的url
    urls_seen = set()

    def parse(self, response):
        #分类-动作，喜剧...
        class_urls = [response.urljoin(url) for url in \
                      response.xpath('/html/body/div[@class="CurrentLocation"]/div[2]/a/@href').extract()]
        for url in class_urls:
            yield Request(url, callback=self.parse_class)

    def parse_class(self, response):
        #从分类页中提取详细信息页链接
        detail_urls = [response.urljoin(url) for url in \
                       response.xpath('//tr[@class="CommonListCell"]/td[1]/a[2]/@href').extract()]
        for url in detail_urls:
            yield Request(url, callback=self.parse_detail)
        #第2页，第3页。。。
        if not response.url.startswith('http://www.ed2000.com/FileList.asp'):
            page_urls = [ response.urljoin(url) for url in \
                    response.xpath('//div[@style="padding:5px;"]//a[@class="PageNum"]/@href')\
                    .extract()]
            for url in page_urls:
                if not url in self.urls_seen:
                    self.urls_seen.add(url)
                    yield Request(url, callback=self.parse_class)

    def parse_detail(self, response):
        item = Ed2000Item()
        item['tags'] = response.xpath('/html/body/table[1]//table//tr[6]/td[2]/a/text()').extract()
        item['name'] = response.xpath('/html/body/table[1]//table//tr[1]/td/text()').extract()[0]
        try:
            item['size'] = response.xpath('/html/body/table[1]//table//tr[4]/td[2]/text()').extract()[0]
        except IndexError:
            item['size'] = 'null'
        item['ed2k_uris'] = response.xpath('/html/body/table[@class="CommonListArea"]//tr[@class="CommonListCell"]//@href').extract()
        item['image_urls'] = response.xpath('//div[@class="PannelBody"]/img/@src').extract()
        tmp = re.search('ShowMagnet\("(magnet.*)"\);\\r', response.body)
        if tmp:
            item['magnet_uri'] = tmp.group(1)
        yield item




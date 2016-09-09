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

    def parse(self, response):
        #从列表页中提取详细信息也链接
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
                yield Request(url, callback=self.parse)


    def parse_detail(self, response):
        item = Ed2000Item()
        item['name'] = response.xpath('/html/body/table[1]//table//tr[1]/td/text()').extract()
        item['size'] = response.xpath('/html/body/table[1]//table//tr[4]/td[2]/text()').extract()
        item['ed2k_uri'] = response.xpath('/html/body/table[2]//tr[3]/td[2]/a/@href').extract()
        tmp = re.search('ShowMagnet\("(magnet.*)"\);\\r', response.body)
        if tmp:
            item['magnet_uri'] = tmp.group(1)
        print('-----------------------------------------------')
        print(item['name'])
        with open('test.txt', 'a+') as f:
            if item['name']:
                f.write(item['name'][0].encode('utf-8'))
                f.write('\n\r')
            if item['ed2k_uri']:
                f.write(item['ed2k_uri'][0].encode('utf-8'))
                f.write('\n\r')
            if item['magnet_uri']:
                f.write(item['magnet_uri'][0].encode('utf-8'))
                f.write('\n\r')
                f.write('\n\r')




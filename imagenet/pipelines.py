# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
#from io import BytesIO
#import hashlib


class ImagenetPipeline(ImagesPipeline):
    pass
#    def get_media_requests(self, item, info):
#        for image_url in item['image_urls']:
#            yield scrapy.Request(image_url)
#
#    def item_completed(self, results, item, info):
#        item['images'] = [x for ok, x in results if ok]
#        return item

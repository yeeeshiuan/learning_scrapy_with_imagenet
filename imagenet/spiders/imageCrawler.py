# -*- coding: utf-8 -*-
import scrapy
import re
import hashlib
import os
import sys
from io import BytesIO
from scrapy.utils.python import to_bytes
from PIL import Image

from imagenet.spiders.utils import interactive_input_interface

IMAGENET_DOWNLOAD_PAGE_URI = "http://image-net.org/api/text/imagenet.synset.geturls?wnid="

class ImagecrawlerSpider(scrapy.Spider):
    name = 'imageCrawler'
    # dependency: http://image-net.org/archive/words.txt

    def __init__(self, keyword='dog', *args, **kwargs):
        super(ImagecrawlerSpider, self).__init__(*args, **kwargs)
        self.keyword = keyword

        # create image directory if not exist
        if 'image' not in os.listdir('.'):
            os.mkdir('image')
        # create target directory if not exist
        if self.keyword not in os.listdir('image/'):
            os.mkdir('image/%s' % self.keyword)

        self.start_urls = ["http://image-net.org/archive/words.txt"]

    def parse(self, response):
        print("Loading ImageNet keywords list...")
        wnidMapWords = [line.split('\\t') for line in str(response.body).split('\\n')]
        # enter in interactive CLI interface
        winds = interactive_input_interface(wnidMapWords, self.keyword)

        if not winds:
            sys.exist(0)

        for downloadPageUrl in [ IMAGENET_DOWNLOAD_PAGE_URI + val for val in winds ]:
            yield scrapy.Request(downloadPageUrl, callback=self.parse_urls)

    def parse_urls(self, response):
        urls = str(response.body).split('\\r\\n')[:-1]
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_download)

    def parse_download(self, response):
        filename = hashlib.sha1(to_bytes(response.url)).hexdigest()
        path = 'image/%s/%s.jpg' % (self.keyword, filename)
        orig_image = Image.open(BytesIO(response.body))

        image, buf = self.convert_image(orig_image)

        with open(path, 'wb') as f:
            f.write(buf.getvalue())

        self.log("Download image %s" % filename)

    def convert_image(self, image):
        if image.format == 'PNG' and image.mode == 'RGBA':
            background = Image.new('RGBA', image.size, (255, 255, 255))
            background.paste(image, image)
            image = background.convert('RGB')
        elif image.mode == 'P':
            image = image.convert("RGBA")
            background = Image.new('RGBA', image.size, (255, 255, 255))
            background.paste(image, image)
            image = background.convert('RGB')
        elif image.mode != 'RGB':
            image = image.convert('RGB')

        buf = BytesIO()
        image.save(buf, 'JPEG')
        return image, buf

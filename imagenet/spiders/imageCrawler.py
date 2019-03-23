# -*- coding: utf-8 -*-
import scrapy
import re
import hashlib
import os
from io import BytesIO
from scrapy.utils.python import to_bytes
from PIL import Image
#from scrapy.loader import ItemLoader

#from imagenet.items import ImagenetItem



class ImagecrawlerSpider(scrapy.Spider):
    name = 'imageCrawler'
    # TODO: http://image-net.org/archive/words.txt

    def __init__(self, getSearch='dog', wnid=None, *args, **kwargs):
        super(ImagecrawlerSpider, self).__init__(*args, **kwargs)
        self.wnid=wnid
        self.getSearch = getSearch

        if 'image' not in os.listdir('.'):
            os.mkdir('image')
        if self.getSearch not in os.listdir('image/'):
            os.mkdir('image/%s' % self.getSearch)
        url = "http://www.image-net.org/search?q=" + getSearch
        if self.wnid:
            url = "http://image-net.org/api/text/imagenet.synset.geturls?wnid=" + wnid
        
        self.start_urls = [url]

    def parse(self, response):
        if self.wnid:
            urls = str(response.body).split('\\r\\n')[:-1]
            for url in urls:
                yield scrapy.Request(url, callback=self.parse_download)
        else:
            mainLinks = response.xpath('//td[@width="70%"]/a/@href').extract()

            for mainLink in mainLinks:
                wnidSeg = re.search('\?([^\?]+)', mainLink)
                download_page = "api/text/imagenet.synset.geturls?" + wnidSeg.group(1)
                yield scrapy.Request(response.urljoin(download_page), callback=self.parse_urls)

    def parse_urls(self, response):
        urls = str(response.body).split('\\r\\n')[:-1]
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_download)

    def parse_download(self, response):
        filename = hashlib.sha1(to_bytes(response.url)).hexdigest()
        path = 'image/%s/%s.jpg' % (self.getSearch, filename)
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

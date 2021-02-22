import scrapy


class LkongSpider(scrapy.Spider):
    name = 'lkong'
    allowed_domains = ['www.lkong.net']
    start_urls = ['http://www.lkong.net/']

    def parse(self, response):
        pass

import scrapy


class PrivateSpider(scrapy.Spider):
    name = 'private'
    allowed_domains = ['www.privateclassics.com']
    start_urls = ['https://www.privateclassics.com/']

    def parse(self, response):
        pass

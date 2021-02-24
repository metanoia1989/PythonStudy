import scrapy


class QuestionSpider(scrapy.Spider):
    name = 'question'
    allowed_domains = ['wx.anzhuoxfpx.com']
    start_urls = ['http://wx.anzhuoxfpx.com/member/']

    def parse(self, response):
        pass

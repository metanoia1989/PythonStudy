from VintageEeroticaForum.items import PornStartItem
import scrapy


class VintageSpider(scrapy.Spider):
    name = 'vintage'
    allowed_domains = ['vintage-erotica-forum.com']
    start_urls = ['http://vintage-erotica-forum.com/t4681-classic-pornstar-list-a-to-z.html']

    def parse(self, response):
        # 下一页处理
        links = response.css('.pagenav.awn-ignore:first-child .alt1 a::attr(href)').getall()       
        next_pages = []
        [next_pages.append(x) for x in links if x not in next_pages]
        for next_page in next_pages:
            yield response.follow(next_page, callback=self.parse_page)

        self.prase_page(response)
        
    def prase_page(self, response):
        """
        解析提取所有的明星链接
        """ 
        a_items = response.css('[id^="post_message_"] a')
        for a_item in a_items:
            porn_item = PornStartItem()
            porn_item["link"] = a_item.css('::attr(href)').get()
            porn_item["name"] = a_item.css('::text').get()
            if porn_item["name"] == '' or porn_item.isspace():
                continue
            yield porn_item
            # yield response.follow(porn_item["link"], callback=self.parse_porn_star)
            
    def parse_porn_start(self, response):
        """
        解析单个明星的数据
        """

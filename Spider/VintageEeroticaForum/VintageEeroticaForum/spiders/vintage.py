from VintageEeroticaForum.items import ImgItem, PornStartItem
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
            
        # 解析当前页面
        self.parse_page(response)
        
    def parse_page(self, response):
        """
        解析提取所有的明星链接
        """ 
        a_items = response.css('[id^="post_message_"] a')
        for a_item in a_items:
            porn_item = PornStartItem()
            porn_item["link"] = a_item.css('::attr(href)').get()
            porn_item["name"] = a_item.css('::text').get()
            if porn_item["name"] is None or porn_item["name"] == '' or porn_item["name"].isspace():
                continue
            print("提取明星数据", porn_item)
            yield response.follow(
                porn_item["link"], 
                callback=self.parse_porn_star,
                cb_kwargs={ "name": porn_item["name"] }
            )

            
    def parse_porn_star(self, response, name):
        """
        解析单个明星的数据
        """
        # 解析单个页面
        self.fetchImageItem(response, name)
        
        # 解析下一页
        next_page = response.css('.pagenav.awn-ignore:first-child .alt1 a[rel="next"]::attr(href)').get()       
        if next_page is not None:
            yield response.follow(next_page, callback=self.fetchImageItem, cb_kwargs={"name": name})

    def fetchImageItem(self, response, name):
        """
        提取明星页面的图片
        """
        img_srcs = response.css('[id^="post_message_"] img::attr(src)').getall()
        img_srcs = list(filter(lambda item: item.startswith("http"), img_srcs))
        imgItem = ImgItem()
        imgItem["pornName"] = name
        imgItem["image_urls"] = img_srcs
        print("提取图片", imgItem)
        yield imgItem

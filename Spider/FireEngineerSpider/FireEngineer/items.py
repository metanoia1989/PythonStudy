# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ChapterItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    level = scrapy.Field()
    pid = scrapy.Field()

class QuestionItem(scrapy.Item):
    # define the fields for your item here like:
    chapater_id = scrapy.Field()
    title = scrapy.Field()
    questtype = scrapy.Field()
    content = scrapy.Field()
    select = scrapy.Field()
    order = scrapy.Field()
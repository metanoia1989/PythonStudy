# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from VintageEeroticaForum.items import PornStartItem
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class PronStartItemPipeline:
    pornstar_names = set()
    pornstar_items = []
    
    def process_item(self, item, spider):
        if isinstance(item, PornStartItem):
            if item["name"] in self.pornstar_names:
                raise DropItem("Duplicate item found: %1".format(item["name"]))
            else:
                self.pornstar_names.add(item["name"])

            return item

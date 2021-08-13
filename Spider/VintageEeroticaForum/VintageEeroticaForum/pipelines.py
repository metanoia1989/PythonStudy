# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from VintageEeroticaForum.items import ImgItem, PornStartItem
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
from urllib.parse import urlparse
import os

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

class DownloadImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        pornName = item["pornName"]
        return  f"{pornName}/" + os.path.basename(urlparse(request.url).path)    

    def get_media_requests(self, item, info):
        print("获取信息", item)
        if isinstance(item, ImgItem):
            for image_url in item['image_urls']:
                yield Request(image_url)
         
    def item_completed(self, results, item, info):
        print(results, item)
        image_paths = [ x['path'] for ok, x in results if ok ]
        if not image_paths:
            raise DropItem("Item contains no images")
        item["image_paths"] = image_paths
        return item

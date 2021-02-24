# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from scrapy.exceptions import DropItem
from FireEngineer.items import ChapterItem, QuestionItem 
from FireEngineer.mysql import MySQL

class MysqlPipeline:

    def open_spider(self, spider):
        db = spider.settings.get('MYSQL_DB_NAME','fire_engineer')
        host = spider.settings.get('MYSQL_HOST', 'localhost')
        port = spider.settings.get('MYSQL_PORT', 3306)
        user = spider.settings.get('MYSQL_USER', 'root')
        passwd = spider.settings.get('MYSQL_PASSWORD', 'root')        
        
        self.db = MySQL(host, user, passwd, db)

    def process_item(self, item, spider):
        if isinstance(item, ChapterItem):
            sql = "select * from fire_chapter where name = %s and pid = %s"
            if self.db.select_one(sql, [item.name, item.pid]):
                raise DropItem("Duplicate chapter item found: %s. Filter was %s" % (item))
            sql = "INSERT INTO `fire_chapter` ( `name`, `level`, `pid` ) VALUES ( %s, %s, %s)"
            self.db.insert(sql, [item.name, item.level, item.pid])
            
        if isinstance(item, QuestionItem):
            sql = "select * from fire_questions where title = %s and chapter_id = %s"
            if self.db.select_one(sql, [item.title, item.chapter_id]):
                raise DropItem("Duplicate question item found: %s. Filter was %s" % (item))
            sql = """
                INSERT INTO `fire_questions` ( `chapter_id`, `title`, `questype`, `content`, `select`, `order`) 
                VALUES ( %s, %s, %s, %s, %s, %s)
            """
            data = (item.chapter_id, item.title, item.questtype, item.content, item.select, item.order)
            self.db.insert(sql, data)

        return item

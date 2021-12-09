# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


import pymysql

from rating import settings


class RatingPipeline:
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            db=settings.MYSQL_DBNAME,
            charset='utf8'
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        insert_sql = "INSERT INTO tp_rating(id, title, cf_name, cf_rating, cf_solve_num, luogu_id, " \
                     "luogu_solve_num, is_success, description, time) VALUES ('%d', '%s', '%s', '%d', '%d', '%d', " \
                     "'%d', '%r', '%s', '%s')" % (item['id'], item['name'], item.get('cf_name', None),
                                            item.get('cf_rating', 0), item.get('cf_solve_num', 0),
                                            item.get('luogu_id', 0), item.get('luogu_solve_num', 0),
                                            int(item.get('is_success', False)),
                                            item.get('description', ""),
                                            item['time'])
        self.cursor.execute(insert_sql)
        self.connect.commit()

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()

import scrapy
from scrapy import Request
import time

from rating import settings
from rating.items import RatingItem
from rating.spiders.get_url import get_cf_url, get_luogu_url_uid
import pymysql


class AcmSpider(scrapy.Spider):
    name = "acm"

    def start_requests(self):
        conn = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            db=settings.MYSQL_DBNAME,
            charset='utf8'
        )
        cursor = conn.cursor()
        #
        sql = "select id, title, cf_name, luogu_id from acm.user"

        # sql = "select id, title, cf_name, luogu_id from tp6.tp_dygl"

        cursor.execute(sql)
        results = cursor.fetchall()
        for result in results:
            item = RatingItem()
            item['id'] = result[0]
            item['name'] = result[1]
            item['cf_name'] = result[2]
            item['luogu_id'] = result[3]
            item['time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            if item['cf_name'] is None or item['cf_name'] == "":
                yield Request(url=get_luogu_url_uid(item['luogu_id']), meta={'item': item},
                          callback=self.parse_luogu_uid, dont_filter=True)
            else:
                yield Request(url=get_cf_url(item['cf_name']), meta={'item': item}, callback=self.parse_cf)

    def parse_cf(self, response):
        item = response.meta['item']
        item['cf_rating'] = int(
            response.xpath('//*[@id="pageContent"]/div[2]/div[5]/div[2]/ul/li[1]/span[1]/text()').get())
        item['cf_solve_num'] = int(
            response.xpath('//*[@id="pageContent"]/div[4]/div/div[7]/div[1]/div[1]/div[1]/text()').get().split()[0])
        yield Request(url=get_luogu_url_uid(item['luogu_id']), meta={'item': item}, callback=self.parse_luogu_uid, dont_filter=True)

    def parse_luogu_uid(self, response):
        item = response.meta['item']
        if item['luogu_id'] != 0 and response.json()['code'] == 200:
            item['luogu_solve_num'] = int(response.json()['currentData']['user']['passedProblemCount'])
            item['is_success'] = True
        else:
            item['is_success'] = False
            item['description'] = item.get('description', "") + 'luogu id is incorrect!'
        return item

import scrapy
from scrapy import Request
import time

from rating import settings
from rating.items import RatingItem
from rating.spiders.get_url import get_cf_url, get_luogu_url_uid, get_niuke_url, get_atcoder_url
import pymysql


class AcmSpider(scrapy.Spider):
    name = "acm"

    def start_requests(self):
        conn = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWD,
            db=settings.MYSQL_DBNAME,
            charset='utf8'
        )
        cursor = conn.cursor()
        #
        sql = "select id, title, pid, cf_name, luogu_id, niuke_id, atcoder_name from tp6.tp_dygl"

        cursor.execute(sql)
        results = cursor.fetchall()
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        for result in results:
            item = RatingItem()
            item['id'] = result[0]
            item['name'] = result[1]
            item['pid'] = result[2]
            item['cf_name'] = result[3]
            item['luogu_id'] = result[4]
            item['niuke_id'] = result[5]
            item['atcoder_name'] = result[6]
            item['time'] = current_time
            if item['cf_name'] is None or item['cf_name'] == "":
                item['description'] = item.get('description', "") + 'cf name is incorrect!'
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
        yield Request(url=get_luogu_url_uid(item['luogu_id']), meta={'item': item}, callback=self.parse_luogu,
                      dont_filter=True)

    def parse_luogu(self, response):
        item = response.meta['item']
        if item['luogu_id'] != 0 and response.json()['code'] == 200:
            item['luogu_solve_num'] = int(response.json()['currentData']['user']['passedProblemCount'])
            item['is_success'] = True
        else:
            item['is_success'] = False
            item['description'] = item.get('description', "") + 'luogu id is incorrect!'
        yield Request(url=get_niuke_url(item['niuke_id']), meta={'item': item}, callback=self.parse_niuke,
                      dont_filter=True)

    def parse_niuke(self, response):
        item = response.meta['item']
        if item['niuke_id'] is not None and item['niuke_id'] != 0 and len(response.xpath("//div[has-class('null')]").getall()) == 0:
            item['niuke_solve_num'] = int(response.xpath("//div[has-class('my-state-item') and "
                                                         "contains(., '题已通过')]/div[1]/text()").getall()[0])
            item['is_success'] = True
        else:
            item['is_success'] = False
            item['description'] = item.get('description', "") + 'niuke id is incorrect!'
        yield Request(url=get_atcoder_url(item['atcoder_name']), meta={'item': item}, callback=self.parse_atcoder,
                      dont_filter=True)

    def parse_atcoder(self, response):
        item = response.meta['item']
        if item['atcoder_name'] is not None and item['atcoder_name'] != '':
            ac = 0
            for i in response.json():
                if i['result'] == 'AC':
                    ac += 1
            item['atcoder_solve_num'] = ac
            item['is_success'] = True
        else:
            item['is_success'] = False
            item['atcoder_solve_num'] = 0
            item['description'] = item.get('description', "") + 'atcoder name is incorrect!'
        return item

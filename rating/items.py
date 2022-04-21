# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RatingItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    pid = scrapy.Field()
    cf_name = scrapy.Field()
    cf_rating = scrapy.Field()
    cf_solve_num = scrapy.Field()
    luogu_id = scrapy.Field()
    luogu_solve_num = scrapy.Field()
    niuke_id = scrapy.Field()
    niuke_solve_num = scrapy.Field()
    atcoder_name = scrapy.Field()
    atcoder_solve_num = scrapy.Field()
    time = scrapy.Field()
    is_success = scrapy.Field()
    description = scrapy.Field()

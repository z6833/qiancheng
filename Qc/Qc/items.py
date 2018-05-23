# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class QcItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 数据来源
    source = scrapy.Field()
    # 抓取时间
    utc_time = scrapy.Field()

    # 职位名称
    work_position = scrapy.Field()
    # 公司名称
    name_company = scrapy.Field()
    # 工作地点
    work_place = scrapy.Field()
    # 薪资范围
    salary = scrapy.Field()
    # 发布时间
    publish_time = scrapy.Field()

    # 工作详情
    content = scrapy.Field()
    # 联系方式
    contact = scrapy.Field()

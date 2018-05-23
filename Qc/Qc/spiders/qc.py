# -*- coding: utf-8 -*-
import re
import scrapy
from Qc.items import QcItem

class QcSpider(scrapy.Spider):
    name = 'qc'
    # allowed_domains = ['51job.com']

    # 开始url
    start_urls = ['https://search.51job.com/list/000000,000000,0000,00,9,99,python,2,1.html']

    def parse(self, response):
        # 先编写下载中间件，给每个请求加一个User-Agent
        # 解析数据
        node_list = response.xpath('//div[@class="el"]')
        for node in node_list:

            # 匹配详情页链接,观察51job发现前面4个节点不是招聘信息，因此也没有详情页
            # 因此，取不到详情页链接，表示可以忽略，不用存
            detail_link = node.xpath('./p/span/a/@href')
            if detail_link:
                item = QcItem()
                item['work_position'] = node.xpath('./p/span/a/@title').extract_first()
                item['name_company'] = node.xpath('./span[@class="t2"]/a/text()').extract_first()
                item['work_place'] = node.xpath('./span[@class="t3"]/text()').extract_first()
                item['salary'] = node.xpath('./span[@class="t4"]/text()').extract_first()
                item['publish_time'] = node.xpath('./span[@class="t5"]/text()').extract_first()

                # 解析详情页数据
                yield scrapy.Request(detail_link.extract_first(), callback=self.parse_detail, meta={"item": item})

    def parse_detail(self, response):
        item = response.meta['item']
        # 编写下载中间件，将详情页链接存到redis中，达到去重复的目的

        # 解析页面所有数据
        content = response.xpath('//div[@class="bmsg job_msg inbox"]').xpath('string(.)').extract()

        # content = response.xpath('//div[@class="bmsg job_msg inbox"]/*/text()').extract()
        # 取联系方式
        contact = response.xpath('//div[@class="bmsg inbox"]/p/text()').extract()

        # 拿到的content有空格和换行符，利用正则，去掉空白符
        item['content'] = re.sub('\s', '', ''.join(content))
        item['contact'] = ''.join(contact).strip()

        yield item

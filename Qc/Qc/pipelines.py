# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymongo
import pymysql
from datetime import datetime

class QcPipeline(object):
    def process_item(self, item, spider):

        # 添加数据源
        item['source'] = spider.name

        # 添加爬取时间
        item['utc_time'] = str(datetime.utcnow())

        return item

class QcJsonPipeline(object):
    """
    保存为json数据
    """
    def open_spider(self, spider):

        # 打开文件
        self.file = open('qc.json', 'a', encoding='utf-8')

    def process_item(self, item, spider):

        content = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(content)

        return item

    def close_spider(self, spider):
        self.file.close()

class QcMongoPipeline(object):
    """
    存入大Mongodb中
    """
    def open_spider(self, spider):

        # 实例化mongo客户端并链接
        self.client = pymongo.MongoClient(host='localhost', port=27017)
        # 创建库和集合
        self.collection = self.client['qc']['qc']

    def process_item(self, item, spider):
        # 添加数据
        self.collection.insert(dict(item))

        return item

    def close_spider(self, spider):
        # 关闭数据库
        self.client.close()


class QcMysqlPipeline(object):
    """
    数据存入到mysql
    """
    def open_spider(self, spider):
        self.conn = pymysql.connect(
            host='localhost',
            port=3306,
            database='qc',
            user='z',
            password='136833',
            charset='utf8'
        )
        # 实例一个游标
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):

        sql = ("insert into qc(source, utcTime, workName, "
               "company, workPosition, salary, publishTime, "
               "content, contact)"
               "values (%s, %s, %s, %s, %s, %s, %s, %s, %s)")

        list_item = [item['source'], item['utc_time'], item['work_position'],
                  item['name_company'], item['work_place'], item['salary'], item['publish_time'],
                  item['content'], item['contact']]

        self.cursor.execute(sql, list_item)
        # 提交数据
        self.conn.commit()

        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

    # create table qc
    # (
    #     id INT unsigned PRIMARY KEY auto_increment NOT NULL,
    #     source VARCHAR(20) DEFAULT "",
    #     utcTime DATETIME DEFAULT "1111-11-11 11:11:11",
    #     workName VARCHAR(40) DEFAULT "",
    #     company VARCHAR(40) DEFAULT "",
    #     workPosition VARCHAR(40) DEFAULT "",
    #     salary VARCHAR(40) DEFAULT "",
    #     publishTime VARCHAR(20) DEFAULT "",
    #     content TEXT(1024),
    #     contact VARCHAR(40) DEFAULT ""
    # );


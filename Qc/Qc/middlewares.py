# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random
import hashlib
import redis
from scrapy.exceptions import IgnoreRequest
from Qc.settings import USER_AGENTS as ua


class QcSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    def process_request(self, request, spider):
        """
        给每一个请求随机分配一个代理
        :param request:
        :param spider:
        :return:
        """
        user_agent = random.choice(ua)
        request.headers['User-Agent'] = user_agent

class QcRedisMiddleware(object):
    """
    将第一个页面上的每一个url放入redis的set类型中，防止重复爬取
    """
    # 连接redis
    def __init__(self):
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=1)

    def process_request(self, request, spider):

        # 将来自详情页的链接存到redis中
        if request.url.startswith("https://jobs.51job.com/"):
            # MD5加密详情页链接
            url_md5 = hashlib.md5(request.url.encode()).hexdigest()

            # 添加到redis，添加成功返回True,否则返回False
            result = self.redis.sadd('qc_url', url_md5)

            # 添加失败，说明链接已爬取，忽略该请求
            if not result:
                raise IgnoreRequest
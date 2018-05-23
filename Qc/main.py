from scrapy import cmdline
import time

# cmdline.execute("scrapy crawl qc".split())


import os
import time

while True:
    """
    每隔10s自动爬取一次，实现自动更新
    """
    os.system("scrapy crawl qc")
    time.sleep(20)
# -*- coding: utf-8 -*-

import time
from multiprocessing import Process

import logging
import schedule
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from model import loadSession
from model.rules import Rule
from spiders.proxy_spider import ProxySpiderSpider


def run():
    settings = get_project_settings()

    try:
        session = loadSession()
        # 取出规则表中已激活的rule
        rules = session.query(Rule).filter(Rule.enable == 1)
    except Exception, e:
        logging.info("Error: %s" % str(e))
    finally:
        session.close()

    process = CrawlerProcess(settings)

    for rule in rules:
        process.crawl(ProxySpiderSpider, rule)
    process.start()

def run_spider():
    p = Process(target=run)
    p.start()
    p.join()

if __name__ == '__main__':
    schedule.every(1).minutes.do(run_spider)
    while True:
        schedule.run_pending()
        # time.sleep(1)防止cpu占用过高
        time.sleep(1)

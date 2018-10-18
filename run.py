# -*- coding: utf-8 -*-
import subprocess
from Queue import Queue

from multiprocessing import Process

import schedule
import time

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings

from spider_website.model import loadSession
from spider_website.model.rules import Rule
from spider_website.spiders.proxy_spider import ProxySpiderSpider

import scrapy.spiderloader
import scrapy.statscollectors
import scrapy.logformatter
import scrapy.dupefilters
import scrapy.squeues

import scrapy.extensions.spiderstate
import scrapy.extensions.corestats
import scrapy.extensions.telnet
import scrapy.extensions.logstats
import scrapy.extensions.memusage
import scrapy.extensions.memdebug
import scrapy.extensions.feedexport
import scrapy.extensions.closespider
import scrapy.extensions.debug
import scrapy.extensions.httpcache
import scrapy.extensions.statsmailer
import scrapy.extensions.throttle

import scrapy.core.scheduler
import scrapy.core.engine
import scrapy.core.scraper
import scrapy.core.spidermw
import scrapy.core.downloader

import scrapy.downloadermiddlewares.stats
import scrapy.downloadermiddlewares.httpcache
import scrapy.downloadermiddlewares.cookies
import scrapy.downloadermiddlewares.useragent
import scrapy.downloadermiddlewares.httpproxy
import scrapy.downloadermiddlewares.ajaxcrawl
import scrapy.downloadermiddlewares.decompression
import scrapy.downloadermiddlewares.defaultheaders
import scrapy.downloadermiddlewares.downloadtimeout
import scrapy.downloadermiddlewares.httpauth
import scrapy.downloadermiddlewares.httpcompression
import scrapy.downloadermiddlewares.redirect
import scrapy.downloadermiddlewares.retry
import scrapy.downloadermiddlewares.robotstxt

import scrapy.spidermiddlewares.depth
import scrapy.spidermiddlewares.httperror
import scrapy.spidermiddlewares.offsite
import scrapy.spidermiddlewares.referer
import scrapy.spidermiddlewares.urllength

import scrapy.pipelines

import scrapy.core.downloader.handlers.http
import scrapy.core.downloader.contextfactory

def run():
    # # spider相关设置
    # settings = Settings()
    # '''
    # Scrapy框架的高度灵活性得益于其数据管道的架构设计，开发者可以通过简单的配置就能轻松地添加新特性。
    # 我们可以通过如下的方式添加pipline。
    # '''
    # settings.set("ITEM_PIPELINES", {
    #     'spider_website.pipelines.DuplicatesPipeline': 200,
    #     'spider_website.pipelines.IpProxyPoolPipeline': 300,
    # })
    #
    # # 设置默认请求头
    # settings.set("DEFAULT_REQUEST_HEADERS", {
    #     'Accept': 'text/html, application/xhtml+xml, application/xml',
    #     'Accept-Language': 'zh-CN,zh;q=0.8'}
    #              )
    #
    # # 注册自定义中间件，激活切换UA的组件和切换代理IP的组件
    # settings.set("DOWNLOADER_MIDDLEWARES", {
    #     'spider_website.middlewares.UserAgent': 1,
    #     # 'proxy_middlewares.ProxyMiddleware':100,
    #     'scrapy.downloadermiddleware.useragent.UserAgentMiddleware': None,
    # }
    #              )
    # # 设置爬取间隔
    # settings.set("DOWNLOAD_DELAY", 1)
    #
    # # 禁用cookies
    # settings.get("COOKIES_ENABLED", False)
    #
    # # 设定是否遵循目标站点robot.txt中的规则
    # settings.get("ROBOTSTXT_OBEY", True)

    settings = get_project_settings()

    session = loadSession()
    # 取出规则表中已激活的rule
    rules = session.query(Rule).filter(Rule.enable == 1)

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

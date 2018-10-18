# -*- coding: utf-8 -*-
import scrapy
from pydispatch import dispatcher
from scrapy import signals
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


# 抓取信息的数据结构，类似于javabean
class IpProxyPoolItem(scrapy.Item):
    ip_port = scrapy.Field()
    type = scrapy.Field()
    level = scrapy.Field()
    location = scrapy.Field()
    speed = scrapy.Field()
    lifetime = scrapy.Field()
    lastcheck = scrapy.Field()
    rule_id = scrapy.Field()
    source = scrapy.Field()


# 搭建spider的主体框架，继承CrawlSpider类
class ProxySpiderSpider(CrawlSpider):
    name = 'MagicSpider'

    def __init__(self, rule):
        # spider启动信号和spider_opened函数绑定
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        # spider关闭信号和spider_spider_closed函数绑定
        dispatcher.connect(self.spider_closed, signals.spider_closed)

        self.rule = rule
        self.name = rule.name
        # spilt函数通过分隔符分割字符串，得到列表类型
        self.allowed_domains = rule.allowed_domains.split(',')
        self.start_urls = rule.start_urls.split(',')
        rule_list = []

        # 添加"下一页"链接的规则
        if len(rule.next_page):
            rule_list.append(Rule(LinkExtractor(restrict_xpaths=rule.next_page), follow=True))
        # 链接提取规则
        rule_list.append(Rule(LinkExtractor(
            allow=rule.allow_url.split(','),
            unique=True),  # 链接去重
            follow=True,  # 跟随爬取
            callback='parse_item'))  # 调用parse_item提取数据
        # 使用tuple()将列表转换为元组
        self.rules = tuple(rule_list)
        # 当有子类继承ProxySpiderSpider的时候，调用初始化方法启动爬取过程
        super(ProxySpiderSpider, self).__init__()

    # spider启动时的逻辑
    def spider_opened(self, spider):
        print "spider is running!"

    # spider关闭时的逻辑
    def spider_closed(self, spider):
        print "spider is closed!"

    def parse_item(self, response):
        item = IpProxyPoolItem()
        if len(self.rule.loop_xpath):
            for proxy in response.xpath(self.rule.loop_xpath):
                if len(self.rule.ip_xpath):
                    tmp_ip = proxy.xpath(self.rule.ip_xpath).extract_first()
                    # strip函数用来删除空白字符(包括'\n', '\r',  '\t',  ' ')
                    ip = tmp_ip.strip() if tmp_ip is not None else ""
                else:
                    ip = ""
                if len(self.rule.port_xpath):
                    tmp_port = proxy.xpath(self.rule.port_xpath).extract_first()
                    port = tmp_port.strip() if tmp_port is not None else ""
                else:
                    port = ""
                if len(self.rule.location1_xpath):
                    tmp_location1 = proxy.xpath(self.rule.location1_xpath).extract_first()
                    location1 = tmp_location1.strip() if tmp_location1 is not None else ""
                else:
                    location1 = ""
                if len(self.rule.location2_xpath):
                    tmp_location2 = proxy.xpath(self.rule.location2_xpath).extract_first()
                    location2 = tmp_location2.strip() if tmp_location2 is not None else ""
                else:
                    location2 = ""
                if len(self.rule.lifetime_xpath):
                    tmp_lifetime = proxy.xpath(self.rule.lifetime_xpath).extract_first()
                    lifetime = tmp_lifetime.strip() if tmp_lifetime is not None else ""
                else:
                    lifetime = ""
                if len(self.rule.lastcheck_xpath):
                    tmp_lastcheck = proxy.xpath(self.rule.lastcheck_xpath).extract_first()
                    lastcheck = tmp_lastcheck.strip() if tmp_lastcheck is not None else ""
                else:
                    lastcheck = ""
                if len(self.rule.level_xpath):
                    tmp_level = proxy.xpath(self.rule.level_xpath).extract_first()
                    level = tmp_level.strip() if tmp_level is not None else ""
                else:
                    level = ""
                if len(self.rule.type_xpath):
                    tmp_type = proxy.xpath(self.rule.type_xpath).extract_first()
                    type = tmp_type.strip() if tmp_type is not None else ""
                else:
                    type = ""
                if len(self.rule.speed_xpath):
                    tmp_speed = proxy.xpath(self.rule.speed_xpath).extract_first()
                    speed = tmp_speed.strip() if tmp_speed is not None else ""
                else:
                    speed = ""
                # join函数用来拼接字符串，接收的参数为列表类型
                item['ip_port'] = (":".join([ip, port])) if len(port) else ip
                item['type'] = type
                item['level'] = level
                item['location'] = (" ".join([location1, location2])) if location2 is not None and len(
                    location2) else location1
                item['speed'] = speed
                item['lifetime'] = lifetime
                item['lastcheck'] = lastcheck
                item['rule_id'] = self.rule.id
                item['source'] = response.url
                yield item

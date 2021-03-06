# -*- coding: utf-8 -*-
import MySQLdb
from scrapy.exceptions import DropItem
import redis

import logging

from spider_website.model import proxy, engine, Base, loadSession

Base.metadata.create_all(engine)
Redis = redis.StrictRedis(host='*.*.*.*', port=6379, db=0, password='*')


# item去重
class DuplicatesPipeline(object):
    def process_item(self, item, spider):
        if Redis.exists('ip_port:%s' % item['ip_port']):
            raise DropItem("Duplicate item found: %s" % item)
        else:
            Redis.set('ip_port:%s' % item['ip_port'], 1)
            return item


# 数据入库
class IpProxyPoolPipeline(object):
    def process_item(self, item, spider):
        if len(item['ip_port']):
            a = proxy.Proxy(
                ip_port=item['ip_port'],
                type=item['type'],
                level=item['level'],
                location=item['location'],
                speed=item['speed'],
                lifetime=item['lifetime'],
                lastcheck=item['lastcheck'],
                rule_id=item['rule_id'],
                source=item['source']
            )
            session = loadSession()
            try:
                session.merge(a)
                session.commit()
            except MySQLdb.IntegrityError, e:
                logging.info("MySQL Error: %s" % str(e))
            finally:
                session.close()
            return item
        else:
            logging.info("ip_port is invalid!")

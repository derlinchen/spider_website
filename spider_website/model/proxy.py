# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Integer, DateTime
from . import Base
import datetime


class Proxy(Base):  # 继承Base类
    __tablename__ = 'proxies'

    ip_port = Column(String(30), primary_key=True, nullable=False)  # 主键
    type = Column(String(20), nullable=True, default="")  # 协议类型
    level = Column(String(20), nullable=True, default="")  # 匿名级别
    location = Column(String(100), nullable=True, default="")  # ip所在地区
    speed = Column(String(20), nullable=True, default="")  # 连接速度
    lifetime = Column(String(20), nullable=True, default="")  # 生存时间
    lastcheck = Column(String(20), nullable=True, default="")  # 最后校验时间
    source = Column(String(500), nullable=False)  # 页面地址
    rule_id = Column(Integer, nullable=False)  # 规则(网站/spider)id
    indate = Column(DateTime, nullable=False)  # 入库时间

    def __init__(self, ip_port, source, type, level, location, speed, lifetime, lastcheck, rule_id):
        self.ip_port = ip_port
        self.type = type
        self.level = level
        self.location = location
        self.speed = speed
        self.source = source
        self.lifetime = lifetime
        self.lastcheck = lastcheck
        self.rule_id = rule_id
        self.indate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

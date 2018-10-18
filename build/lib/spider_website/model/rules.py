# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Integer
from sqlalchemy import Sequence
from . import Base


class Rule(Base):
    __tablename__ = 'rules'
    # 表结构:
    id = Column(Integer, Sequence('id', start=1, increment=1), primary_key=True)  # 设定自增长主键
    name = Column(String(100), nullable=False)  # spider的名字
    allowed_domains = Column(String(500), nullable=False)  # 允许爬取的域
    start_urls = Column(String(500), nullable=False)  # 开始爬取的入口
    next_page = Column(String(500), nullable=False, default="")  # xpath表达式，爬取下一页
    allow_url = Column(String(500), nullable=False)  # 正则表达式，匹配符合要求的链接
    extract_from = Column(String(500), nullable=False, default="")  # xpath表达式，限制解析区域
    loop_xpath = Column(String(500), nullable=False)  # xpath表达式，控制单页面循环次数
    ip_xpath = Column(String(500), nullable=False)  # xpath表达式，解析IP
    port_xpath = Column(String(500), nullable=False, default="")  # xpath表达式，解析端口
    location1_xpath = Column(String(500), nullable=False)  # xpath表达式，解析区域
    location2_xpath = Column(String(500), nullable=False, default="")  # xpath表达式，解析区域
    speed_xpath = Column(String(500), nullable=False, default="")  # xpath表达式，解析连接速度
    lifetime_xpath = Column(String(500), nullable=False, default="")  # xpath表达式，解析生存时间
    type_xpath = Column(String(500), nullable=False, default="")  # xpath表达式，解析协议类别
    level_xpath = Column(String(500), nullable=False, default="")  # xpath表达式，解析匿名级别
    lastcheck_xpath = Column(String(500), nullable=False, default="")  # xpath表达式，解析最后校验时间
    enable = Column(Integer, nullable=False)  # 激活rule的开关，1为开0为关

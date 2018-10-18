# -*- coding: utf-8 -*-
#寻找Base的所有子类，并在数据库中生成表
from climber.model import engine, loadSession, Base
from climber.model.rules import Rule

Base.metadata.create_all(engine)
#返回数据库会话
session = loadSession()

#实例化一个Rule对象
item=Rule()
item.name="xicidaili"
item.allowed_domains="www.xicidaili.com"
item.start_urls="http://www.xicidaili.com/nn/,http://www.xicidaili.com/wn/"
item.next_page="//div[@class='pagination']/a[@class='next_page']"
item.allow_url="/nn/\d+,/wn/\d+"
item.loop_xpath="//tr[position()>1]"
item.ip_xpath="td[2]/text()"
item.port_xpath="td[3]/text()"
item.location1_xpath="td[4]/a/text()"
item.location2_xpath=""
item.speed_xpath="td[7]/div/@title"
item.lifetime_xpath = "td[9]/text()"
item.type_xpath="td[6]/text()"
item.level_xpath="td[5]/text()"
item.lastcheck_xpath = "td[10]/text()"
item.enable="1"
#添加到数据库
session.add(item)
session.commit()
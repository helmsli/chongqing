# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ChongqingItem(scrapy.Item):
    # define the fields for your item here like:
    # 开奖号码
    winNumberResult = scrapy.Field()
    # 期号
    onesPlaceResult = scrapy.Field()
    # 开奖时间
    tensPlaceResult = scrapy.Field()
    #原始的页面
    lastThreeResult = scrapy.Field()
    pass
#开奖号码对象模型
class WinNumberItem(scrapy.Item):

    # define the fields for your item here like:
    periodNo = scrapy.Field()
    # 开奖时间
    openDate = scrapy.Field()
    # 开奖号码
    firstNumber = scrapy.Field()
    # 期号
    secondNumber = scrapy.Field()
    # 开奖时间
    thirdNumber = scrapy.Field()
    #原始的页面
    fourthNumber = scrapy.Field()

    fifthNumber = scrapy.Field()
    pass

#个位开奖模型
class OnesPlaceItem(scrapy.Item):
    # define the fields for your item here like:
    periodNo = scrapy.Field()
    # 开奖时间
    openDate = scrapy.Field()
    #
    onesPlaceOpenResult = scrapy.Field()
    pass
#十位开奖模型
class TensPlaceItem(scrapy.Item):
    # define the fields for your item here like:
    periodNo = scrapy.Field()
    # 开奖时间
    openDate = scrapy.Field()
    #
    tensPlaceOpenResult = scrapy.Field()
    pass
#十位开奖模型
class LastThreeItem(scrapy.Item):
    # define the fields for your item here like:
    periodNo = scrapy.Field()
    # 开奖时间
    openDate = scrapy.Field()
    #
    lastThreeOpenResult = scrapy.Field()
    pass

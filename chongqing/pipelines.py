# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ChongqingPipeline(object):
    def process_item(self, item, spider):
        '''
        #使用 from_crawler 方法
        @classsmethod
        def from_crawler(self, crawler):
            return cls(crawler)
        #之后就可以正常用了
        logger.info(self.crawler.settings.getint("Customer_Setting"))

        '''
        return item

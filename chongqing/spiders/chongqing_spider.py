# encoding=utf8
import scrapy
from chongqing.items import  ChongqingItem

class ChongqingSpider(scrapy.Spider):
    name = "chongqing"
    allowed_domains = ["caipiao.163.com"]
    start_urls = [
        "http://caipiao.163.com/award/cqssc/"
    ]


    def readTable(self,response):
        chongqingTables = response.xpath(
            '//div[@class="lottery-results"]/table[1]')
        return chongqingTables

    def readWinNumber(self,table,index):
        chongqingTableAlltr = table.xpath(
            '//tr[2]/td[@class="award-winNum"]/text()').extract()
        print(chongqingTableAlltr)


    def readItemFromResponse(self,response):
        item= ChongqingItem();


    def parse(self, response):
        //定义文件名称，保存原始的页面记录
        filename = 'chongqing.txt'
        with open(filename, 'wb') as f:
            f.write(response.body)
        print "*********************"
        # 抓取页面中的表格对象
        chongqingTables = response.xpath(
            '//div[@class="lottery-results"]/table[1]')

        for i in range(2,3):
            print("********************* " +str(i))
            chongqingTableChild = chongqingTables.xpath(
            '//tr[2]/td[@class="start"]').extract()
            print(chongqingTableChild)
            print('55555555555555')
            chongqingTableAlltr = response.xpath('//div[@class="lottery-results"]/table[1]/tr[2]/td[@class="start"]').extract()
            chongqingTableTensPlace = response.xpath(
                '//div[@class="lottery-results"]/table[1]/tr[2]/td[3]/text()').extract()
            chongqingTableOnesPlace = response.xpath(
                '//div[@class="lottery-results"]/table[1]/tr[2]/td[4]/text()').extract()
            chongqingTableLastThree = response.xpath(
                '//div[@class="lottery-results"]/table[1]/tr[2]/td[5]/text()').extract()

            print(chongqingTableAlltr)
            print(chongqingTableTensPlace)
            print(chongqingTableOnesPlace)
            print(chongqingTableLastThree)

            print("############# " + str(i))


            #for chongqingTableTr in chongqingTableAlltr:
                #print(type(chongqingTableTr))
                #print(chongqingTableTr)

        #获取重庆时时彩的信息
        #chongqingTableAlltr = response.xpath('//div[@class="lottery-results"]/table/tr/*').extract()
        print(chongqingTableAlltr)
        with open("result.txt",'wb') as f:

            for chongqingTableTr in chongqingTableAlltr:

                print(type(chongqingTableTr))
                print(chongqingTableTr)

                f.write(chongqingTableTr)
                f.write(" "+'\n')

# encoding=utf8
import scrapy
from chongqing.items import  ChongqingItem
from chongqing.items import  WinNumberItem
from lxml import etree

class ChongqingSpider(scrapy.Spider):
    name = "chongqing"
    allowed_domains = ["caipiao.163.com"]
    start_urls = [
        #"http://caipiao.163.com/award/cqssc/",
        "http://caipiao.163.com/award/cqssc/20181122.html"

    ]

    #读取开奖表格
    def readTable(self,response):
        chongqingTables = response.xpath('//div[@class="lottery-results"]/table[1]')
        return chongqingTables;
    #读取表格的所有开奖记录
    def getWinNumberTd(self,table):
        openResultTd = table.xpath('//tr/td[@data-win-number and @data-period]').extract()
        return openResultTd;
    def getWinNumber(self,winNumberTd):
        #对某一个TR下的TD进行循环
        winTrIndexList=[]
        for winnumberOneTd in winNumberTd:
            winNumberItem = WinNumberItem()
            #将文本winnumberOneTd转换为HTML
            html = etree.fromstring(winnumberOneTd)
            #获取开奖号码,结果为列表
            winNumber = html.xpath(
                '//@data-win-number')
            #print('winnumber:' + '\n')
            #print(type(winNumber))
            #如果列表个数大于0
            if len(winNumber)>0:
                #获取开奖的号码
                winNumbers = winNumber[0]
                winNumberItem['winNumbers']=winNumbers
            #获取开奖期号，结果为列表
            dataPeriod = html.xpath(
                '//@data-period')
            if len(dataPeriod)>0:
                #获取开奖的期号
                winNumberItem['periodNo'] = dataPeriod[0]
            winTrIndexList.append(winNumberItem)
        #print(winTrIndexList)
        #print('after get winnumber tr:')
        return winTrIndexList

        winNumber = winNumberTd.xpath(
            '//@data-win-number')
        #print(winNumber)
        print('winnumber')


    def readItemFromResponse(self,response):
        item= ChongqingItem();


    def parse(self, response):
        chongqingItem =ChongqingItem()
        #定义文件名称，保存原始的页面记录
        filename = 'chongqing.txt'
        with open(filename, 'wb') as f:
            f.write(response.body)
        print "*********************"
        # 抓取页面中的表格对象,得到一个表格的HTML
        chongqingTables = self.readTable(response)
        #获取表格中的所有开奖记录
        getWinNumberTd = self.getWinNumberTd(chongqingTables)
        winNumberList =self.getWinNumber(getWinNumberTd)
        winNumberList.sort(key=lambda winNumberTemp: winNumberTemp['periodNo'], reverse=False)

        chongqingItem['winNumberResult']=winNumberList
        #print(chongqingItem['winNumberResult'])
        yield chongqingItem
        #print(chongqingTables)
        #print(self.readPeriod(chongqingTables,1))

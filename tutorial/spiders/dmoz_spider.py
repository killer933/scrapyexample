import scrapy
import datetime
 
from tutorial.HouseItems import HouseItem

class DmozSpider(scrapy.Spider):
    name = "MySpider"
    allowed_domains = []
    start_urls = ["http://www.cdfgj.gov.cn/SCXX/Default.aspx"]

    def parse(self, response):
        item = HouseItem()
    #    for sel in response.xpath('//table[@class="rightContent"]'/a[@target="_self"]'):
     #       title = sel.xpath('tr/text()').extract()
     #       link = sel.xpath('a/@href').extract()
    #        desc = sel.xpath('text()').extract()
   #         print title, link, desc
        flag = 1
        now = datetime.datetime.now()
        datenow =now.strftime('%Y-%m-%d') 
        weekday = now.weekday()
        for sel in response.xpath('//table[@class="blank"]'):
            if flag==1:
                item['house_type'] = u"\u65b0\u623f"
  
            else:
                item['house_type'] = u"\u4e8c\u624b\u623f"
            flag =2
            for i in range(3,9):
        #    tmp = sel.xpath('tr[5]/td[1]/text()').extract()[0]
                stri = 'tr[' + str(i) + ']'
                item['house_area'] = sel.xpath(stri + '/td[1]/text()').extract()[0].strip().lstrip().rstrip(',')
       #     item['house_area'] = sel.xpath('tr[5]/td[1]/text()').extract()[1]
                item['full_square_meter'] = sel.xpath(stri + '/td[2]/text()').extract()[0].strip().lstrip().rstrip(',')
                item['num'] = sel.xpath(stri + '/td[3]/text()').extract()[0].strip().lstrip().rstrip(',')
                item['square_meter'] = sel.xpath(stri + '/td[4]/text()').extract()[0].strip().lstrip().rstrip(',')
                item['date'] = datenow
                item['weekday'] = weekday + 1
                yield item
#encoding=UTF-8
import scrapy
from cnblogSpider.items import CnblogspiderItem
from scrapy import Selector

class cnblogSpiders(scrapy.Spider):
    name = "cnblog"
    start_urls=['http://www.cnblogs.com/qiyeboy/default.html?page=1']
    allowed_domains=['cnblogs.com']

    def parse(self, response):
        days=response.xpath('.//*[@class="day"]')
        for day in days:
            postTitle=day.xpath('.//*[@class="postTitle"]/a/text()').extract()[0]
            time=day.xpath('.//*[@class="dayTitle"]/a/text()').extract()[0]
            content=day.xpath('.//*[@class="postCon"]/div/text()').extract()[0]
            url=day.xpath('.//*[@class="postTitle"]/a/@href').extract()[0]
            items=CnblogspiderItem(url=url,postTitle=postTitle,time=time,content=content)
            print url,postTitle,time,content
            yield items
            next_paper=Selector(response).re(u'<a href="(\S*)">下一页</a>')
            if next_paper:
                yield scrapy.Request(url=next_paper[0],callback=self.parse)
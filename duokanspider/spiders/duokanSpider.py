# -*- coding: utf-8 -*-

import scrapy

from duokanspider.items import DuokanSpiderItem

class DuokanSpider(scrapy.Spider):
    name = "duokan"
    allowed_domains = ["duokan.com"]
    start_urls = ['http://www.duokan.com/list/6-1-1']

    def parse(self, response):
        #pagenumber = response.xpath('//ul[contains(@id, "bookpage")]//a[contains(@href, "list")]/@href').re(r'.*-(\d*)$')[-1]
        for bookinfo in response.xpath('//li[@class="u-bookitm1 j-bookitm"]'):
            print bookinfo.extract()
            item = DuokanSpiderItem()
            item['bookprice'] = bookinfo.xpath('.//em/text()').extract()
            item['bookdelprice'] = bookinfo.xpath('.//del/text()').extract()
            item['bookid'] = bookinfo.xpath('.//div/a[contains(@href, "book")]/@href').re(r'(\d*)$')[0]
            item['bookname'] = bookinfo.xpath('.//img[@src]/@alt').extract()
            item['bookauthor'] = bookinfo.xpath('.//div[@class="u-author"]/span/text()').extract()
            raw_input(item)
            yield item

        #get next page
        nextpage = response.xpath('//div//a[@class="next "]/@href').re(r'.*-(\d*)$')
        print nextpage
        if nextpage:
            nexturl = 'http://www.duokan.com/list/6-1-%s'%int(nextpage[0])
            yield scrapy.Request(nexturl, callback=self.parse)

# -*- coding: utf-8 -*-
import scrapy
from ..items import QsbkDemoItem


class QsbkspiderSpider(scrapy.Spider):
    name = 'QsbkSpider'
    # allowed_domains = ['//www.qiushibaike.com/']
    allowed_domains = ['qiushibaike.com/']
    start_urls = ['https://www.qiushibaike.com/text/page/1/']
    base_domain = "https://www.qiushibaike.com"

    def parse(self, response):
        contentLefts = response.xpath("//div[@class='article block untagged mb15 typs_hot']")
        for x in contentLefts:
            author = x.xpath(".//h2/text()").get().strip()
            content = x.xpath(".//div[@class='content']//span//text()").getall()
            content = "".join(content).strip()
            item = QsbkDemoItem(author=author, content=content)
            yield item
        next_url = response.xpath("//ul[@class='pagination']/li[last()]/a/@href").get()
        print(next_url)
        if not next_url:
            return
        else:
            print(self.base_domain+next_url)
            yield scrapy.Request(self.base_domain+next_url, callback=self.parse, dont_filter=True)

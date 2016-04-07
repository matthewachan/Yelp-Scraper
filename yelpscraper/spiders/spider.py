# -*- coding: utf-8 -*-
"""
Created on Thu Apr 07 00:24:50 2016

@author: Matt
"""

import scrapy
from yelpscraper.items import YelpItem

class YelpSpider(scrapy.Spider):
    name = "yelp"
    allowed_domains = ["yelp.com"]
    start_urls = [
        "http://www.yelp.com/search?find_desc=Burgers&find_loc=Los+Angeles,+CA"
    ]
            
    def __init__(self):
        self.i = 0 # counter to limit number of results
    
    def parse(self,response):
        if self.i < 10:
            for sel in response.xpath("//li[@class='regular-search-result']"):
                item = YelpItem()
                item["name"] = sel.xpath(".//a[@class='biz-name']/span/text()").extract()
                item["stars"]= sel.xpath(".//i[contains(@class,'star-img')]/img/@alt").extract()
                item["reviews"]= sel.xpath(".//span[@class='review-count rating-qualifier']/text()").extract()[0].strip()
                item["street_address1"]= sel.xpath(".//address/text()[1]").extract()[0].strip()
                item["street_address2"]= sel.xpath(".//address/text()[2]").extract()[0].strip()
                link = sel.xpath(".//a[@class='biz-name']/@href")
                if link:
                    url = response.urljoin(link[0].extract())
                    request = scrapy.Request(url, self.parse_quote)
                    request.meta['item'] = item
                    yield request
#                yield item # we don't want the item to be returned until we get the top-quoted item
                
            next_page = response.xpath("//a[@class='u-decoration-none next pagination-links_anchor']/@href")
            if next_page:
                url = response.urljoin(next_page[0].extract())
                yield scrapy.Request(url, self.parse)
        self.i +=1
        
    def parse_quote(self,response):
        x = response.xpath("//a[@class='ngram']/text()")
        item = response.meta['item']
        item["top_item"] = x[0].extract()
        return item
        
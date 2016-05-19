# !/usr/bin/python
# -*-coding:utf-8-*-

import scrapy
import traceback
from firstspider.items import Firstitem
from scrapy.spider import Spider
from scrapy.contrib.spiders import Rule
from scrapy.http import Request
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy_splash import SplashRequest

class First(Spider):
    name = 'first'
    allow_domain = ["aisec.cn"]
    start_urls = ["http://demo.aisec.cn/demo/aisec/"]
    rule = (
        Rule(LinkExtractor(), callback='parse', follow=True),
    )
    Link = LinkExtractor(allow_domains="aisec.cn")
    JsLink = LinkExtractor(allow_domains="aisec.cn", tags=('script'), attrs=('src',))
    ImgLink = LinkExtractor(allow_domains="aisec.cn", tags=('img'), attrs=('src',))

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, endpoint='render.html', args={"html": 1}
                                 )

    def parse(self, response):
        try:
            Item = Firstitem()
            links = self.Link.extract_links(response)
            jslinks = self.JsLink.extract_links(response)
            imglinks = self.ImgLink.extract_links(response)
            Item['link'] = response.url
            ls = []
            Item['jslink'] = ls
            for link in jslinks:
                Item['jslink'].append(link.url)
            Item['imglink'] = ls
            for link in imglinks:
                Item['imglink'].append(link.url)
            yield Item
            for link in links:
                url = link.url
                yield SplashRequest(url=url, callback=self.parse, endpoint='render.html', args={"html":1})
        except:
            traceback.print_exc()

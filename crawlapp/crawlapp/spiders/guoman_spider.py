import uuid
import time
import scrapy
from crawlapp.items import CrawlappItem


class GuomanSpider(scrapy.Spider):
    name = "guoman"
    start_urls = ['http://acg.178.com/list/guoman/index.html']

    def parse(self, response):
        for href in response.css('li.ui-repeater-item p.textbox a::attr(href)').extract():
            yield scrapy.Request(url=href, callback=self.parse_detail)

    def parse_detail(self, response):
        item = CrawlappItem()

        create_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        classify = '国漫'

        def uuid_without():
            s_uuid = str(uuid.uuid4())
            l_uuid = s_uuid.split('-')
            s_uuid = ''.join(l_uuid)

            return s_uuid

        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        item['uuid'] = uuid_without()
        item['classify'] = classify
        item['create_date'] = create_date
        item['title'] = extract_with_css('div.ui-rt-border h1.artical-title::text')
        item['author'] = extract_with_css('div.author span.atr::text')[3:]
        item['web_time'] = extract_with_css('div.author span.time::text')
        item['content'] = extract_with_css('div.artical-content p::text')
        # item['browse'] = 0
        # item['love'] = 0
        # print(item)

        yield item

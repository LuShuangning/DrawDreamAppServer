import uuid
import time
import scrapy
from crawlapp.items import CrawlappItem


class GuomanSpider(scrapy.Spider):
    name = "guoman"
    start_urls = ['http://acg.178.com/list/guoman/index.html']

    def parse(self, response):
        href_list = response.css('li.ui-repeater-item p.textbox a::attr(href)').extract()
        img_list = response.css('li.ui-repeater-item div.imgbox a img::attr(src)').extract()
        count = 0

        for href in href_list:
            item = CrawlappItem()
            item['cover_img'] = img_list[count]
            count += 1
            yield scrapy.Request(url=href, callback=self.parse_detail, meta={'item': item})

    # 进入链接解析具体的内容
    def parse_detail(self, response):
        item = response.meta['item']
        create_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        classify = '国漫'

        # uuid转换去掉'-'
        def uuid_without():
            s_uuid = str(uuid.uuid4())
            l_uuid = s_uuid.split('-')
            s_uuid = ''.join(l_uuid)

            return s_uuid

        # 获取相应节点内容
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

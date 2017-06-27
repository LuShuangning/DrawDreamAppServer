# -*- coding: utf-8 -*-

import codecs
import json

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class CrawlappPipeline(object):
    # def __init__(self):
        # self.file = open('data.json', 'wb')
        # self.file = codecs.open(
        #     'guoman.txt', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        file = codecs.open(str(item['title']), 'w', encoding='utf-8')
        line = json.dumps(dict(item['content']), ensure_ascii=False) + "\n"
        file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()


class StorePipeline(object):

    # pipeline调用
    def process_item(self, item, spider):

        connection = pymysql.connect(
            user='root',
            passwd='135569',
            db='draw_dream',
            host='127.0.0.1',
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor)

        sql = """INSERT INTO news_detail 
(nede_id, nede_classify, nede_title, nede_author, nede_web_time, nede_content, nede_create_date) 
VALUES(%s, %s, %s, %s, %s, %s, %s) """

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, (
                    item['uuid'],
                    item['classify'],
                    item['title'],
                    item['author'],
                    item['web_time'],
                    item['content'],
                    item['create_date'],
                )
                                    )
                connection.commit()
        finally:
            connection.close()

        return item

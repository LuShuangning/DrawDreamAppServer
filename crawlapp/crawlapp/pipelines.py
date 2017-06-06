# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class CrawlappPipeline(object):

    def process_item(self, item, spider):
        return item


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

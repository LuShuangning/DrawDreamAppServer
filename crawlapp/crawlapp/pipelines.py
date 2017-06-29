# -*- coding: utf-8 -*-

import codecs
import simplejson

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class CrawlappPipeline(object):
    # def __init__(self):
    #     self.file = codecs.open(
    #         'guoman.txt', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        # write content in local file
        file = codecs.open(str('/home/file_server/file/'
                               + item['title'][0:10] + '.html'), 'w', encoding='utf-8')
        # file = codecs.open(str('/home/sunnylu/Documents/scrapy/'
        #                        + item['title'][0:10] + '.html'), 'w', encoding='utf-8')
        try:

            line = simplejson.dumps(item['content'], ensure_ascii=False).replace('\\n', '')[2:-2]
            # print('*********************************************' + str(item['cover_img']))
            file.write(line)
        finally:
            file.close()
        return item

    # def process_item(self, item, spider):
    #     line = json.dumps(dict(item), ensure_ascii=False) + "\n"
    #     self.file.write(line)
    #     return item
    #
    # def spider_closed(self, spider):
    #     self.file.close()


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
(nede_id, nede_classify_id, nede_title, 
nede_author, nede_web_time, nede_content, 
nede_create_date, nede_cover_img, nede_browse, nede_love) 
VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, (
                    item['uuid'],
                    item['classify'],
                    item['title'],
                    item['author'],
                    item['web_time'],
                    item['content_url'] + '.html',
                    item['create_date'],
                    item['cover_img'],
                    0,
                    0
                )
                                    )
                connection.commit()
        finally:
            connection.close()

        return item

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import MySQLdb 
import MySQLdb.cursors

from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi

class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonWithEncodingPipeline(object):
	def __init__(self):
		self.file = codecs.open('article.json', 'w', encoding='utf8')

	def process_item(self, item, spider):
		lines = json.dump(dict(item), ensure_ascii=True) + "\n"
		print('XXXXXXXXXXX', item)
		self.file.write(lines)
		return item

	def spider_closed(self, spider):
		self.file.close()

class JsonExporterPipeline(object):
	def __init__(self):
		self.file = open('article.json', 'wb')
		self.exporter = JsonItemExporter(self.file, encoding='utf8', ensure_ascii=True)
		self.exporter.start_exporting()

	def close_spider(self,spider):
		self.exporter.finish_exporting()
		self.file.close()

	def process_item(self, item, spider):
		self.exporter.export_item(item)
		return item

class MysqlPipeline(object):
	def __init__(self):
		self.conn = MySQLdb.connect('127.0.0.1', 'root', 'yangzhikai668', 'spider', charset='utf8')
		self.cursor = self.conn.cursor()

	def process_item(self, item):
		inser_sql = """
			insert into post(
				title,
			    create_date,
			    url_object_id
			    url, 
			    praise_numbers,
			    favor_numbers,
			    comment_numbers,
			    tags,
			) values (
				%s, %s, %s, %s,
				%s, %s, %s, %s
			)
		"""
		# synchronous version:
		self.cursor.execute(inser_sql, (item['title'],...))
		self.conn.commit()

		return item

class MysqlTwistedPipeline(object):
	"""
	asychronous version
	"""
	def __init__(self, dbpool):
		self.dbpool = dbpool
		
	@classmethod
	def from_settings(cls, settings):
		"""
		can be called by spyder to load setting's params
		"""
		db_params = dict(
			host=settings['MYSQL_HOST'],
			db=settings['MYSQL_DBNAME'],
			user=settings['MYSQL_USER'],
			passwd=settings['MYSQL_PASSWORD'],
			charset='utf8',
			cursorclass=MySQLdb.cursors.DictCursor,
			use_unicode=True, 
		)
		dbpoll = adbapi.ConnectionPool('MySQLdb', **db_params)

		return cls(dbpoll)

	def process_item(self, item, spider):
		query = self.dbpool.runInteraction(self.do_insert, item)
		query.addErrback(self.handle_error) # handle errors
		return item

	def do_insert(self, cursor, item):
		inser_sql = """
						insert into post(title, 
										create_date, 
										url_object_id, 
										url, 
										praise_numbers, 
										favor_numbers, 
										comment_numbers, 
										tags) 
						values(%s, %s, %s, %s,%s, %s, %s, %s)
					"""
		cursor.execute(inser_sql, (item['title'],
								item['create_date'],
								item['url_object_id'],
								item['url'],
								item['praise_num'],
								item['favor_num'],
								item['comment_num'],
								item['tags']))

	def handle_error(self, failure):
		print(failure)


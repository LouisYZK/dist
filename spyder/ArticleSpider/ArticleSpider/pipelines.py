# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json

from scrapy.exporters import JsonItemExporter

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

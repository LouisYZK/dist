# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy.loader.processors import MapCompose

class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

def add_prefix(value):
	return value + 'YZK_SPIDER'
	
class JobboleArticleItem(scrapy.Item):
	title = scrapy.Field(
		input_processor = MapCompose(add_prefix)
	)
	create_date = scrapy.Field()
	url = scrapy.Field()
	url_object_id = scrapy.Field()
	praise_num = scrapy.Field()
	favor_num = scrapy.Field()
	comment_num = scrapy.Field()
	tags = scrapy.Field()

# -*- coding: utf-8 -*-
import scrapy
import re
import datetime 

from scrapy.http import Request
from urllib import parse 

from ArticleSpider.items import JobboleArticleItem
from ArticleSpider.utils.common import get_md5

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    # start_urls = ['http://blog.jobbole.com/']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        1. Get all the article's url on one article list page and apply it to scrapy;
        2. Get the next article urls page;
        """
        post_urls = response.css(".archive-title::attr(href)").extract()
        for url in post_urls:
            yield Request(parse.urljoin(response.url, url), callback=self.parse_article)

        next_page =  response.css(".next.page-numbers::attr(href)").extract_first("")
        # if next_page:
        #     yield Request(next_page, self.parse)
    
    def parse_article(self, response):
        # title = response.css(".entry-header h1::text").extract()[0]  CSS-selector写法
        
        # time = response.xpath('//*[@id="post-114638"]/div[2]/p/text()').extract()[0].strip().replace(' ·','')
        # praise_num = int(response.xpath('//*[@id="post-114638"]/div[3]/div[5]/span[1]/h10/text()').extract()[0])
        # favor_num = response.xpath('//*[@id="post-114638"]/div[3]/div[5]/span[2]/text()').extract()[0].strip()
        # match_info = re.match(r'.*(\d+).*', favor_num)
        # if match_info:
        #     favor_num = match_info.group(1) 
        # comment_num = response.xpath('//*[@id="post-114638"]/div[3]/div[5]/a/span/text()').extract()[0].strip()
        # match_info = re.match(r'.*(\d+).*', favor_num)
        # if match_info:
        #     comment_num - match_info.group(1)
        # tags = response.xpath('//*[@id="post-114638"]/div[2]/p/a/text()').extract()
        # tags = ','.join(tags)
        # print(tags)
        title = response.xpath("//*[@class='entry-header']/h1/text()").extract()[0].strip()

        time =  response.css(".entry-meta-hide-on-mobile::text")[0].extract().strip().replace(' ·','')
        try:
            create_date = datetime.datetime.strptime(time, "%Y/%m/%d").date()
        except Exception as e:
            create_date = datetime.datetime.now().date()

        tags = response.css(".entry-meta-hide-on-mobile a::text").extract()
        for tag in tags:
            if not re.match(r'\D.*', tag.strip()): 
                tags.remove(tag)
        tags = ','.join(tags)

        article_data = response.css(".post-adds span")
        try:
            praise_num = self.extratc_num(article_data[0].css("h10::text").extract()[0])
            favor_num = self.extratc_num(response.css(".post-adds span::text").extract()[2])
            comment_num = self.extratc_num(response.css(".post-adds span::text").extract()[3])
        except Exception as e:
            praise_num, favor_num, comment_num = None, None, None
            print(e)

        article_item = JobboleArticleItem()
        article_item['title'] = title 
        article_item['create_date'] = create_date
        article_item['tags'] = tags
        article_item['url'] = response.url
        article_item['url_object_id'] = get_md5(response.url)
        article_item['praise_num'] = praise_num
        article_item['favor_num'] = favor_num
        article_item['comment_num'] = comment_num

        yield article_item # Very Important!!

    def extratc_num(self, string):
        match_info = re.match(r'.*(\d).*', string)
        if match_info:
            return int(match_info.group(1))
        else:
            return 0



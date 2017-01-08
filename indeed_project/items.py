# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IndeedProjectItem(scrapy.Item):
    job_title = scrapy.Field()
    job_url = scrapy.Field()
    company = scrapy.Field()
    location = scrapy.Field()
    summary = scrapy.Field()
    date = scrapy.Field()
    create_date = scrapy.Field()

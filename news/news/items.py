# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from datetime import datetime
from scrapy.loader.processors import MapCompose, TakeFirst, Join


class ArticleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field(
        output_processor=TakeFirst()
    )
    headline = scrapy.Field(    
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    authors = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=Join('-')
    )
    text = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=Join('\n')
    )
    date = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )

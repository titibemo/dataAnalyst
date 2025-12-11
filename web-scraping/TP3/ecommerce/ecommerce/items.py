# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EcommerceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class BookItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    rating = scrapy.Field()
    availability = scrapy.Field()
    picture = scrapy.Field()

class CategoryItem(scrapy.Item):
    category = scrapy.Field()

class PageCategoryItem(scrapy.Item):
    titre = scrapy.Field()

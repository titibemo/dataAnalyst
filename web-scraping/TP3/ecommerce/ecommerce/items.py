# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class BookItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    rating = scrapy.Field()
    description = scrapy.Field()
    category = scrapy.Field()
    number_review = scrapy.Field()
    picture = scrapy.Field()

class CategoryItem(scrapy.Item):
    category_title = scrapy.Field()
    category_url = scrapy.Field()

class PageCategoryItem(scrapy.Item):
    titre = scrapy.Field()

import scrapy
import logging
import re
from bookstore.items import BookItem


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]
    custom_settings = {
        "DEPTH_LIMIT": 2
    }

    def parse(self, response):
        for quote in response.css('section .row li'):
            item = BookItem()
            item['title'] = quote.css('.product_pod h3 a::text').get()
            item['price'] = quote.css('.price_color::text').re_first(r'\d+\.\d{2}')
            item['rating'] = quote.css('.product_pod p::attr(class)').get().split()[1]
            item['availability'] = quote.css('.instock.availability ::text').getall()[-1].strip()
            yield item
            
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
import scrapy
import scrapy
import logging
import re
from ecommerce.items import BookItem, CategoryItem

# logger = logging.getLogger("mycustomlogger")
# logging.basicConfig(filename='log/rapport.log', encoding='utf-8', level=logging.DEBUG)

# class BookSpider(scrapy.Spider):
#     name = "book"
#     allowed_domains = ["books.toscrape.com"]
#     start_urls = ["https://books.toscrape.com"]

#     def parse(self, response):
#         logger.info("============= LOGGING =============")

#         # for quote in response.css('section .row li'):
#         #     item = BookItem()
#         #     item['title'] = quote.css('.product_pod h3 a::attr(title)').get()
#         #     item['price'] = quote.css('.price_color::text').re_first(r'\d+\.\d{2}') # https://docs.scrapy.org/en/latest/topics/selectors.html#using-selectors-with-regular-expressions
#         #     item['rating'] = quote.css('.product_pod p::attr(class)').get().split()[1] # https://docs.scrapy.org/en/latest/topics/selectors.html
#         #     item['availability'] = quote.css('.instock.availability ::text').getall()[-1].strip()
#         #     #sauvegarder le fichier dans le dossier images
            
#         #     yield item

#         # 1. **Spider multi-niveaux**
#         # - Page d'accueil → Catégories
#         categories = []

#         for category in response.css('div.side_categories ul li ul li'):
#             item = CategoryItem()
#             item['category'] = category.css('a::attr(href)').get()
#             #yield item
        
#         # next_page = response.css("li.next a::attr(href)").get()
#         response.follow(item['category'], callback=self.parse_category(response))

#     def parse_category(response):

#         for t in response.css('div.side_categories ul li ul li'):
#             item = CategoryItem()
#             item['titre'] = t.css('h1::text').get()
#             yield item
                 



#         # 2. **Spider multi-niveaux**
#         # - Page d'accueil → Catégories → Livres


class BookSpider(scrapy.Spider):
    name = "book"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]
    custom_settings = {
        "DEPTH_LIMIT": 2
    }

    def parse(self, response):

        # 1. Récupérer les catégories
        for category in response.css('div.side_categories ul li ul li a'):
            url = response.urljoin(category.attrib['href'])
            yield response.follow(url, callback=self.parse_category)

    def parse_category(self, response):

        # Titre de la catégorie
        title = response.css('div.page-header h1::text').get()

        # Suivi des livres de la catégorie
        for book in response.css('h3 a'):
            url = response.urljoin(book.attrib['href'])
            # On passe la catégorie dans les meta (utile pour l'item final)
            yield response.follow(url, callback=self.parse_book_category, meta={'category': title})

        # Pagination
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(response.urljoin(next_page), callback=self.parse_category)

    def parse_book_category(self, response):

        item = BookItem()

        item['title'] = response.css('h1::text').get()
        item['price'] = response.css('.price_color::text').re_first(r'\d+\.\d{2}')
        item['rating'] = response.css('p.star-rating::attr(class)').get().split()[-1]
        item['description'] = response.css('#product_description ~ p::text').get()
        item['number_review'] = response.css('.instock.availability::text').re_first(r'\d+')
        item['category'] = response.meta.get('category')

        yield item

import scrapy
import scrapy
from ecommerce.items import BookItem, CategoryItem

class BookSpider(scrapy.Spider):
    name = "book"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]
    custom_settings = {
        "DEPTH_LIMIT": 2
    }

    def parse(self, response):

        # 1. Récupérer les catégories
        for category in response.css('div.side_categories ul li ul li a')[:2]:
            url = response.urljoin(category.attrib['href'])
            yield response.follow(url, callback=self.parse_category)

    def parse_category(self, response):

        # Titre de la catégorie
        title = response.css('div.page-header h1::text').get()

        yield CategoryItem(
            category_title=title,
            category_url=response.url
        )

        # Suivi des livres de la catégorie
        for book in response.css('h3 a')[:2]:
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

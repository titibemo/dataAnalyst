# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# Useful for handling different item types with a single interface
import json
import os
from datetime import datetime
import logging

from ecommerce.items import CategoryItem, BookItem
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

from openpyxl import Workbook

os.makedirs("log", exist_ok=True)
logger = logging.getLogger("PIPELINE_SCRAPY")
# logging.basicConfig(filename='log/rapport.log', encoding='utf-8', level=logging.INFO)

class PriceConversionPipeline:
    """
    Pipeline to convert prices to float.

    This pipeline is mainly intended for "BookItem" type items
    (scraped from a book site with a 'price' field).

    Example transformation:
    - "£51.77" -> 51.77 (float)

    If the 'price' field is missing or invalid, the item is returned as-is.
    """

    def process_item(self, item, spider):
        logger.info("=" * 50)
        logger.info("============= PriceConversionPipeline ACTIVATED  =============")
        logger.info("=" * 50)

        adapter = ItemAdapter(item)

        if adapter.get("price"):
            price_text = str(adapter["price"]).strip()

            # Remove all non-numeric characters (except the dot)
            cleaned = "".join(ch for ch in price_text if ch.isdigit() or ch == ".")

            try:
                adapter["price"] = float(cleaned)
            except ValueError:
                # If conversion fails, leave the price as-is
                adapter["price"] = adapter["price"]

        return item


class DuplicatesPipeline:
    """
    Pipeline to remove duplicate items.

    This pipeline is suitable for quotes:
    - A set "texts_seen" keeps track of texts already encountered.
    - If a text is already present, the item is ignored (DropItem).

    It illustrates duplicate detection and filtering.
    """

    def __init__(self):
        # Set of texts already seen
        self.texts_seen = set()

    def process_item(self, item, spider):
        logger.info("=" * 50)
        logger.info("============= DuplicatesPipeline ACTIVATED  =============")
        logger.info("=" * 50)

        adapter = ItemAdapter(item)

        # The "text" field is used as the deduplication key
        text = adapter.get("text")

        if text is None:
            # If no text is available, keep the item
            return item

        if text in self.texts_seen:
            # Ignore the item because it has already been seen
            raise DropItem(f"Duplicate detected for the quote: {text!r}")

        # Record the text as already seen
        self.texts_seen.add(text)
        return item


class ExcelWriterPipeline:
    """
    Pipeline to save items into an Excel file.

    This pipeline is suitable for "CategoryItem" and "BookItem" types.
    """

    def open_spider(self, spider):
        logger.info("=" * 50)
        logger.info("============= EXCELWRITERPIPELINE ACTIVATED  =============")
        logger.info("=" * 50)

        # Create outputs folder
        os.makedirs("outputs/excel", exist_ok=True)
        self.file_path = os.path.join("outputs/excel", "books.xlsx")

        # Create a new Excel workbook
        self.wb = Workbook()

        # Categories sheet
        logger.info("=" * 50)
        logger.info("============= EXCELWRITERPIPELINE CREATE SHEET CATEGORIES  =============")
        logger.info("=" * 50)

        self.sheet_categories = self.wb.active
        self.sheet_categories.title = "categories"
        self.sheet_categories.append(["category_title", "category_url"])

        # Books sheet
        logger.info("=" * 50)
        logger.info("============= EXCELWRITERPIPELINE CREATE SHEET BOOKS  =============")
        logger.info("=" * 50)
        self.sheet_books = self.wb.create_sheet("books")
        self.sheet_books.append(["title", "price", "rating", "description", "number_review", "category"])

    def close_spider(self, spider):
        self.wb.save(self.file_path)

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # If it's a category → write to categories sheet
        if isinstance(item, CategoryItem):
            self.sheet_categories.append([
                adapter.get("category_title"),
                adapter.get("category_url")
            ])
            return item

        # If it's a book → write to books sheet
        if isinstance(item, BookItem):
            self.sheet_books.append([
                adapter.get("title"),
                adapter.get("price"),
                adapter.get("rating"),
                adapter.get("description"),
                adapter.get("number_review"),
                adapter.get("category")
            ])
            return item

        # Any other item → ignore
        return item


class JsonArchivePipeline:
    """
    Pipeline that saves all items into a JSON file.
    Useful for archiving or backup.
    """

    def open_spider(self, spider):
        os.makedirs("outputs/json", exist_ok=True)
        self.file_path = os.path.join("outputs/json", f"archive_{datetime.now().strftime('%Y%m%d%H%M%S')}.json")
        self.file = open(self.file_path, "w", encoding="utf-8")
        self.items = []

    def close_spider(self, spider):
        # Final write of all items into a formatted JSON file
        json.dump(self.items, self.file, indent=2, ensure_ascii=False)
        self.file.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        self.items.append(adapter.asdict())
        return item

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
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
#logging.basicConfig(filename='log/rapport.log', encoding='utf-8', level=logging.INFO)

class PriceConversionPipeline:
    """
    Pipeline de conversion des prix en float.

    Ce pipeline est principalement destiné aux Items de type "BookItem"
    (extraction depuis un site de livres avec un champ 'price').

    Exemple de transformation :
    - "£51.77" -> 51.77 (float)

    Si le champ 'price' n'existe pas ou n'est pas exploitable,
    l'item est renvoyé tel quel.
    """

    def process_item(self, item, spider):
        logger.info("=" * 50)
        logger.info("============= PriceConversionPipeline ACTIVATED  =============")
        logger.info("=" * 50)

        adapter = ItemAdapter(item)

        if adapter.get("price"):
            price_text = str(adapter["price"]).strip()

            # Suppression de tous les caractères non numériques (sauf le point).
            cleaned = "".join(ch for ch in price_text if ch.isdigit() or ch == ".")

            try:
                adapter["price"] = float(cleaned)
            except ValueError:
                # En cas d'échec de conversion, le prix est laissé tel quel.
                adapter["price"] = adapter["price"]

        return item


class DuplicatesPipeline:
    """
    Pipeline de suppression des doublons.

    Ce pipeline est adapté aux citations :
    - Un ensemble "ids_seen" conserve les textes déjà rencontrés.
    - Si un texte est déjà présent, l'item est ignoré (DropItem).

    Il illustre le comportement décrit dans le cours :
    détection et filtrage des doublons.
    """

    def __init__(self):
        # Ensemble des textes déjà vus.
        self.texts_seen = set()

    def process_item(self, item, spider):
        logger.info("=" * 50)
        logger.info("============= DuplicatesPipeline ACTIVATED  =============")
        logger.info("=" * 50)

        adapter = ItemAdapter(item)

        # Le champ "text" est utilisé comme clé de déduplication.
        text = adapter.get("text")

        if text is None:
            # Si aucun texte n'est disponible, l'item est conservé.
            return item

        if text in self.texts_seen:
            # L'item est ignoré car déjà rencontré.
            raise DropItem(f"Doublon détecté pour la citation : {text!r}")

        # Enregistrement du texte comme déjà vu.
        self.texts_seen.add(text)
        return item
    
class ExcelWriterPipeline:
    """"
    Pipeline d'enregistrement des items dans un fichier Excel.

    Ce pipeline est adapté aux Items de type "CategoryItem" et "BookItem".
    """
    

    def open_spider(self, spider):
        logger.info("=" * 50)
        logger.info("============= EXCELWRITERPIPELINE ACTIVATED  =============")
        logger.info("=" * 50)

        # Dossier outputs
        os.makedirs("outputs/excel", exist_ok=True)
        self.file_path = os.path.join("outputs/excel", "books.xlsx")

        # Nouveau fichier Excel
        self.wb = Workbook()

        # Feuille catégories
        logger.info("=" * 50)
        logger.info("============= EXCELWRITERPIPELINE CREATE SHEET CATEGORIES  =============")
        logger.info("=" * 50)

        self.sheet_categories = self.wb.active
        self.sheet_categories.title = "categories"
        self.sheet_categories.append(["category_title", "category_url"])

        # Feuille livres
        logger.info("=" * 50)
        logger.info("============= EXCELWRITERPIPELINE CREATE SHEET BOOKS  =============")
        logger.info("=" * 50)
        self.sheet_books = self.wb.create_sheet("books")
        self.sheet_books.append(["title", "price", "rating", "description", "number_review", "category"])

    def close_spider(self, spider):
        self.wb.save(self.file_path)

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Si c’est une catégorie → feuille categories
        if isinstance(item, CategoryItem):
            self.sheet_categories.append([
                adapter.get("category_title"),
                adapter.get("category_url")
            ])
            return item
        
        # Si c’est un livre → feuille books
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

        # Tout autre item → ignoré
        return item

import os
import json
from itemadapter import ItemAdapter

class JsonArchivePipeline:
    """
    Pipeline qui sauvegarde tous les items dans un fichier JSON.
    Utile pour archivage ou backup.
    """

    def open_spider(self, spider):
        os.makedirs("outputs/json", exist_ok=True)
        self.file_path = os.path.join("outputs/json", f"archive_{datetime.now().strftime('%Y%m%d%H%M%S')}.json")

        #self.file_path = os.path.join("outputs", "archive.json")
        self.file = open(self.file_path, "w", encoding="utf-8")
        self.items = []

    def close_spider(self, spider):
        # Écriture finale de tous les items dans un JSON formaté
        json.dump(self.items, self.file, indent=2, ensure_ascii=False)
        self.file.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        self.items.append(adapter.asdict())
        return item

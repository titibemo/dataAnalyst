# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from itemadapter import ItemAdapter
import json
import os

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class EcommercePipeline:
    def process_item(self, item, spider):
        return item

class JsonWriterPipeline:
    """
    Pipeline de sauvegarde des items dans un fichier JSON.

    Fonctionnement :
    - open_spider : ouverture du fichier et initialisation d'une liste tampon
    - process_item : ajout de chaque item dans la liste
    - close_spider : écriture de tous les items dans le fichier JSON

    Ce pipeline illustre la logique présentée dans le cours :
    sauvegarde en JSON via open_spider / close_spider.
    """

    def open_spider(self, spider):
        # Création du dossier "outputs" si nécessaire.
        os.makedirs("outputs", exist_ok=True)

        # Ouverture du fichier en écriture, encodage UTF-8.
        self.file_path = os.path.join("outputs", "quotes_pipelines.json")
        self.file = open(self.file_path, "w", encoding="utf-8")

        # Liste utilisée comme tampon pour accumuler les items.
        self.items = []

    def close_spider(self, spider):
        # Écriture de la liste complète dans le fichier JSON.
        json.dump(self.items, self.file, indent=2, ensure_ascii=False)
        self.file.close()

    def process_item(self, item, spider):
        # Conversion de l'item (Item ou dict) en dict standard.
        adapter = ItemAdapter(item)
        self.items.append(adapter.asdict())
        return item


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


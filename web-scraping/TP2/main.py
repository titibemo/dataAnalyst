## TP 2 - Scraper multi-pages

# **Objectif** : Scraper plusieurs pages avec pagination

# **Site** : http://quotes.toscrape.com

# **Mission**
# Créer un scraper complet qui :
# 1. Détecte automatiquement le nombre de pages
# 2. Scrape toutes les pages (jusqu'à 10 max)
# 3. Pour chaque citation, extrait :
#    - Texte
#    - Auteur
#    - Tags
#    - URL de l'auteur
# 4. Crée un fichier Excel avec 3 feuilles :
#    - "Citations" : Toutes les citations
#    - "Auteurs" : Liste unique des auteurs avec nb de citations
#    - "Tags" : Liste des tags avec fréquence
# 5. Génère des statistiques :
#    - Top 5 auteurs les plus cités
#    - Top 10 tags les plus utilisés
#    - Longueur moyenne des citations

# **Contraintes**
# - Code modulaire (fonctions)
# - Gestion d'erreurs complète
# - Logging
# - Respect du délai entre requêtes

import os
from dotenv import load_dotenv
from logger import setup_logger

import datetime as dt
from extract.extract import get_link_next_pages, request_page
load_dotenv()

BASE_URL = os.getenv('BASE_URL')

def main(logger):
    logger.info(f"Scraping {BASE_URL}")
    pagination_link = get_link_next_pages(logger)
    request_page(logger, scrape_many_pages=True, nbres_pages_to_scrape=3, pagination_link=pagination_link)

if __name__ == "__main__":
    logger = setup_logger('TP2')
    main(logger)
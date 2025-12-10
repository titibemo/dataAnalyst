import requests
import os
import time
from bs4 import BeautifulSoup
from load.load import load_excel
from transform.transform import transforms_data
from dotenv import load_dotenv
load_dotenv()

BASE_URL = os.getenv('BASE_URL')

def extrac_citation(soup):
    quotes_citations = []
    quotes_authors = []
    quotes_tags = []
    try:
        quotes_class: list = soup.select('.quote')

        if not quotes_class:
            raise Exception("No quotes found")
        
        for quote in quotes_class:
            quotes_citations.append(quote.select('.text')[0].text)
            quotes_authors.append(quote.select('.author')[0].text)
            tags = []
            all_tags = quote.select('.tags a')
            for tag in all_tags:
                tags.append(tag.get_text(strip=True, separator=", "))
            quotes_tags.extend(tags)

        return quotes_citations, quotes_authors, quotes_tags
    
    except Exception as e:
        print(e)

def get_link_next_pages(logger, soup=None):
    logger.info(f"EXTRACTION DES LIENS DE PAGES NEXT")
    if soup:
        pagination = soup.select('.pager .next a')[0]['href']
        print('pagination', pagination)
        return pagination
    else:
        soup = request_page(logger)
        pagination = soup.select('.pager .next a')[0]['href']
        return pagination
    
def request_page(logger, scrape_many_pages=False, nbres_pages_to_scrape=2, pagination_link=None):
    if scrape_many_pages:
        quotes_citations = []
        quotes_authors = []
        quotes_tags = []

        number_pages = 1
        while number_pages <= nbres_pages_to_scrape:
            try:
                if number_pages == 1:
                    pagination_link = "/page/1"
                logger.info(f"MULTIPLE SCRAPING - APPEL DE LA PAGE: {BASE_URL}{pagination_link} - page-{number_pages}")

                response = requests.get(f'{BASE_URL}{pagination_link}')
                response.raise_for_status()
                soup = BeautifulSoup(response.text, features="lxml")

                extract_quotes_citation, extract_quotes_authors, extract_quotes_tags = extrac_citation(soup)
                quotes_citations.extend(extract_quotes_citation)
                quotes_authors.extend(extract_quotes_authors)
                quotes_tags.extend(extract_quotes_tags)
                number_pages += 1
                pagination_link = get_link_next_pages(logger, soup)

                time.sleep(1)
            except Exception:
                logger.warning(f"MULTIPLE SCRAPING - PLUS DE PAGE DISPO {BASE_URL} - page-{number_pages}")
                break
            finally:
                logger.info(f" ====== MULTIPLE SCRAPING - FIN DU MULTIPLE SCRAPING ====")
                df_citations, df_authors, df_tags = transforms_data(logger, quotes_citations, quotes_authors, quotes_tags)
                load_excel(logger, df_citations, df_authors, df_tags)
    
    else:
        logger.info(f"APPEL DE LA PAGE: {BASE_URL}")
        response = requests.get(f'{BASE_URL}')
        response.raise_for_status()
        soup = BeautifulSoup(response.text, features="lxml")
        return soup

def get_link_next_pages(logger, soup=None):
    if soup:
        pagination = soup.select('.pager .next a')[0]['href']
        print('pagination', pagination)
        return pagination
    else:
        logger.info(f"EXTRACTION DES LIENS DE PAGES NEXT")
        soup = request_page(logger)
        pagination = soup.select('.pager .next a')[0]['href']
        print('pagination', pagination)
        return pagination

def get_next_page(logger, soup):
    logger.info(f"EXTRACTION DU LIEN DE PAGES NEXT")

    soup = request_page(logger)
    pagination = soup.select('.pager .next a')[0]['href']
    print('pagination', pagination)
    return pagination

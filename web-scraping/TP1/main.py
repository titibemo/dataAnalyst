import requests
import logging
import pandas as pd
from requests.exceptions import RequestException, Timeout, ConnectionError
import time


BASE_URL = "https://quotes.toscrape.com/page"

# **Mission**
# 1. Créer une fonction `fetch_page(url)` avec gestion d'erreurs
# 2. Scraper les 3 premières pages du site
# 3. Pour chaque page, extraire le HTML brut
# 4. Compter le nombre de caractères de chaque page
# 5. Sauvegarder chaque page dans un fichier HTML
# 6. Créer un rapport CSV avec :
#    - URL de la page
#    - Statut HTTP
#    - Taille en octets
#    - Temps de réponse

# **Contraintes**
# - Utiliser une session
# - Ajouter un délai de 1 seconde entre requêtes
# - Gérer les erreurs proprement

# **Bonus**
# - Logger les étapes

def setup_logger(name, log_file=None, level=logging.INFO):
    """Logger """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if log_file:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

def fetch_page(logger,url, timeout=10):
    logger.info("="*60)
    logger.info(f"DÉBUT DES LOG ")
    logger.info("="*60)

    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0'})

    datas = []

    try:
        for page in range(1, 4):
            logger.info("="*60)
            logger.info(f"DÉBUT DE l'extraction - {page} ")
            logger.info("="*60)

            response = session.get(
                url=f"{BASE_URL}/{page}",
                timeout=timeout
            )

            response.raise_for_status()

            # 3. Pour chaque page, extraire le HTML brut
            html_page = response.text

            # 4. Compter le nombre de caractères de chaque page
            size_page = len(response.text)

            # 5. Sauvegarder chaque page dans un fichier HTML
            logger.info("="*60)
            logger.info(f"Sauvegarde de la page en fichier HTML {page}")
            logger.info("="*60)

            with open(f"exercices/TP1/page-html/page_{page}.html", "w", encoding="utf-8") as f:
                f.write(html_page)


            data = {
                "url": f"{BASE_URL}/{page}",
                "status": response.status_code,
                "size": size_page,
                "time": response.elapsed.total_seconds(),
            }
            datas.append(data)
            time.sleep(1)

        # 6. Créer un rapport CSV avec :
        #    - URL de la page
        #    - Statut HTTP
        #    - Taille en octets
        #    - Temps de réponse

        logger.info("="*60)
        logger.info(f"création du rapport CSV {page} ")
        logger.info("="*60)

        df = pd.DataFrame(datas)
        df.to_csv(f"exercices/TP1/csv/rapport{page}.csv", index=False)

        logger.info("="*60)
        logger.info(f"FIN DES LOG ")
        logger.info("="*60)


    except Timeout:
        logger.error(f"Timeout pour {url}")

        return None
    except ConnectionError:
        logger.error(f"Erreur de connexion pour {url}")
        return None
    except requests.exceptions.HTTPError as e:
        logger.error(f"Erreur HTTP {response.status_code}: {url}")
        return None
    except RequestException as e:
        logger.error(f"Erreur générale: {e}")
        return None

if "__main__" == __name__:
    logger = setup_logger("fetch_page", "exercices/TP1/logs/fetch_page.log")
    fetch_page(logger, BASE_URL)
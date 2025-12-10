## Exercice - Scraping de livres

# **Objectif** : Scraper un catalogue de livres

# **Site** : http://books.toscrape.com

# **Tâches**
# 1. Récupérer la page d'accueil
# 2. Pour chaque livre sur la page, extraire :
#    - Titre
#    - Prix (convertir en float)
#    - Note (étoiles → nombre)
#    - Disponibilité (In stock / Out of stock)
#    - URL de l'image
# 3. Créer un DataFrame Pandas
# 4. Calculer :
#    - Prix moyen
#    - Livre le plus cher
#    - Livre le moins cher
#    - Répartition par note
# 5. Sauvegarder dans `books.csv`
# 6. **Bonus** : Télécharger l'image du livre le plus cher

from bs4 import BeautifulSoup
import requests
import pandas as pd
from urllib.parse import urljoin, urlparse
import re
import os
from dotenv import load_dotenv
load_dotenv()

BASE_URL = os.getenv('BASE_URL')

def main():

    # 1. Récupérer la page d'accueil avec Requests
    response = requests.get(f'{BASE_URL}')
    response.raise_for_status()

    # 2. Pour chaque livre sur la page, extraire :
    #    - Titre
    #    - Prix (convertir en float)
    #    - Note (étoiles → nombre)
    #    - Disponibilité (In stock / Out of stock)
    #    - URL de l'image
    soup = BeautifulSoup(response.text, features="lxml")

    all_li = soup.select('section .row li')
    #print('li', all_li)

    books = []

    for li in all_li:
        book = {
            'Titre': li.select('.product_pod h3 a')[0]['title'],
            'Prix': float(re.search('\d+\.\d{2}', li.select('.product_pod .price_color')[0].text).group()), #li.select('.product_pod .price_color')[0].text[1:],
            'Note': li.select('.product_pod p:nth-of-type(1)')[0]['class'][1],
            'Disponibilité': li.select('.product_price p:nth-of-type(2)')[0].text.strip(),
            'URL de l\'image': urljoin(BASE_URL, li.select('img')[0]['src'])
        }
        books.append(book)
    
    # 3. Créer un DataFrame Pandas
    df = pd.DataFrame(books)
    print(df)

    # 4. Calculer :
    #    - Prix moyen
    #    - Livre le plus cher
    #    - Livre le moins cher
    #    - Répartition par note
    average_price = df['Prix'].mean()
    most_expensive_price = df['Prix'].max()
    less_expensive_price = df['Prix'].min()
    #    - Répartition par note (meilleur à la pire)
    repartition_by_notation = df.groupby('Note', sort=False)
    print(f"""
    Prix moyen : {average_price}
    Livre le plus cher : {most_expensive_price}
    Livre le moins cher : {less_expensive_price}
    Repartition par note : {repartition_by_notation}
""")

    # 5. Sauvegarder dans `books.csv`
    df.to_csv('books.csv', index=False)

    #6. **Bonus** : Telecharger l'image du livre le plus cher
    most_expensive_book_image_url = df['URL de l\'image'].loc[df['Prix'] == most_expensive_price].iloc[0]
    response = requests.get(most_expensive_book_image_url)
    response.raise_for_status()
    with open('most_expensive_book.jpg', 'wb') as f:
        f.write(response.content)

if __name__ == "__main__":
    main()
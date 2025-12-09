from bs4 import BeautifulSoup
import requests
import json

# **Objectif** : Extraire des données avec BeautifulSoup

# **Site** : http://quotes.toscrape.com

# **Tâches**
# 1. Récupérer la page d'accueil
# 2. Parser avec BeautifulSoup
# 3. Trouver toutes les citations (class="quote")
# 4. Pour chaque citation, extraire :
#    - Le texte de la citation
#    - L'auteur
#    - Les tags
# 5. Afficher les 5 premières citations
# 6. Compter le nombre total de citations sur la page
# 7. Créer une liste de dictionnaires avec les données
# 8. **Bonus** : Sauvegarder dans un fichier JSON

BASE_URL = "https://quotes.toscrape.com"

def main():
    # 1. Récupérer la page d'accueil avec Requests
    response = requests.get(BASE_URL)
    response.raise_for_status()

    # 2. Parser avec BeautifulSoup
    soup = BeautifulSoup(response.text, features="lxml")

    # 3. Trouver toutes les citations (class="quote")
    quotes_class: list = soup.select('.quote') # select all p in div

    # 4. Pour chaque citation, extraire :
    #    - Le texte de la citation
    #    - L'auteur
    #    - Les tags
    for quote in quotes_class:
        print(quote.select('.text')[0].text)
        print(quote.select('.author')[0].text)
        print(quote.select('.tags')[0].text)

    # 5. Afficher les 5 premières citations
    for quote in quotes_class[:5]:
        print(quote.select('.text')[0].text)
        print(quote.select('.author')[0].text)
        print(quote.select('.tags')[0].text)
    
    # 6. Compter le nombre total de citations sur la page
    print(len(quotes_class))

    # 7. Créer une liste de dictionnaires avec les données
    quotes_list = []
    for quote in quotes_class:
        tags = []
        all_tags = quote.select('.tags a')
        for tag in all_tags:
            tags.append(tag.get_text(strip=True, separator=", "))
        
        all_tags = quote.select('.tags a')
        clean_tag = all_tags[0].get_text(strip=True, separator=", ")
        quotes_list.append({
            'text': quote.select('.text')[0].text,
            'author': quote.select('.author')[0].text,
            'tags': tags
        })

    # 8. **Bonus** : Sauvegarder dans un fichier JSON
    with open('exercices/exercice2/quotes.json', 'w', encoding='utf-8') as file:
        json.dump(quotes_list, file, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
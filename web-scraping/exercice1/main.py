# # Exercice : Récupérer et analyser une page web

# **Site** : https://quotes.toscrape.com (site d'entraînement)

# **Tâches**
# 1. Récupérer la page d'accueil avec Requests
# 2. Afficher le code de statut
# 3. Afficher les 500 premiers caractères du HTML
# 4. Vérifier l'encodage de la page
# 5. Afficher les headers de la réponse
# 6. Récupérer le robots.txt du site
# 7. **Bonus** : Utiliser une session pour faire 3 requêtes successives

import requests
from urllib.robotparser import RobotFileParser

# 1. Récupérer la page d'accueil avec Requests
url = "https://quotes.toscrape.com"
response = requests.get(url)
response.raise_for_status()

# 2. Afficher le code de statut
print("Code HTTP :", response.status_code)

# 3. Afficher les 500 premiers caractères du HTML
landing_page = response.text

# 4. Vérifier l'encodage de la page
encoding = response.encoding

# "5. Afficher les headers de la réponse
headers = response.headers

# 6. Récupérer le robots.txt du site
robots_url = f"{url}/robots.txt"

# 7. **Bonus** : Utiliser une session pour faire 3 requêtes successives
def tester_acces():
    rp = RobotFileParser()
    rp.set_url(url)
    rp.read()

    print(f"Peut-on accéder à toutes les pages de: {url} ?",
        rp.can_fetch("*", url))

    
print(f"code statut : {response.status_code}, Encodage de la page : {encoding}, 500 prmeier caractères : {landing_page[:500]}, headers : {headers}, ")
print( "=" * 50)
tester_acces()

session = requests.Session()

session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0'})

response1 = session.get('https://quotes.toscrape.com/tag/love/')
response2 = session.get('https://quotes.toscrape.com/author/Andre-Gide/')
response3 = session.get('https://quotes.toscrape.com/author/Steve-Martin/')

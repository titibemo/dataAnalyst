import requests
import pandas as pd
import os
from requests.exceptions import RequestException, ConnectionError
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('API_KEY')
BASE_URL = os.getenv('BASE_URL')

print(BASE_URL, API_KEY)


# **Tâches**
# 1. Définir une liste de 10 villes françaises
#cities = ['Paris', 'Lyon', 'Marseille', 'Toulouse', 'Nice', 'Nantes', 'Strasbourg', 'Montpellier', 'Bordeaux', 'Lille']
#cities = ['Paris', 'Lyon', 'Marseille']
#cities = ["HHFHDSJKHH", "Paris"]
cities = ["HHFHDSJKHH", "Paris", "Toulouse", "Thierry", "Nice"]


# 2. Pour chaque ville, récupérer :
#    - Température actuelle
#    - Température ressentie
#    - Humidité
#    - Description
datas = []

def get_informations(params):
    try:
        response = requests.get(f"{BASE_URL}/weather", params=params)
        response.raise_for_status()
        data = response.json()

        datas.append({
            'ville': city,
            'temperature': data['main']['temp'],
            'ressenti': data['main']['feels_like'],
            'humidite': data['main']['humidity'],
            'description': data['weather'][0]['description']
        })

    except ConnectionError:
        print(" Erreur de connexion : Vérifiez votre réseau")
    except requests.exceptions.HTTPError as e:
        print(f" Erreur HTTP : {e}")
        print(f"Code : {response.status_code}")
        print(f"Message : {response.text}")
    except RequestException as e:
        print(f" Erreur générale : {e}")
    except ValueError:
        print(" La réponse n'est pas du JSON valide")


for city in cities:
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'fr'
    }
    get_informations(params)

# 3. Créer un DataFrame avec ces informations
df = pd.DataFrame(datas)
print(df)

# 4. Identifier la ville la plus chaude et la plus froide
max_temperature = df['temperature'].max()
min_temperature = df['temperature'].min()

# 5. Calculer la température moyenne
mean_temp = df['temperature'].mean()

# 6. Sauvegarder dans `meteo_villes.csv`
df.to_csv('meteo_villes.csv', index=False)

# 7. **Bonus** : Ajouter une gestion d'erreur si une ville n'est pas trouvée


import os
import requests
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

BASE_URL = os.getenv('BASE_URL')
API_VERSION = os.getenv('API_VERSION')

params_europe = {
    "field": "name",
    
}

# 1. Récupérer tous les pays d'Europe
try:
    response = requests.get(f"{BASE_URL}/{API_VERSION}/region/europe")
    response.raise_for_status()

    countries_europe = response.json()
    print(response)
    # for res in response:
    #     print(f"Nom du pays : {res['name']['common']}")
    
except Exception:
    print("Impossible de récupérer les infos")

# 2. Créer un DataFrame avec : nom, capitale, population, superficie
countries = []
capitals = []
population = []
area = []


for country in countries_europe:
    countries.append(country["translations"]["fra"]["common"])
    capitals.append(country["capital"][0])
    population.append(country["population"])
    area.append(country["area"])
    #print(f"country: {country["name"]}, capital: {country['capital']}, population: {country['population']}, area: {area['area']}")

df = pd.DataFrame({
    "country": countries,
    "capital": capitals,
    "population": population,
    "area": area,
})
    
print(df)

# 3. Calculer la densité de population (population / superficie)
df["density"] = df["population"] / df["area"]

# 4. Identifier les 5 pays les plus peuplés d'Europe
top_5_by_population = df.sort_values(by="population", ascending=False).head(5).reset_index()

# 5. Calculer la population totale de l'Europe
total_population = df["population"].sum()

# 6. Trouver le pays avec la plus grande densité
country_most_dense = df.sort_values(by="density", ascending=False).head(1).reset_index()

# 7. Sauvegarder les résultats dans `pays_europe.xlsx`
with pd.ExcelWriter('etl/exercices/exercice4/pays_europe.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='pays_europe', index=False)
    top_5_by_population.to_excel(writer, sheet_name='population_top_5', index=False)
#
    country_most_dense.to_excel(writer, sheet_name='plays_le_plus_densee', index=False)










# params_europe = {
#     'userId': 1
# }

# try:
#     response = requests.get('https://restcountries.com/v3.1/region/europe', params=params_europe)
#     response.raise_for_status()

#     response = response.json()
#     # print(response)
#     # print(len(response))

# except Exception:
#     print("Impossible de récup les infos")


# 3. Calculer la densité de population (population / superficie)
# 4. Identifier les 5 pays les plus peuplés d'Europe
# 5. Calculer la population totale de l'Europe
# 6. Trouver le pays avec la plus grande densité
# 7. Sauvegarder les résultats dans `pays_europe.xlsx`
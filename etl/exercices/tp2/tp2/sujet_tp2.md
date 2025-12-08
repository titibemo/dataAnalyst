
## Projet - Cahier des charges


**Contexte**
Vous êtes data engineer pour une entreprise de e-commerce. Vous devez créer un pipeline ETL quotidien pour analyser les ventes.

**Sources de données**
1. **Fichier CSV** (`ventes.csv`) : Transactions quotidiennes
   - Colonnes : date, produit_id, quantite, prix_unitaire, client_id
2. **API interne** : Catalogue produits (simulation avec JSONPlaceholder)
   - Endpoint : `/products`
   - Données : produit_id, nom, categorie, fournisseur
3. **API météo** : OpenWeatherMap pour la ville du siège
   - Impact des conditions météo sur les ventes

**Transformations requises**
- Nettoyage : doublons, valeurs manquantes
- Enrichissement : ajouter nom produit, catégorie
- Calculs : montant_total, moyenne par catégorie
- Agrégations : ventes par produit, par catégorie, par jour


## Projet final - Livrable


**Livrables attendus**

1. **Code source structuré**
   - Architecture modulaire
   - Classes Extract/Transform/Load
   - Configuration externe
   - Logging complet

2. **Fichier Excel de sortie** (`rapport_ventes.xlsx`)
   - Feuille "Ventes détaillées" : Données enrichies
   - Feuille "Par produit" : Agrégation par produit
   - Feuille "Par catégorie" : Agrégation par catégorie
   - Feuille "Métadonnées" : Date d'exécution, nombre de lignes, météo

3. **Documentation**
   - README avec instructions d'exécution
   - Comments dans le code

## Projet - Structure de départ possible


```python
# main.py
import os
from dotenv import load_dotenv
from src.pipeline import SalesPipeline
from src.utils.logger import setup_logger

def main():
    # Configuration
    load_dotenv()
    logger = setup_logger('Sales_ETL', 'logs/etl.log')
    
    config = {
        'csv_path': 'data/raw/ventes.csv',
        'api_base_url': 'https://jsonplaceholder.typicode.com',
        'weather_api_key': os.getenv('OPENWEATHER_API_KEY'),
        'output_path': 'data/output/rapport_ventes.xlsx'
    }
    
    # Exécuter pipeline
    pipeline = SalesPipeline(config, logger)
    pipeline.run()

if __name__ == '__main__':
    main()
```

## Projet - Données de test


**Mapping produits (à simuler ou créer)**
```python
produits = {
    1: {'nom': 'Souris', 'categorie': 'Périphérique'},
    2: {'nom': 'Clavier', 'categorie': 'Périphérique'},
    3: {'nom': 'Câble USB', 'categorie': 'Accessoire'},
    4: {'nom': 'Webcam', 'categorie': 'Périphérique'},
    5: {'nom': 'Casque', 'categorie': 'Audio'}
}
```
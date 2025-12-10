# 🕷️ Web Scraping Project

Ce projet permet d'extraire des données depuis un site web, de les nettoyer puis de les stocker dans un format exploitable (Fichier excel) Avec logs

## 🚀 Installation

Clonez le dépôt :

```bash
git clone https://github.com/titibemo/dataAnalyst/tree/main/web-scraping/TP2
```

Créer un environnement virtuel pour utiliser le projet :
```bash
python3 -m venv venv 
venv\Scripts\activate         
```

Installer les dépendances :
```bash
pip install -r requirements.txt  
```

Ajouter à la racine du projet un fichier .env pour y ajouter l'url:

```bash
BASE_URL=http://quotes.toscrape.com
```


Pour faire fonctionner le scraping, ouvrez un terminal à la racine du projet et effectuer la commande :
```bash
python main.py
```





## TP 2 - Scraper multi-pages

**Objectif** : Scraper plusieurs pages avec pagination

**Site** : http://quotes.toscrape.com

**Mission**
Créer un scraper complet qui :
1. Détecte automatiquement le nombre de pages
2. Scrape toutes les pages (jusqu'à 10 max)
3. Pour chaque citation, extrait :
   - Texte
   - Auteur
   - Tags
   - URL de l'auteur
4. Crée un fichier Excel avec 3 feuilles :
   - "Citations" : Toutes les citations
   - "Auteurs" : Liste unique des auteurs avec nb de citations
   - "Tags" : Liste des tags avec fréquence
5. Génère des statistiques :
   - Top 5 auteurs les plus cités
   - Top 10 tags les plus utilisés
   - Longueur moyenne des citations

**Contraintes**
- Code modulaire (fonctions)
- Gestion d'erreurs complète
- Logging
- Respect du délai entre requêtes
## Exercice - Scraping de livres

**Objectif** : Scraper un catalogue de livres

**Site** : http://books.toscrape.com

**Tâches**
1. Récupérer la page d'accueil
2. Pour chaque livre sur la page, extraire :
   - Titre
   - Prix (convertir en float)
   - Note (étoiles → nombre)
   - Disponibilité (In stock / Out of stock)
   - URL de l'image
3. Créer un DataFrame Pandas
4. Calculer :
   - Prix moyen
   - Livre le plus cher
   - Livre le moins cher
   - Répartition par note
5. Sauvegarder dans `books.csv`
6. **Bonus** : Télécharger l'image du livre le plus cher
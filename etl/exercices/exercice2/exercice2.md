## Exercice 2 - Excel complet


**Objectif** : Traiter des données de ventes mensuelles

**Fichier** : `ventes_janvier.xlsx` avec colonnes : date, produit, quantite, prix_unitaire, region

**Tâches**
1. Charger les données avec Pandas
2. Nettoyer :
   - Supprimer les doublons
   - Remplir les valeurs manquantes de `region` par "Non spécifié"
   - Convertir `date` en datetime
3. Transformer :
   - Créer `montant_total` = quantite × prix_unitaire
   - Extraire le `jour` et `jour_semaine` de la date
4. Analyser :
   - Total des ventes par région
   - Produit le plus vendu (en quantité)
   - Jour de la semaine avec le plus de ventes
5. Créer un fichier Excel avec 3 feuilles :
   - Feuille "Données" : Données nettoyées
   - Feuille "Par région" : Agrégation par région
   - Feuille "Par produit" : Agrégation par produit
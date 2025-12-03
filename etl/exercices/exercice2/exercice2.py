import pandas as pd

## Exercice 2 - Excel complet

# **Objectif** : Traiter des données de ventes mensuelles

# **Fichier** : `ventes_janvier.xlsx` avec colonnes : date, produit, quantite, prix_unitaire, region

# **Tâches**
# 1. Charger les données avec Pandas
df = pd.read_excel("etl/exercices/exercice2/ventes_janvier.xlsx")

# 2. Nettoyer :
#    - Supprimer les doublons
#    - Remplir les valeurs manquantes de `region` par "Non spécifié"
#    - Convertir `date` en datetime
df.drop_duplicates()
df["region"] = df["region"].fillna("Non spécifié")
df["date"] = pd.to_datetime(df['date'])

# 3. Transformer :
#    - Créer `montant_total` = quantite × prix_unitaire
#    - Extraire le `jour` et `jour_semaine` de la date
df["montant_total"] = df["quantite"]*df["prix_unitaire"]

# 4. Analyser :
#    - Total des ventes par région
#    - Produit le plus vendu (en quantité)
#    - Jour de la semaine avec le plus de ventes
total_sell_by_region = df.groupby("region")["montant_total"].sum().reset_index()

best_selled_product = df.groupby("produit")["quantite"].sum().sort_values(ascending=False).reset_index().head(1)


#    - Jour de la semaine avec le plus de ventes
df["days"] = df["date"].dt.day
df["day_by_week"] = df["date"].dt.dayofweek
best_selled_day = df.groupby("day_by_week")["quantite"].sum().sort_values(ascending=False).head(1)



# 5. Créer un fichier Excel avec 3 feuilles :
#    - Feuille "Données" : Données nettoyées
#    - Feuille "Par région" : Agrégation par région
#    - Feuille "Par produit" : Agrégation par produit

with pd.ExcelWriter('etl/exercices/exercice2/rapport.xlsx') as writer:
    df.to_excel(writer, sheet_name='Données', index=False)
    best_selled_product.to_excel(writer, sheet_name='Par région', index=False)
    total_sell_by_region.to_excel(writer, sheet_name='Par produit', index=False)


print(best_selled_product)
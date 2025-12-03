import pandas as pd
## TP 1 - Pipeline CSV vers Excel

# **Objectif** : Créer un pipeline de traitement automatisé

# **Contexte** : Vous recevez quotidiennement des fichiers CSV de différentes sources (magasins) et devez les consolider dans un rapport Excel.

# **Fichiers d'entrée** : `magasin_A.csv`, `magasin_B.csv`, `magasin_C.csv`

# **Colonnes** : date, produit, quantite, prix_unitaire, vendeur

# **Pipeline à construire** :
# 1. Charger tous les fichiers CSV
df_magasin_a = pd.read_csv("etl/exercices/tp1/magasin_A.csv")
df_magasin_b = pd.read_csv("etl/exercices/tp1/magasin_B.csv")
df_magasin_c = pd.read_csv("etl/exercices/tp1/magasin_C.csv")

# 2. Ajouter une colonne `magasin` (A, B ou C)
df_magasin_a["magasin"] = "A"
df_magasin_b["magasin"] = "B"
df_magasin_c["magasin"] = "C"

# 3. Concaténer tous les DataFrames

df_concat_magasin = pd.concat([df_magasin_a, df_magasin_b, df_magasin_c])

# 4. Nettoyer (doublons, valeurs manquantes)
df_concat_magasin.drop_duplicates()

# 5. Calculer `montant_total`
df_concat_magasin["montant_total"] = df_concat_magasin["quantite"] * df_concat_magasin["prix_unitaire"]

print(df_concat_magasin)
# 6. Créer un rapport Excel avec :
#    - Feuille "Consolidé" : Toutes les données
#    - Feuille "Par magasin" : Totaux par magasin
#    - Feuille "Par vendeur" : Performance des vendeurs
#    - Feuille "Top produits" : 10 produits les plus vendus
df_par_magasin = df_concat_magasin.groupby("magasin")["montant_total"].sum().reset_index()
df_par_magasin.columns = ["nom_magasin", "total_par_magasin"]

df_par_vendeur = df_concat_magasin.groupby("vendeur")["montant_total"].sum().reset_index()
df_par_vendeur.columns = ["nom_vendeur", "total_chiffres_d_affaires"]

df_par_top_produit = df_concat_magasin.groupby("produit")["quantite"].sum().sort_values(ascending=False).reset_index().head(10)
df_par_top_produit.columns = ["nom_produit", "quantite_total_vendu"]

with pd.ExcelWriter('etl/exercices/tp1/rapport.xlsx', engine='openpyxl') as writer:
    df_concat_magasin.to_excel(writer, sheet_name='Consolidé', index=False)
    df_par_magasin.to_excel(writer, sheet_name='Par magasin', index=False)
    df_par_vendeur.to_excel(writer, sheet_name='Par vendeur', index=False)
    df_par_top_produit.to_excel(writer, sheet_name='Top produits', index=False)
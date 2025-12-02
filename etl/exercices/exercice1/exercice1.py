import pandas as pd
# Exercice 1 - CSV avec Pandas

# question 1
df = pd.read_csv("etl/exercices/exercice1/ventes.csv")

# question 2
df["montant_total "] = df["quantite"]*df["prix_unitaire"]
print(df)

# question 3

total_sell_by_customer = df.groupby("vendeur").agg(
    {
        "montant_total ": "sum"
    })


## fonctionne aussi mais pas jolie
# total_sell_by_customer = df.groupby("vendeur").sum()

print(total_sell_by_customer)

# question 4

total_sell_by_product = df.groupby("produit").agg(
    {
        "quantite": "sum"
    })


print(total_sell_by_product)


# # question 5 Identifier le top 3 des ventes (montant le plus élevé)

top_3_sell = df.sort_values("montant_total ", ascending=False).head(3)
print(top_3_sell)


# # question 6

df.to_csv("etl/exercices/exercice1/ventes_analysees.csv", index=False)
import requests
import pandas as pd

## Exercice 3 - GET avec JSONPlaceholder


# **Objectif** : Récupérer et analyser des données


#1 et 2 :  Récupérer tous les utilisateurs (`/users`) et  Afficher le nom et l'email de chaque utilisateur
try:
    response = requests.get('https://jsonplaceholder.typicode.com/users')
    response.raise_for_status()

    response = response.json()
    for res in response:
        pass
        # print(res['name'])
        # print(res['email'])

except Exception:
    print("Impossible de récup les infos")

#3 et 4 Récupérer tous les posts de l'utilisateur avec `userId=1` et Compter combien de posts chaque utilisateur a créé
params = {
    'userId': 1
}

try:
    response = requests.get('https://jsonplaceholder.typicode.com/posts', params=params)
    response.raise_for_status()

    response = response.json()
    # print(response)
    # print(len(response))

except Exception:
    print("Impossible de récup les infos")

#5 Récupérer les commentaires du post `id=1`

params = {
    'id': 1
}

try:
    response = requests.get('https://jsonplaceholder.typicode.com/comments', params=params)
    response.raise_for_status()

    response = response.json()
    print(response)

except Exception:
    print("Impossible de récup les infos")


# 6. Créer un DataFrame Pandas avec :
#    - Colonnes : post_id, post_title, nombre_commentaires
#    - Pour les 10 premiers posts
#   -  enregistrer en csv


try:
    response = requests.get('https://jsonplaceholder.typicode.com/posts')
    response.raise_for_status()

    response = response.json()

except Exception:
    print("Erreur ! ")
userId = []
title = []
body = []

for i,post in enumerate(response):
    if i == 10:
        break
    userId.append(post["userId"])
    title.append(post["title"])
    body.append(post["body"])

df = pd.DataFrame({
    "post_id": userId,
    "post_title": title,
    "nombre_commentaires": body,
})


df.to_csv("etl/exercices/exercice3/output.csv", index=False)


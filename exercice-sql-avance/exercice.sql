-- =========================
-- TABLE : users
-- =========================
CREATE TABLE users (
    user_id       INTEGER PRIMARY KEY,
    username      TEXT        NOT NULL,
    country       TEXT        NOT NULL,
    subscription  TEXT        NOT NULL  -- 'Free' ou 'Premium'
);

-- =========================
-- TABLE : artists
-- =========================
CREATE TABLE artists (
    artist_id  INTEGER PRIMARY KEY,
    name       TEXT        NOT NULL,
    country    TEXT        NOT NULL
);

-- =========================
-- TABLE : tracks
-- =========================
CREATE TABLE tracks (
    track_id   INTEGER PRIMARY KEY,
    title      TEXT        NOT NULL,
    duration_s INTEGER     NOT NULL,
    artist_id  INTEGER     NOT NULL REFERENCES artists(artist_id)
);
-- =========================
-- TABLE : listenings
-- =========================
CREATE TABLE listenings (
    listening_id   INTEGER PRIMARY KEY,
    user_id        INTEGER NOT NULL REFERENCES users(user_id),
    track_id       INTEGER NOT NULL REFERENCES tracks(track_id),
    listened_at    TIMESTAMP NOT NULL,
    seconds_played INTEGER NOT NULL
);

--#################################### exercice 1

-- 1. Catalogue public des morceaux
/*Le service Produit souhaite afficher une liste publique des morceaux, contenant :

les informations du morceau,
la durée,
le nom de l’artiste associé.
Créer une vue adaptée à ce besoin, puis l’utiliser pour lister l’ensemble du catalogue de manière ordonnée.
*/

CREATE VIEW v_list_tracks AS 
SELECT t.track_id, t.title, t.duration, a.name, a.country
FROM tracks AS t
INNER JOIN artists AS a 
ON t.artist_is = a.artist_id
ORDER BY t.track_id ASC;

SELECT * FROM v_list_tracks;

/*
2. Utilisateurs Premium français
L’équipe marketing souhaite travailler spécifiquement sur les utilisateurs :

ayant un abonnement Premium,
résidant en France.
Créer une vue filtrée permettant d’identifier ces utilisateurs, puis l’utiliser pour obtenir une liste ordonnée.
*/

CREATE VIEW v_users_fr_premium AS
SELECT user_id, username, country, subscription
FROM users
WHERE country = 'France' AND subscription = 'Premium'
ORDER BY user_id ASC;

SELECT * FROM v_users_fr_premium;

/*
3. Historique détaillé des écoutes
L’équipe Data souhaite une vue qui rassemble toutes les informations utiles sur les écoutes :

l’utilisateur (identifiant, nom, pays),
le morceau (titre),
l’artiste,
la date/heure d’écoute,
la durée réellement écoutée.
Créer cette vue consolidée en utilisant les relations entre les tables, puis l’interroger pour extraire uniquement les écoutes réalisées par des utilisateurs français.
*/

CREATE VIEW v_listening_details_users AS 
SELECT u.user_id, u.username, u.country, t.title, a.name, l.listened_at, l.seconds_played
FROM users AS u
INNER JOIN listenings AS l
ON u.user_id = l.user_id
INNER JOIN tracks AS t
ON l.track_id = t.track_id
INNER JOIN artists AS a
ON t.artist_id = a.artist_id;

SELECT * FROM v_listening_details_users
where country = 'France';

/*
4. Statistiques d’écoute par artiste
Pour optimiser l’analyse, cette statistique doit être construite à partir d’une vue matérialisée reposant sur les écoutes détaillées :

Pour chaque artiste, calculer :

le nombre total d’écoutes,
le nombre total de secondes écoutées,
la durée moyenne écoutée par écoute.
Créer cette vue matérialisée, puis l’utiliser pour identifier les artistes les plus écoutés selon différents critères (par exemple ceux qui ont un nombre d’écoutes élevé, ou un volume total de lecture important).
*/

CREATE MATERIALIZED VIEW v_listening_details_artists AS 
SELECT 
    a.name,
    COUNT(l.listening_id) AS total_count_listening,
    SUM(l.seconds_played) AS total_seconds_listening, 
    AVG(l.seconds_played) AS avg_seconds_listening
FROM artists AS a
INNER JOIN tracks as t
ON a.artist_id = t.artist_id
INNER JOIN listenings AS l
ON t.track_id = l.track_id
GROUP BY a.name;

SELECT * FROM v_listening_details_artists
ORDER BY total_count_listening DESC;

/*
5. Analyse par pays d’artiste
À partir des statistiques d’écoute par artiste, analyser maintenant la performance :

par pays d’artiste,
en regroupant l’ensemble des artistes du même pays.
Produire une requête donnant, pour chaque pays :

le volume total d’écoute cumulé,
le nombre d’artistes concernés,
et ordonner ce classement.
*/

SELECT *, a.country FROM v_listening_details_artists
INNER JOIN artists AS a
ON v_listening_details_artists.name = a.name
ORDER BY a.country ASC;


/* 
6. Optimisation et index
Certaines colonnes de ces vues matérialisées seront utilisées très souvent dans des filtres et tris (par exemple le total de secondes ou la moyenne par écoute).

Identifier les colonnes les plus pertinentes à indexer, et proposer les index adaptés pour optimiser ces usages.
*/
CREATE INDEX idx_v_listening_detail_artists_total_listenings
ON v_listening_details_artists(total_count_listening);

CREATE INDEX idx_v_listening_detail_artists_avg_listenings
ON v_listening_details_artists(avg_seconds_listening);

--#################################### exercice 2  Vues matérialisées (Boutique en ligne)


-- =========================
-- TABLE : customers
-- =========================
CREATE TABLE customers (
    customer_id   INTEGER PRIMARY KEY,
    full_name     TEXT        NOT NULL,
    city          TEXT        NOT NULL,
    created_at    DATE        NOT NULL
);

-- =========================
-- TABLE : products
-- =========================
CREATE TABLE products (
    product_id   INTEGER PRIMARY KEY,
    name         TEXT        NOT NULL,
    category     TEXT        NOT NULL,
    unit_price   NUMERIC(10,2) NOT NULL
);

-- =========================
-- TABLE : orders
-- =========================
CREATE TABLE orders (
    order_id     INTEGER PRIMARY KEY,
    customer_id  INTEGER NOT NULL REFERENCES customers(customer_id),
    order_date   DATE    NOT NULL,
    status       TEXT    NOT NULL   -- 'PENDING', 'COMPLETED', 'CANCELLED'
);

-- =========================
-- TABLE : order_items
-- =========================
CREATE TABLE order_items (
    order_item_id  INTEGER PRIMARY KEY,
    order_id       INTEGER NOT NULL REFERENCES orders(order_id),
    product_id     INTEGER NOT NULL REFERENCES products(product_id),
    quantity       INTEGER NOT NULL,
    unit_price     NUMERIC(10,2) NOT NULL
);


/* 
1. Synthèse des commandes
L’équipe métier souhaite disposer d’une vue qui centralise, pour chaque commande :

les informations de base de la commande (client, date, statut),
le montant total de la commande.

Mettre en place une vue adaptée à ce besoin à partir des tables existantes.

Exploiter cette vue pour obtenir la liste des commandes complétées, avec leurs montants, classées par date puis par identifiant de commande.
*/

CREATE VIEW v_orders_informations AS
SELECT 
    o.order_id,
    o.order_date,
    o.status,
    c.full_name,
    c.city,
    SUM(oi.quantity * oi.unit_price) AS total_order
FROM orders AS o
INNER JOIN customers AS c
ON o.customer_id = c.customer_id
INNER JOIN order_items AS oi
ON o.order_id = oi.order_id
GROUP BY o.order_id, o.order_date, o.status, c.full_name, c.city
;

SELECT * FROM v_orders_informations
WHERE status = 'COMPLETED'
ORDER BY order_date ASC, order_id ASC;

/*
2. Statistiques de ventes par jour
Le service de reporting a besoin d’un tableau de bord quotidien indiquant, pour chaque jour :

le nombre de commandes complétées,
le chiffre d’affaires total de ces commandes.
Pour optimiser les performances, ce tableau de bord doit être construit à partir d’une vue matérialisée basée sur les données des commandes.

Mettre en place une vue matérialisée qui fournit ces statistiques quotidiennes.
Interroger cette vue pour afficher la totalité des jours connus, classés par date.
Interroger cette même vue pour obtenir uniquement les jours dont le chiffre d’affaires est supérieur ou égal à 200.
*/

CREATE MATERIALIZED VIEW mv_orders_informations AS
SELECT 
    o.order_date,
    COUNT(o.order_id) AS nb_orders,
    SUM(oi.quantity * oi.unit_price) AS total_order
FROM orders AS o
INNER JOIN order_items AS oi
ON o.order_id = oi.order_id
GROUP BY o.order_date;

SELECT * FROM mv_orders_informations
ORDER BY order_date ASC;

SELECT * FROM mv_orders_informations
WHERE total_order >+ 200
ORDER BY order_date ASC;

/*
3. Clients les plus rentables
La direction souhaite identifier les clients les plus intéressants commercialement, en se basant uniquement sur les commandes complétées :

Pour chaque client, on veut connaître :

le nombre de commandes complétées,
le chiffre d’affaires total associé.

Mettre en place une vue matérialisée qui regroupe ces informations par client.

Exploiter cette vue pour afficher la liste des clients, classés du plus gros chiffre d’affaires au plus faible.
Exploiter cette vue pour afficher uniquement les clients ayant passé au moins deux commandes complétées.
*/

CREATE MATERIALIZED VIEW mv_best_customers AS
SELECT 
    c.full_name,
    COUNT(o.order_id) AS nb_orders,
    SUM(oi.quantity * oi.unit_price) AS total_order
FROM orders AS o
INNER JOIN customers AS c
ON o.customer_id = c.customer_id
INNER JOIN order_items AS oi
ON o.order_id = oi.order_id
GROUP BY c.full_name;

SELECT * FROM mv_best_customers
ORDER BY total_order DESC;

SELECT * FROM mv_best_customers
WHERE nb_orders >= 2
ORDER BY total_order DESC;

/*
4. Optimisation via index
Certaines requêtes sont particulièrement fréquentes :

filtrer ou trier les statistiques par date,
interroger souvent les clients par chiffre d’affaires total.

Proposer un ou plusieurs index pertinents sur les vues matérialisées précédentes afin d’optimiser ces usages.

Justifier brièvement, pour chaque index, le type de requête qu’il permet d’accélérer.

*/

CREATE INDEX idx_mv_best_customers_total_order
ON mv_best_customers(total_order);


/*
5. Données à jour vs vues matérialisées
On simule maintenant l’arrivée de nouvelles données dans le système :

Une nouvelle commande complétée est enregistrée pour le client 2 :

INSERT INTO orders (order_id, customer_id, order_date, status)
VALUES (7, 2, DATE '2024-05-04', 'COMPLETED');

INSERT INTO order_items (order_item_id, order_id, product_id, quantity, unit_price) VALUES
    (8, 7, 3, 1, 89.00),
    (9, 7, 4, 1, 19.90);
Vérifier, à l’aide de la vue classique mise en place à la question 1, que cette nouvelle commande est bien prise en compte.
Vérifier, à l’aide de la vue matérialisée de statistiques quotidiennes, si les données reflètent ou non cette nouvelle commande.
Mettre à jour la vue matérialisée de statistiques quotidiennes pour qu’elle reflète l’état actuel des données.
Refaire la vérification et expliquer (en quelques mots, par commentaire ou à l’oral) la différence de comportement entre la vue classique et la vue matérialisée.
*/

-- 1
SELECT * FROM v_orders_informations
WHERE status = 'COMPLETED'
ORDER BY order_date ASC, order_id ASC;

-- 2 ancienne données ne faisant pas apparaitre la niuvelle commande

SELECT * FROM mv_orders_informations
ORDER BY order_date ASC;

/* resultat
    "2024-05-01"	2	119.70
    "2024-05-02"	3	158.80
    "2024-05-03"	2	209.70
*/

-- 3 mise a jour vue statistiques :

REFRESH MATERIALIZED VIEW mv_orders_informations;

-- 4 après refresh

SELECT * FROM mv_orders_informations
ORDER BY order_date ASC;

/* resultat
    "2024-05-01"	2	119.70
    "2024-05-02"	3	158.80
    "2024-05-03"	2	209.70
    "2024-05-04"	2	108.90
/*
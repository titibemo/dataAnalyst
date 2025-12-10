import pandas as pd

def transforms_data(logger, quotes_citation, quotes_authors, quotes_tags):
    logger.info(f" ================ TRANSFORMATION DES DONNEES ===============")
    df_citations = pd.DataFrame(quotes_citation, columns=['Citations'])
    df_authors = pd.DataFrame(quotes_authors, columns=['Auteurs'])
    df_tags = pd.DataFrame(quotes_tags, columns=['Tags'])

#    - Top 5 auteurs les plus cités
    top_5_authors = df_authors['Auteurs'].groupby(df_authors['Auteurs']).count().sort_values(ascending=False).head(5)
    logger.info(f"top 5 auteurs: {top_5_authors}")

#    - Longueur moyenne des citations
    df_citations['longueur moyenne'] = df_citations['Citations'].str.len().mean()
    logger.info(f"longueur moyenne des citations: {df_citations['longueur moyenne']}")

#    - Top 10 tags les plus utilisés
    top_10_tags = df_tags["Tags"].groupby(df_tags["Tags"]).count().sort_values(ascending=False).head(10)
    logger.info(f"top 10 tags: {top_10_tags}")

    logger.info(f" ================ FIN DE TRANSFORMATION DES DONNEES ===============")
    return df_citations, df_authors, df_tags

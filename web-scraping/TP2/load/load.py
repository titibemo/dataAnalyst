import pandas as pd
def load_excel(logger, df_citations, df_authors, df_tags):
    logger.info(f" ================ CHARGEMENT DES DONNEES DANS EXCEL ===============")

    with pd.ExcelWriter('test-quotes.xlsx', engine='openpyxl') as writer:
        df_citations.to_excel(writer, sheet_name='Citations', index=False)
        df_authors.to_excel(writer, sheet_name='Auteurs', index=False)
        df_tags.to_excel(writer, sheet_name='Tags', index=False)

    logger.info(f" ================ FIN DU CHARGEMENT DES DONNEES DANS EXCEL ===============")
    logger.info(f" ================ FIN DU PROGRAMME ===============")
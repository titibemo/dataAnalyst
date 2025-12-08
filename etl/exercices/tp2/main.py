import os
import yaml
import pandas as pd

from src.utils.logger import setup_logger
from src.pipeline_csv import Pipeline_csv
from src.pipeline_api import Pipeline_api


def load_config():
    """Lit le fichier config/config.yaml et renvoie un dict."""
    config_path = os.path.join("config", "config.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config


def main():
    # 1) Logger principal
    logger = setup_logger("ETL_API", "logs/etl_api.log")

    # 2) Chargement de la configuration
    config = load_config()

    # 3) Instanciation de la pipeline API
    pipeline_csv = Pipeline_csv(config=config, logger=logger)

    pipeline_api = Pipeline_api(config=config, logger=logger)

    # 4) Exécution du pipeline
    pipeline_csv.run()
    pipeline_api.run()

    files = os.listdir(config["paths"]["output"])

    dataframes = []

    for file in files:
        df = pd.read_excel(config["paths"]["output"] + "/" + file)
        dataframes.append(df)

    # merge 
    df = pd.merge(dataframes[0], dataframes[1], how="inner")

    print(df)

    df_by_product = df.groupby("produit_id")["quantite"].sum().reset_index()
    df_by_product = df[["produit_id", "nom", "categorie", "quantite", "montant_total"]]

    df_by_category = df.groupby("categorie")["montant_total"].sum().reset_index()

    with pd.ExcelWriter(config["paths"]["rapport"] + "/" + "rapport_ventes.xlsx", engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name="Ventes détaillées", index=False)
        df_by_product.to_excel(writer, sheet_name="Par produit", index=False)
        df_by_category.to_excel(writer, sheet_name="Par catégorie", index=False)
   

if __name__ == "__main__":
    main()
import os
import pandas as pd

from src.pipeline.pipeline_base import ETLPipeline        # ETLPipeline générique déjà existante
from src.extractors.extractors import CSVExtractor

class Pipeline_csv(ETLPipeline):
    """
    Pipeline CSV Transactions quotidiennes
   - Colonnes : date, produit_id, quantite, prix_unitaire, client_id

    Étapes :
    1) EXTRACT  : fichier dans data/raw
    2) TRANSFORM:
         - nettoyage (doublons, espaces, colonnes vides)
         - validation des colonnes essentielles
         - enrichissement (longueur du titre)
    3) LOAD     : écriture en Excel dans data/output/posts_api.xlsx
    """

    def _extract(self) -> pd.DataFrame:
        """Extraction du fichier vente depuis data/raw."""

        # 1) Récupéreration du file_path
        file_path = self.config["paths"]["raw_data"] + "/ventes.csv"

        # 2) extracteur csv
        self.extractor = CSVExtractor(
            logger=self.logger,
        )

        df = self.extractor.extract(file_path)

        return df
    
    def _transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """Nettoie, valide et enrichit les données issues du CSVI."""

        df_clean = self.transformer.clean(data)

        # 2) Validation de la présence de colonnes clés
        required_cols = ["date", "produit_id", "quantite", "prix_unitaire", "client_id"]
        self.transformer.validate(df_clean, required_cols)

        # 3) Enrichissement : ajout d'une colonne "add_total_product"
        def add_total_product(df: pd.DataFrame) -> pd.DataFrame:
            df = df.copy()
            df["montant_total"] = df["quantite"]*df["prix_unitaire"]
            return df

        df_enriched = self.transformer.enrich(df_clean, add_total_product)

        return df_enriched

    
    def _load(self, data: pd.DataFrame) -> None:
        """Charge les données transformées dans un fichier Excel."""

        # Dossier de sortie depuis la config
        output_dir = self.config["paths"]["output"]
        os.makedirs(output_dir, exist_ok=True)

        # Nom du fichier de sortie Excel
        output_file = os.path.join(output_dir, "ventes.xlsx")

        # Utilisation du DataLoader pour écrire en Excel
        self.loader.load_excel(
            df=data,
            filepath=output_file,
            sheet_name="ventes"
        )

        # À la fin, on aura un fichier data/output/posts_api.xlsx
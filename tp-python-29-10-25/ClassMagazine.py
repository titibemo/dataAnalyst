from ClassDocument import Document
from ClassConsultable import Consultable

class Magazine(Document, Consultable):
    def __init__(self, titre, annee_publication, numero_magazine):
        super().__init__(titre, annee_publication)
        self.numero_magazine = numero_magazine
    
    def afficher_infos(self):
        print(f"magazine: {self.titre}, {self.annee_publication}, {self.numero_magazine}, ")

    def consulter(self):
        print("vous consulter un MAGAZINE")
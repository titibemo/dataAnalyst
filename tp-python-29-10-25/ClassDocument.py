from abc import ABC, abstractmethod

class Document(ABC):
    nb_document = 0
     
    def __init__(self, titre: str, annee_publication: int):
        self.titre = titre
        self.annee_publication = annee_publication
        Document.nb_document += 1
    
    @abstractmethod
    def afficher_infos():
        pass

    @classmethod
    def afficherNbDocument(cls):
        print(f"nombre de document {cls.nb_document}")
    
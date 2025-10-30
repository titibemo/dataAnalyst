from ClassDocument import Document
from ClassEmpruntable import Empruntable
from ClassConsultable import Consultable
from ClassDocumentDejaEmprunteException import DocumentDejaEmprunteException
from ClassDocumentNonEmprunteException import DocumentNonEmprunteException

class Livre(Document, Empruntable, Consultable):
    def __init__(self, titre, annee_publication, auteur, nbPages, genre, est_emprunte):
        Document.__init__(self, titre, annee_publication)
        Empruntable.__init__(self, est_emprunte)
        self.auteur = auteur
        self.nbPages = nbPages
        self.genre = genre

    @staticmethod
    def compteur_pages(list_book: Livre):
        pages = 0
        for book in list_book:
            if isinstance(book, Livre):
                pages += book.nbPages
        print(f"📕📕📕 Plus de {pages} pages de livres à dévorer 📕📕📕")

    def afficher_infos(self):
        print(f"livre: {self.titre}, {self.annee_publication}, {self.auteur}, {self.nbPages}, {self.genre}, {self.est_emprunte} ")
    
    def consulter(self):
        print("vous consulter un LIVRE")

    def emprunter(self):
        try:
            if self.est_emprunte:
                raise DocumentDejaEmprunteException("🚫  Le livre est déja emprunté !  🚫")
        except DocumentDejaEmprunteException as e:
            print()
            print(e)
            print()
        else:
            print("livre emprunté")
            self.est_emprunte = True

    def rendre(self):
        try:
            if not self.est_emprunte:
                raise DocumentNonEmprunteException("🚫  Vous n'avez pas emprunté le livre ! 🚫")
        except DocumentNonEmprunteException as e:
            print()
            print(e)
            print()
        else:
            print("livre rendu ")
            self.est_emprunte = False

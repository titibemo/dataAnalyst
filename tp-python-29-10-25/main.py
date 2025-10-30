from ClassLivre import Livre
from ClassMagazine import Magazine
from ClassDocument import Document
from ClassGenre import Genre


def nav():
    print("====== GESTION BIBLIOTHEQUE ======")
    print("====== 1. Consulter ======")
    print("====== 2. Emprunt ======")
    print("====== 3. Restitution ======")
    print("====== 0. Quitter ======")

def show_book(books):
    print()
    Document.afficherNbDocument()
    Livre.compteur_pages(books)
    for i, book in enumerate(books):
        print(f"=== element {i+1}   ===")
        book.afficher_infos()
    print()

def main():
    all_books = [
        Livre("livre 1", 2001, "titi_1", 100, Genre.ROMAN.value, True),
        Livre("livre 2", 2002, "titi_2", 200, Genre.FANTASTIQUE.value, False),
        Livre("livre 3", 2003, "titi_3", 300, Genre.SCIENCE_FICTION.value, False),
        Magazine("le mag 1", 1998, 1),
        Magazine("le mag 2", 1999, 2)
    ]
    

    while True:
        nav()
        user_input = input("Que voulez vous faire ? :")
        match user_input:
            case "1":
                show_book(all_books)
                user_input = int(input("➡️  quel livre Voulez-vous CONSULTER ? "))
                all_books[user_input -1].consulter()             
            case "2":
                show_book(all_books)
                user_input = int(input("➡️  quel livre ou magazine voulez vous EMPRUNTER ? "))
                all_books[user_input -1].emprunter()
            case "3":
                show_book(all_books)
                user_input = int(input("➡️  quel livre ou magazine voulez vous RESTITUER ? "))
                all_books[user_input -1].rendre()
            case "0":
                print("🖐️  Merci et bonne journée")
                exit()

if __name__ == '__main__':
    main()
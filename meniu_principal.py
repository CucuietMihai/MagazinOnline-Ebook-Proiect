from utilizatori import Utilizator, Admin
from produse import Produs
from cos_cumparaturi import CosCumparaturi
from recenzii import Recenzie
from contact import formular_contact

# Meniul principal al aplicatiei, apelat la pornirea programului.
# Permite inregistrare, login, trimitere mesaj de contact sau iesire din aplicatie.
def meniu_principal():
    # Initializam toate tabelele din baza de date la pornirea aplicatiei
    Utilizator.init_db()
    Produs.init_db()
    CosCumparaturi.init_db()
    Recenzie.init_db()

    while True:
        print("\n=== Meniu Principal ===")
        print("1. Inregistrare")
        print("2. Login")
        print("3. Formular de contact")
        print("4. Iesire")

        opt = input("Alege o optiune: ")

        if opt == "1":
            utilizator = Utilizator.inregistrare()
            if utilizator:
                meniu_utilizator(utilizator)
        elif opt == "2":
            utilizator = Utilizator.login()
            if utilizator:
                # Daca username-ul este 'admin', transformam in obiect Admin
                if utilizator.username.lower() == "admin":
                    utilizator = Admin(utilizator.username, utilizator.get_email(), "admin")
                meniu_utilizator(utilizator)
        elif opt == "3":
            formular_contact()
        elif opt == "4":
            print("La revedere!")
            break
        else:
            print("Optiune invalida.")

# Meniul disponibil pentru utilizatorul logat (inclusiv admin).
# Permite acces la toate functionalitatile aplicatiei.
def meniu_utilizator(utilizator):
    cos = CosCumparaturi(utilizator.username)

    while True:
        print(f"\n--- Bine ai venit {utilizator.username} ---")
        print("1. Listare produse")
        print("2. Detalii produs")
        print("3. Adauga in cos")
        print("4. Vezi cosul")
        print("5. Goleste cosul")
        print("6. Finalizeaza comanda")
        print("7. Formular de contact")
        print("8. Adauga recenzie produs")
        print("9. Vezi recenzii produs")
        print("10. Cautare produs")
        print("11. Adauga produs")
        print("12. Sterge produs")
        print("13. Afiseaza categorii unice de produse")
        if isinstance(utilizator, Admin):
            print("14. Sterge produs direct (ADMIN)")
        print("0. Logout")

        opt = input("Alege o optiune: ")

        if opt == "1":
            Produs.listare_produse()
        elif opt == "2":
            try:
                produs_id = int(input("ID produs: "))
                Produs.afiseaza_detalii(produs_id)
            except ValueError:
                print("ID invalid.")
        elif opt == "3":
            try:
                produs_id = int(input("ID produs: "))
                cantitate = int(input("Cantitate: "))
                cos.adauga(produs_id, cantitate)
            except ValueError:
                print("Date invalide.")
        elif opt == "4":
            cos.vezi()
        elif opt == "5":
            cos.goleste()
        elif opt == "6":
            cos.finalizeaza()
        elif opt == "7":
            formular_contact()
        elif opt == "8":
            try:
                produs_id = int(input("ID produs pentru recenzie: "))
                Recenzie.adauga(utilizator.username, produs_id)
            except ValueError:
                print("ID invalid.")
        elif opt == "9":
            try:
                produs_id = int(input("ID produs pentru vizualizare recenzii: "))
                Recenzie.vezi(produs_id)
            except ValueError:
                print("ID invalid.")
        elif opt == "10":
            cuvant_cheie = input("Introduceti cuvantul cheie pentru cautare: ").strip()
            Produs.cauta(cuvant_cheie)
        elif opt == "11":
            Produs.adauga()
        elif opt == "12":
            Produs.sterge()
        elif opt == "13":
            Produs.categorii_disponibile()
        elif opt == "14" and isinstance(utilizator, Admin):
            try:
                produs_id = int(input("ID produs de sters: "))
                utilizator.sterge_produs_direct(produs_id)
            except ValueError:
                print("ID invalid.")
        elif opt == "0":
            utilizator.logout()
            break
        else:
            print("Optiune invalida.")

if __name__ == "__main__":
    meniu_principal()

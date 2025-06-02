import sqlite3

class Produs:
    """
    Clasa care defineste produsele din magazinul de eBook-uri.
    """

    def __init__(self, nume=None, pret=None, categorie=None):
        """
        Initializeaza un obiect de tip Produs.
        """
        self.nume = nume
        self.pret = pret
        self.categorie = categorie

    @staticmethod
    def init_db():
        """
        Creeaza tabela produse in baza de date si insereaza produse initiale daca nu exista deja produse.
        """
        conn = sqlite3.connect("magazin_ebook.db")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produse (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nume TEXT NOT NULL,
                descriere TEXT,
                pret REAL NOT NULL,
                categorie TEXT NOT NULL,
                stoc INTEGER NOT NULL DEFAULT 0
            )
        ''')
        conn.commit()

        cursor.execute("SELECT COUNT(*) FROM produse")
        if cursor.fetchone()[0] == 0:
            produse_initiale = [
                ("Atomic Habits", "Schimba-ti obiceiurile, transforma-ti viata", 24.99, "Dezvoltare personala", 20),
                ("Clean Code", "Ghid pentru un cod curat", 39.99, "Programare", 15),
                ("1984", "Roman distopic de George Orwell", 19.99, "Fictiune", 12),
                ("Deep Work", "Concentrare profunda intr-o lume distrasa", 29.99, "Productivitate", 18),
                ("Python Crash Course", "Curs complet pentru incepatori", 34.99, "Programare", 25),
                ("Steve Jobs", "Biografia fondatorului Apple", 27.50, "Biografii", 10),
                ("The Lean Startup", "Inoveaza rapid si eficient", 22.00, "Afaceri", 17),
                ("The Subtle Art of Not Giving a F*ck", "Carte motivationala realista", 21.50, "Dezvoltare personala", 13),
                ("Zero to One", "Note despre startup-uri", 23.75, "Afaceri", 11),
                ("Harry Potter si Piatra Filozofala", "Primul volum al seriei", 17.99, "Fictiune", 20),
                ("Educated", "Memoriile unei fete ce a fugit de fanatism", 25.00, "Memorii", 14),
                ("Gandire rapida, gandire lenta", "Psihologia deciziilor", 28.99, "Psihologie", 16)
            ]
            cursor.executemany("INSERT INTO produse (nume, descriere, pret, categorie, stoc) VALUES (?, ?, ?, ?, ?)", produse_initiale)
            conn.commit()
        conn.close()

    @staticmethod
    def listare_produse():
        """
        Afiseaza toate produsele existente in baza de date.
        """
        conn = sqlite3.connect("magazin_ebook.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, nume, pret, categorie, stoc FROM produse")
        produse = cursor.fetchall()
        conn.close()
        for p in produse:
            print(f"ID: {p[0]}, {p[1]} - {p[2]} RON ({p[3]}) Stoc: {p[4]}")

    @staticmethod
    def afiseaza_detalii(produs_id):
        """
        Afiseaza detaliile complete pentru un produs selectat dupa ID.
        """
        conn = sqlite3.connect("magazin_ebook.db")
        cursor = conn.cursor()
        cursor.execute("SELECT nume, descriere, pret, categorie, stoc FROM produse WHERE id = ?", (produs_id,))
        produs = cursor.fetchone()
        conn.close()

        if produs:
            print("\n--- Detalii Produs ---")
            print(f"Nume: {produs[0]}")
            print(f"Descriere: {produs[1]}")
            print(f"Pret: {produs[2]} RON")
            print(f"Categorie: {produs[3]}")
            print(f"Stoc disponibil: {produs[4]}")
        else:
            print("Produsul nu a fost gasit.")

    @staticmethod
    def cauta(cuvant_cheie):
        """
        Permite cautarea produselor dupa cuvinte cheie in nume sau descriere.
        """
        conn = sqlite3.connect("magazin_ebook.db")
        cursor = conn.cursor()
        query = f"%{cuvant_cheie}%"
        cursor.execute("SELECT id, nume, pret, categorie FROM produse WHERE nume LIKE ? OR descriere LIKE ?", (query, query))
        rezultate = cursor.fetchall()
        conn.close()

        if rezultate:
            print("\n--- Rezultate cautare ---")
            for r in rezultate:
                print(f"ID: {r[0]}, {r[1]} - {r[2]} RON ({r[3]})")
        else:
            print("Niciun produs gasit.")

    @staticmethod
    def adauga():
        """
        Permite adaugarea manuala a unui produs nou in baza de date.
        """
        nume = input("Nume produs: ")
        descriere = input("Descriere: ")
        try:
            pret = float(input("Pret: "))
            stoc = int(input("Stoc: "))
        except ValueError:
            print("Pret sau stoc invalid.")
            return
        categorie = input("Categorie: ")

        conn = sqlite3.connect("magazin_ebook.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO produse (nume, descriere, pret, categorie, stoc) VALUES (?, ?, ?, ?, ?)",
                       (nume, descriere, pret, categorie, stoc))
        conn.commit()
        conn.close()
        print("Produs adaugat cu succes.")

    @staticmethod
    def sterge():
        """
        Permite stergerea unui produs existent din baza de date dupa ID.
        """
        try:
            produs_id = int(input("ID produs de sters: "))
        except ValueError:
            print("ID invalid.")
            return

        confirmare = input("Esti sigur ca vrei sa stergi acest produs? (da/nu): ").lower()
        if confirmare != "da":
            print("Stergerea a fost anulata.")
            return

        conn = sqlite3.connect("magazin_ebook.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM produse WHERE id = ?", (produs_id,))
        if cursor.rowcount == 0:
            print("Produsul nu a fost gasit.")
        else:
            print("Produs sters cu succes.")
        conn.commit()
        conn.close()

    def afiseaza(self):
        """
        Afiseaza sumarul obiectului curent de tip Produs.
        """
        print(f"Produs: {self.nume} | Pret: {self.pret} RON | Categorie: {self.categorie}")
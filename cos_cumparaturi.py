import sqlite3

class CosCumparaturi:
    """
    Clasa care gestioneaza cosul de cumparaturi pentru fiecare utilizator.
    """

    def __init__(self, username):
        """
        Initializeaza un cos de cumparaturi pentru un utilizator dat.
        """
        self.username = username

    @staticmethod
    def init_db():
        """
        Creeaza tabela cos in baza de date daca nu exista deja.
        """
        conn = sqlite3.connect("magazin_ebook.db")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                produs_id INTEGER NOT NULL,
                cantitate INTEGER NOT NULL,
                FOREIGN KEY(produs_id) REFERENCES produse(id)
            )
        ''')
        conn.commit()
        conn.close()

    def adauga(self, produs_id, cantitate=1):
        """
        Adauga produse in cosul de cumparaturi.
        Verifica daca produsul exista si daca stocul este suficient.
        """
        conn = sqlite3.connect("magazin_ebook.db")
        cursor = conn.cursor()

        cursor.execute("SELECT stoc FROM produse WHERE id = ?", (produs_id,))
        rezultat = cursor.fetchone()
        if not rezultat:
            print("Produsul nu exista.")
            conn.close()
            return

        stoc_disponibil = rezultat[0]
        if stoc_disponibil < cantitate:
            print(f"Stoc insuficient. Doar {stoc_disponibil} bucati disponibile.")
            conn.close()
            return

        cursor.execute("SELECT cantitate FROM cos WHERE username = ? AND produs_id = ?", (self.username, produs_id))
        existing = cursor.fetchone()
        if existing:
            noua_cantitate = existing[0] + cantitate
            cursor.execute("UPDATE cos SET cantitate = ? WHERE username = ? AND produs_id = ?",
                           (noua_cantitate, self.username, produs_id))
        else:
            cursor.execute("INSERT INTO cos (username, produs_id, cantitate) VALUES (?, ?, ?)",
                           (self.username, produs_id, cantitate))

        conn.commit()
        conn.close()
        print("Produs adaugat in cos.")

    def vezi(self):
        """
        Afiseaza continutul cosului de cumparaturi si permite aplicarea de cupoane de reducere.
        """
        conn = sqlite3.connect("magazin_ebook.db")
        cursor = conn.cursor()
        cursor.execute(''' 
            SELECT p.nume, p.pret, c.cantitate, (p.pret * c.cantitate) as total
            FROM cos c
            JOIN produse p ON c.produs_id = p.id
            WHERE c.username = ? 
        ''', (self.username,))
        produse = cursor.fetchall()
        conn.close()

        if not produse:
            print("\nCosul tau este gol.")
            return

        print("\n--- Cosul tau ---")
        total_general = 0
        for produs in produse:
            print(f"{produs[0]} - {produs[1]} RON x {produs[2]} = {produs[3]:.2f} RON")
            total_general += produs[3]

        cupon = input("Ai un cupon de reducere? Introdu codul (sau Enter pentru a ignora): ").strip()
        if cupon:
            reducere = self.valideaza_cupon(cupon)
            if reducere:
                discount = total_general * reducere / 100
                total_general -= discount
                print(f"Reducere aplicata: {reducere}% (-{discount:.2f} RON)")
            else:
                print("Codul de reducere nu este valid.")

        print(f"Total final: {total_general:.2f} RON")

    def goleste(self):
        """
        Goleste complet cosul de cumparaturi.
        """
        conn = sqlite3.connect("magazin_ebook.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cos WHERE username = ?", (self.username,))
        conn.commit()
        conn.close()
        print("Cosul a fost golit.")

    def finalizeaza(self):
        """
        Finalizeaza comanda: verifica stocul si actualizeaza inventarul.
        """
        conn = sqlite3.connect("magazin_ebook.db")
        cursor = conn.cursor()

        cursor.execute("SELECT produs_id, cantitate FROM cos WHERE username = ?", (self.username,))
        produse = cursor.fetchall()

        if not produse:
            print("Nu ai produse in cos pentru a plasa comanda.")
            conn.close()
            return

        for produs_id, cantitate in produse:
            cursor.execute("SELECT stoc FROM produse WHERE id = ?", (produs_id,))
            stoc = cursor.fetchone()[0]
            if cantitate > stoc:
                print(f"Stoc insuficient pentru produsul cu ID {produs_id}. Comanda anulata.")
                conn.close()
                return
            cursor.execute("UPDATE produse SET stoc = stoc - ? WHERE id = ?", (cantitate, produs_id))

        cursor.execute("DELETE FROM cos WHERE username = ?", (self.username,))
        conn.commit()
        conn.close()

        print("\nComanda a fost plasata cu succes! Multumim pentru cumparaturi.")
        print("Nu uita sa lasi o recenzie pentru produsele comandate!")
        input("Apasa Enter pentru a reveni la meniul principal.")

    @staticmethod
    def valideaza_cupon(cupon):
        """
        Valideaza cuponul de reducere introdus.
        """
        cupon_valid = {
            "DISCOUNT10": 10,
            "DISCOUNT20": 20,
            "DISCOUNT30": 30,
        }
        return cupon_valid.get(cupon.upper(), None)

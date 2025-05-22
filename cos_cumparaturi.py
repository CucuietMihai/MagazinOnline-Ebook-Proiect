import sqlite3

class CosCumparaturi:
    def __init__(self, username):
        self.username = username

    @staticmethod
    def init_db():
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
            print(f"Stoc insuficient. Doar {stoc_disponibil} bucăți disponibile.")
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
        print("Produs adăugat în coș.")

    def vezi(self):
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
            print("\nCoșul tău este gol.")
            return

        print("\n--- Coșul tău ---")
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
                print(f"Reducere aplicată: {reducere}% (-{discount:.2f} RON)")
            else:
                print("Codul de reducere nu este valid.")

        print(f"Total final: {total_general:.2f} RON")

    def goleste(self):
        conn = sqlite3.connect("magazin_ebook.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cos WHERE username = ?", (self.username,))
        conn.commit()
        conn.close()
        print("Coșul a fost golit.")

    def finalizeaza(self):
        conn = sqlite3.connect("magazin_ebook.db")
        cursor = conn.cursor()

        cursor.execute("SELECT produs_id, cantitate FROM cos WHERE username = ?", (self.username,))
        produse = cursor.fetchall()

        if not produse:
            print("Nu ai produse în coș pentru a plasa comanda.")
            conn.close()
            return

        for produs_id, cantitate in produse:
            cursor.execute("SELECT stoc FROM produse WHERE id = ?", (produs_id,))
            stoc = cursor.fetchone()[0]
            if cantitate > stoc:
                print(f"Stoc insuficient pentru produsul cu ID {produs_id}. Comanda anulată.")
                conn.close()
                return
            cursor.execute("UPDATE produse SET stoc = stoc - ? WHERE id = ?", (cantitate, produs_id))

        cursor.execute("DELETE FROM cos WHERE username = ?", (self.username,))
        conn.commit()
        conn.close()

        print("\nComanda a fost plasată cu succes! Mulțumim pentru cumpărături.")
        print("Nu uita să lași o recenzie pentru produsele comandate!")
        input("Apasă Enter pentru a reveni la meniul principal.")

    @staticmethod
    def valideaza_cupon(cupon):
        cupon_valid = {
            "DISCOUNT10": 10,
            "DISCOUNT20": 20,
            "DISCOUNT30": 30,
        }
        return cupon_valid.get(cupon.upper(), None)
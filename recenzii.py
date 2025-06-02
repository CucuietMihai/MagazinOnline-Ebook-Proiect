import sqlite3

class Recenzie:
    """
    Clasa care gestioneaza recenziile si evaluarile adaugate de utilizatori pentru produse.
    """

    def __init__(self, username, rating, comentariu):
        """
        Initializeaza un obiect de tip Recenzie.
        """
        self.username = username
        self.rating = rating
        self.comentariu = comentariu

    @staticmethod
    def init_db():
        """
        Creeaza tabela recenzii in baza de date daca nu exista deja.
        """
        conn = sqlite3.connect("magazin_ebook.db")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recenzii (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produs_id INTEGER,
                username TEXT,
                rating INTEGER,
                comentariu TEXT
            )
        ''')
        conn.commit()
        conn.close()

    @staticmethod
    def adauga(username, produs_id):
        """
        Permite adaugarea unei recenzii pentru un anumit produs.
        Se valideaza rating-ul intre 1 si 5.
        """
        try:
            rating = int(input("Rating (1-5): "))
            if not 1 <= rating <= 5:
                print("Rating invalid.")
                return
        except ValueError:
            print("Rating invalid.")
            return

        comentariu = input("Comentariu: ")
        conn = sqlite3.connect("magazin_ebook.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO recenzii (produs_id, username, rating, comentariu) VALUES (?, ?, ?, ?)",
                       (produs_id, username, rating, comentariu))
        conn.commit()
        conn.close()
        print("Recenzia a fost adaugata.")

    @staticmethod
    def vezi(produs_id):
        """
        Afiseaza toate recenziile existente pentru un anumit produs.
        """
        conn = sqlite3.connect("magazin_ebook.db")
        cursor = conn.cursor()
        cursor.execute("SELECT username, rating, comentariu FROM recenzii WHERE produs_id = ?", (produs_id,))
        recenzii = cursor.fetchall()
        conn.close()
        for r in recenzii:
            print(f"{r[0]} | {r[1]}/5\nComentariu: {r[2]}\n{'-'*30}")

    def afiseaza(self):
        """
        Afiseaza sumarul obiectului Recenzie (poate fi folosit daca vei extinde sistemul pe viitor).
        """
        print(f"Recenzie: {self.rating}/5 de la {self.username} - {self.comentariu}")

import sqlite3
from abc import ABC, abstractmethod


#Clasa abstracta pentru orice persoana care poate exista in sistem.
class Persoana(ABC):

    # Metoda abstracta logout care trebuie implementata de clasele copil.
    @abstractmethod
    def logout(self):
        pass

#Clasa care defineste un utilizator obisnuit al aplicatiei.
class Utilizator(Persoana):

    def __init__(self, username, email=None, parola=None):
        self.username = username
        self.__email = email
        self.__parola = parola

    # Creeaza tabela utilizatori in baza de date daca nu exista.
    @staticmethod
    def init_db():
        conn = sqlite3.connect('magazin_ebook.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS utilizatori (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                parola TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    # Permite inregistrarea unui utilizator nou in sistem.
    @staticmethod
    def inregistrare():
        username = input("Alege un nume de utilizator: ")
        email = input("Introduceti un email: ")
        parola = input("Alege o parola: ")

        conn = sqlite3.connect('magazin_ebook.db')
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO utilizatori (username, email, parola) VALUES (?, ?, ?)",
                           (username, email, parola))
            conn.commit()
            print("Inregistrare reusita!")
            return Utilizator(username, email, parola)
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")
        finally:
            conn.close()
        return None

    # Permite autentificarea utilizatorilor existenti.
    @staticmethod
    def login():
        username = input("Username: ")
        parola = input("Parola: ")

        conn = sqlite3.connect("magazin_ebook.db")
        cursor = conn.cursor()

        cursor.execute("SELECT email, parola FROM utilizatori WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and parola == user[1]:
            print(f"Bine ai venit, {username}!")
            return Utilizator(username, user[0], parola)
        else:
            print("Date de autentificare incorecte.")
            return None

    # Realizeaza delogarea utilizatorului curent.
    def logout(self):
        print(f"{self.username} a fost delogat.")

    # Returneaza emailul utilizatorului.
    def get_email(self):
        return self.__email

    # Permite setarea unui nou email (cu validare simpla).
    def set_email(self, email):
        if "@" in email:
            self.__email = email
        else:
            print("Email invalid.")

    # Permite setarea unei noi parole (minim 6 caractere).
    def set_parola(self, parola):
        if len(parola) >= 6:
            self.__parola = parola
        else:
            print("Parola prea scurta.")

#Clasa Admin care mosteneste Utilizator si are drepturi speciale.
class Admin(Utilizator):

    def __init__(self, username, email=None, parola=None):
        super().__init__(username, email, parola)

    # Sterge un produs din baza de date dupa ID (functie speciala pentru admin).
    @staticmethod
    def sterge_produs_direct(produs_id):
        conn = sqlite3.connect("magazin_ebook.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM produse WHERE id = ?", (produs_id,))
        conn.commit()
        conn.close()
        print(f"[ADMIN] Produsul cu ID-ul {produs_id} a fost sters de admin.")

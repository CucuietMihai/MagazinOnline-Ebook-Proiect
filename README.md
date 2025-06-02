
Magazin eBook

Aceasta este o aplicatie de tip magazin online pentru vanzarea de carti in format digital (eBook)


Functionalitati principale


- Autentificare utilizatori (inregistrare, login, logout)
- Listare produse si detalii produs
- Cautare produse dupa cuvinte cheie
- Grupare produse pe categorii
- Adaugare produse in cosul de cumparaturi
- Plasare comenzi (cu actualizarea stocului)
- Gestiune inventar (stoc, adaugare, stergere produse)
- Reduceri si cupoane promotionale
- Formular de contact (scrie intr-un fisier `mesaje_contact.txt`)
- Sistem de evaluare si recenzii pentru produse


Structura aplicatiei


- `meniu_principal.py` – punctul de pornire al aplicatiei
- `utilizatori.py` – clasa `Utilizator` (autentificare, logout)
- `produse.py` – clasa `Produs` (initializare DB, listare, detalii, adaugare, stergere, cautare)
- `cos_cumparaturi.py` – clasa `CosCumparaturi` (cosul fiecarui utilizator)
- `recenzii.py` – clasa `Recenzie` (adaugare, vizualizare recenzii)
- `contact.py` – functie simpla pentru trimitere mesaj
- `magazin_ebook.db` – baza de date SQLite folosita de aplicatie


Cum rulezi aplicatia


1. Ruleaza fisierul principal:

  meniu_principal.py

2. Navigheaza prin meniuri pentru a interactiona cu aplicatia.


Fisiere generate


- magazin_ebook.db – baza de date cu utilizatori, produse, cosuri, recenzii
- mesaje_contact.txt – fisier cu mesajele trimise prin formularul de contact



CUCUIET MIHAI MARIAN
Proiect final pentru examen dupa cursul urmat de la HelloITFactory



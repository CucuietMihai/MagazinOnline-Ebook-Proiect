# Permite trimiterea unui mesaj de contact catre administratorul aplicatiei.
# Mesajele sunt salvate local intr-un fisier text.

def formular_contact():
    print("\n--- Formular Contact ---")
    nume = input("Nume: ")
    email = input("Email: ")
    mesaj = input("Mesajul tau: ")

    # Salvam mesajul in fisier text
    with open("mesaje_contact.txt", "a") as f:
        f.write(f"Nume: {nume}\nEmail: {email}\nMesaj: {mesaj}\n{'-'*40}\n")

    print("Mesajul tau a fost trimis. Iti multumim!")

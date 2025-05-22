def formular_contact():
    print("\n--- Formular Contact ---")
    nume = input("Nume: ")
    email = input("Email: ")
    mesaj = input("Mesajul tau: ")

    with open("mesaje_contact.txt", "a") as f:
        f.write(f"Nume: {nume}\nEmail: {email}\nMesaj: {mesaj}\n{'-'*40}\n")

    print("Mesajul tau a fost trimis. Iti multumim!")

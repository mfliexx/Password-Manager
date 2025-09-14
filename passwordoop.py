import pyfiglet
from colorama import Fore, init
from cryptography.fernet import Fernet
import os


init(autoreset=True)

KEY_FILE = "key.key"

if not os.path.exists(KEY_FILE):
   key = Fernet.generate_key()
   with open(KEY_FILE, "wb") as f:
        f.write(key)

else:
    with open(KEY_FILE, "rb") as f:
        key = f.read()

cipher = Fernet(key)


class PasswordEntry:
    def __init__(self, service, login, password):
        self.service = service
        self.login = login
        self.password = password

    def __str__(self):
        decrypted_password = cipher.decrypt(self.password).decode()
        return f"{self.service}: {self.login} / {decrypted_password}"
    
class PasswordManager:

    entries = []

    def add_entry(self, service, login, password):
        encrypted_password = cipher.encrypt(password.encode())
        entry = PasswordEntry(service, login, encrypted_password)
        self.entries.append(entry)

    def list_entries(self):
        for entry in self.entries:
            print(entry)

    def find_entry(self, service):
        for entry in self.entries:
            if entry.service == service:
                return entry
        return None
    
    def delete_entry(self, service):
        entry = self.find_entry(service)
        if entry:
            self.entries.remove(entry)
            return True
        return False
    
manager = PasswordManager()

while True:
    print(Fore.RED + pyfiglet.figlet_format("Password Manager"))
    print(Fore.LIGHTBLACK_EX + "1. Add Entry")
    print(Fore.LIGHTBLACK_EX + "2. List Entries")
    print(Fore.LIGHTBLACK_EX + "3. Find Entry")
    print(Fore.LIGHTBLACK_EX + "4. Delete Entry")
    print(Fore.LIGHTRED_EX+ "5. Exit")

    choice = input(Fore.LIGHTWHITE_EX + "Choose an option: ")

    if choice == "1":
        service = input("Service: ")
        login = input("Login: ")
        password = input("Password: ")
        manager.add_entry(service, login, password)
        print(Fore.LIGHTBLACK_EX + "Entry added.")
       

    if choice == "2":
        manager.list_entries()

    if choice == "3":
        service = input("Service to find")
        entry = manager.find_entry(service)
        if entry:
            print(entry)
        else:
            print(Fore.LIGHTRED_EX + "Entry not found.")
            

    if choice == "4":
        service = input("Service to delete: ")
        if manager.delete_entry(service):
            print("Entry deleted.")
        else:
            print(Fore.LIGHTRED_EX + "Entry not found.")
        


    if choice == "5":
        break




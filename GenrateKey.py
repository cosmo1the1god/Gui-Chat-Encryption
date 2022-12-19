from cryptography.fernet import Fernet

key = Fernet.generate_key()

# Instance the Fernet class with the key


with open("key.mp", "wb") as file:
    file.write(key)


import json
import os
import cryptography
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def encrypt_data(data, key, iv):
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return encrypted_data

def decrypt_data(encrypted_data, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data

def save_encrypted_dict_to_file(data_dict, output_filename, password):
    json_string = json.dumps(data_dict)
    data = json_string.encode('utf-8')

    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())

    iv = os.urandom(16)
    encrypted_data = encrypt_data(data, key, iv)

    with open(output_filename, 'wb') as file:
        file.write(salt + iv + encrypted_data)

def load_encrypted_dict_from_file(input_filename, password):
    with open(input_filename, 'rb') as file:
        salt = file.read(16)
        iv = file.read(16)
        encrypted_data = file.read()

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())

    decrypted_data = decrypt_data(encrypted_data, key, iv)
    json_string = decrypted_data.decode('utf-8')
    return json.loads(json_string)

# Beispielhafte Verwendung:

# Speichern eines Dictionaries als verschlüsselte Datei
data_dict = {'name': 'John Doe', 'age': 30, 'city': 'New York'}
output_filename = 'encrypted_data.json'
password = 'strong_password123'
save_encrypted_dict_to_file(data_dict, output_filename, password)

# Laden eines Dictionaries aus einer verschlüsselten Datei
loaded_dict = load_encrypted_dict_from_file(output_filename, password)
print(loaded_dict)

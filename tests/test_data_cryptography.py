# pylint: disable=C
import unittest
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from source.data_cryptography import encrypt_data, decrypt_data, save_encrypted_dict_to_file, load_encrypted_dict_from_file

class TestEncryptionModule(unittest.TestCase):

    def setUp(self):
        self.data = b'This is a test.'
        self.password = 'strong_password123'
        self.data_dict = {'name': 'John Doe', 'age': 30, 'city': 'New York'}
        self.filename = 'test_encrypted_file.json'
        self.salt = os.urandom(16)
        self.iv = os.urandom(16)
        self.kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
            backend=default_backend()
        )
        self.key = self.kdf.derive(self.password.encode())

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_encrypt_data(self):
        encrypted_data = encrypt_data(self.data, self.key, self.iv)
        self.assertNotEqual(encrypted_data, self.data)

    def test_decrypt_data(self):
        encrypted_data = encrypt_data(self.data, self.key, self.iv)
        decrypted_data = decrypt_data(encrypted_data, self.key, self.iv)
        self.assertEqual(decrypted_data, self.data)

    def test_save_encrypted_dict_to_file(self):
        save_encrypted_dict_to_file(self.data_dict, self.filename, self.password)
        self.assertTrue(os.path.exists(self.filename))

    def test_load_encrypted_dict_from_file(self):
        save_encrypted_dict_to_file(self.data_dict, self.filename, self.password)
        loaded_dict = load_encrypted_dict_from_file(self.filename, self.password)
        self.assertEqual(loaded_dict, self.data_dict)

    def test_invalid_password(self):
        save_encrypted_dict_to_file(self.data_dict, self.filename, self.password)
        with self.assertRaises(Exception):
            load_encrypted_dict_from_file(self.filename, 'wrong_password')

if __name__ == '__main__':
    unittest.main()

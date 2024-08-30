# pylint: disable=C
import unittest
import string
from source.password_generation import generate_password

class TestGeneratePassword(unittest.TestCase):
    def test_length_only(self):
        options = {'length': 8, 'use_uppercase': False, 'use_lowercase': True, 'use_digits': False, 'use_special': False}
        password = generate_password(options)
        self.assertEqual(len(password), 8)
        self.assertTrue(all(c.islower() for c in password))

    def test_uppercase_inclusion(self):
        options = {'length': 8, 'use_uppercase': True, 'use_lowercase': False, 'use_digits': False, 'use_special': False}
        password = generate_password(options)
        self.assertTrue(any(c.isupper() for c in password))

    def test_lowercase_inclusion(self):
        options = {'length': 8, 'use_uppercase': False, 'use_lowercase': True, 'use_digits': False, 'use_special': False}
        password = generate_password(options)
        self.assertTrue(any(c.islower() for c in password))

    def test_digits_inclusion(self):
        options = {'length': 8, 'use_uppercase': False, 'use_lowercase': False, 'use_digits': True, 'use_special': False}
        password = generate_password(options)
        self.assertTrue(any(c.isdigit() for c in password))

    def test_special_chars_inclusion(self):
        options = {'length': 8, 'use_uppercase': False, 'use_lowercase': False, 'use_digits': False, 'use_special': True}
        password = generate_password(options)
        self.assertTrue(any(c in "!@#$%^&*()_+[]{}|;:,.<>?" for c in password))

    def test_exclude_chars(self):
        options = {'length': 8, 'use_uppercase': True, 'use_lowercase': True, 'use_digits': True, 'use_special': True, 'exclude_chars': 'aeiou'}
        password = generate_password(options)
        self.assertTrue(all(c not in 'aeiou' for c in password))

    def test_enforce_pattern(self):
        options = {'length': 8, 'use_uppercase': True, 'use_lowercase': True, 'use_digits': True, 'use_special': True, 'enforce_pattern': 'ULDS'}
        password = generate_password(options)
        self.assertTrue(any(c.isupper() for c in password))
        self.assertTrue(any(c.islower() for c in password))
        self.assertTrue(any(c.isdigit() for c in password))
        self.assertTrue(any(c in string.punctuation for c in password))

    def test_empty_charset_error(self):
        options = {'length': 8, 'use_uppercase': False, 'use_lowercase': False, 'use_digits': False, 'use_special': False}
        with self.assertRaises(ValueError):
            generate_password(options)

    def test_invalid_pattern_char(self):
        options = {'length': 8, 'use_uppercase': True, 'use_lowercase': True, 'use_digits': True, 'use_special': True, 'enforce_pattern': 'ULX'}
        with self.assertRaises(ValueError):
            generate_password(options)

    def test_pattern_no_valid_chars(self):
        options = {'length': 8, 'use_uppercase': False, 'use_lowercase': False, 'use_digits': True, 'use_special': False, 'enforce_pattern': 'U'}
        with self.assertRaises(ValueError):
            generate_password(options)


if __name__ == '__main__':
    unittest.main()

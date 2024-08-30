"""
This module provides a function for generating secure, random passwords.
The passwords can be generated based on various criteria such as length, uppercase/lowercase usage, digits, special characters, and a custom pattern.
"""

import random
import string

def generate_password(criteria: dict) -> str:
    """
    Generates a random password based on the specified criteria.

    :param length: Length of the password.
    :param use_uppercase: Whether to include uppercase letters.
    :param use_lowercase: Whether to include lowercase letters.
    :param use_digits: Whether to include digits.
    :param use_special: Whether to include special characters.
    :param exclude_chars: Characters to exclude from the password.
    :param enforce_pattern: A pattern to enforce in the password (e.g., "ULDS" for 1 Uppercase, 1 Lowercase, 1 Digit, 1 Special).
    :return: The generated password.
    """

    length = criteria['length']
    use_uppercase = criteria['use_uppercase']
    use_lowercase = criteria['use_lowercase']
    use_digits = criteria['use_digits']
    use_special = criteria['use_special']
    exclude_chars = criteria.get('exclude_chars', '')
    enforce_pattern = criteria.get('enforce_pattern', '')
    # Erstellen des möglichen Zeichensatzes
    characters = ''
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
    if use_special:
        characters += string.punctuation
    # Ausschluss bestimmter Zeichen
    if exclude_chars:
        characters = ''.join(c for c in characters if c not in exclude_chars)
    # Sicherstellen, dass der Zeichensatz nicht leer ist
    if not characters:
        raise ValueError("Zeichensatz ist leer. Bitte mindestens eine Zeichengruppe einschließen.")
    # Generierung des Passworts
    if enforce_pattern:
        password = []
        pattern_dict = {'U': string.ascii_uppercase, 'L': string.ascii_lowercase, 'D': string.digits, 'S': string.punctuation}
        # Für jedes Musterzeichen das entsprechende Zeichen hinzufügen
        for char in enforce_pattern:
            if char in pattern_dict:
                # Ausschluss bestimmter Zeichen aus dem Musterzeichensatz
                valid_chars = [c for c in pattern_dict[char] if c not in exclude_chars]
                if not valid_chars:
                    raise ValueError(f"Kein gültiges Zeichen für das Musterzeichen '{char}'.")
                password.append(random.choice(valid_chars))
            else:
                raise ValueError(f"Ungültiges Musterzeichen '{char}' in enforce_pattern.")
        # Restliche Zeichen zufällig hinzufügen
        remaining_length = length - len(password)
        password += random.choices(characters, k=remaining_length)
        # Passwort zufällig mischen
        random.shuffle(password)
        #muss man sich dann überlegen ob man das muster so haben will wie man es eingibt oder das das nur dafür da ist das auf jeden fall davon welche vorkommen.
        return ''.join(password)
    # Wenn kein Muster erzwungen wird, ein einfaches zufälliges Passwort generieren
    return ''.join(random.choice(characters) for _ in range(length))


# Beispielverwendung:
options = {
    'length': 16,
    'use_uppercase': True,
    'use_lowercase': True,
    'use_digits': True,
    'use_special': True,
    'exclude_chars': 'bums',
    'enforce_pattern': 'ULDS'
}
print(generate_password(options))

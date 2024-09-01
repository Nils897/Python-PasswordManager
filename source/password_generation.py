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
    characters = ''
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
    if use_special:
        characters += string.punctuation    
    if exclude_chars:
        characters = ''.join(c for c in characters if c not in exclude_chars)    
    if not characters:
        raise ValueError("Zeichensatz ist leer. Bitte mindestens eine Zeichengruppe einschließen.")    
    if enforce_pattern:
        password = []
        pattern_dict = {'U': string.ascii_uppercase, 'L': string.ascii_lowercase, 'D': string.digits, 'S': string.punctuation}        
        for char in enforce_pattern:
            if char in pattern_dict:                
                valid_chars = [c for c in pattern_dict[char] if c not in exclude_chars]
                if not valid_chars:
                    raise ValueError(f"Kein gültiges Zeichen für das Musterzeichen '{char}'.")
                password.append(random.choice(valid_chars))
            else:
                raise ValueError(f"Ungültiges Musterzeichen '{char}' in enforce_pattern.")        
        remaining_length = length - len(password)
        password += random.choices(characters, k=remaining_length)        
        random.shuffle(password)
        return ''.join(password)
    return ''.join(random.choice(characters) for _ in range(length))
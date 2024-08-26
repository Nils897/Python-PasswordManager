import re, hashlib, requests

def isPasswordCorrect(password):

    if len(password) < 8:
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[_!@#$%^&*(),.?":{}|<>-]', password):
        return False
    if isPasswordPwned(password):
        return False
    return True

def isPasswordPwned(password):
    sha1_hashed_password = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix_hashed_password = sha1_hashed_password[:5] 
    suffix_hashed_password = sha1_hashed_password[5:]
    
    result = requestAPI(prefix_hashed_password)
    if result is None:
        print("Could not check the password due to API issues.")
        return False
    
    hash_suffixes = (line.split(':') for line in result.splitlines())
    for returned_suffix, count in hash_suffixes:
        if returned_suffix == suffix_hashed_password:
            return True
    return False

def requestAPI(prefix_hashed_password):
    url = f'https://api.pwnedpasswords.com/range/{prefix_hashed_password}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error contacting API: {e}")
        return None
"""
This module provides functions for managing account and password data.
It allows creating, updating, and storing account information in a JSON file,
with a terminal-based user interface using the `curses` library.

Functions:
- create_accounts_file: Ensures the 'data.json' file exists or creates it if missing.
- change_data: Allows users to update account details via terminal input.
- safe_changed_data: Saves updated account data to the JSON file.
- safe_register_data: Registers a new account and stores it in the JSON file.
- read_data_json: returns the data from the JSON file.
"""
import curses
import json
import os
import datetime
from typing import Any
#from source.password_manager_framework import choice_function, input_function
#from source.password import show_password, hash_password
#from source.validation import is_password_correct

def create_accounts_file() -> None:
    """
    Checks if 'data.json' exists in the current directory.
    If not, it creates the file with an initial empty accounts structure.
    """
    if os.path.exists('./data.json'):
        pass
    else:
        data: dict
        data = {
            "accounts": {
            }
        }
        with open('./data.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii = False, indent = 4)

def change_data(stdscr: curses.window, height: int, width: int, mail: str, name: str, url: str, notes: str, password: str, data_to_be_shown: str, data: dict) -> None:
    """
    Manages the process of updating account details via user input in a terminal interface.
    
    Allows the user to change the name, URL, notes, and password of a specified account entry.
    Updates the displayed information and handles saving or discarding changes based on user choices.
    
    Args:
        stdscr: The curses window object used for displaying and capturing user input.
        height (int): The height of the terminal window.
        width (int): The width of the terminal window.
        mail (str): The email associated with the account.
        name (str): The current name of the password entry.
        url (str): The current URL associated with the entry.
        notes (str): The current notes for the entry.
        password (str): The current password for the entry.
        data_to_be_shown: Data to be displayed to the user.
        data (dict): The account data loaded from the JSON file.

    Return:
        None
    """
    stdscr.clear()
    x = width //2
    y = height //2
    text1 = "Einträge ändern:"
    go, go2 = True, True
    ky = 0
    old_name = name
    is_name_changed = False
    pair_number = [1, 2, 2, 2, 2, 2]
    stdscr.addstr(y - 10, x - len(text1), text1, curses.color_pair(2) | curses.A_BOLD)
    stdscr.addstr(y - 6, x - 30, f"Alter Name: {name}", curses.color_pair(2) | curses.A_BOLD)
    stdscr.addstr(y - 2, x - 30, f"Alter Link {url}", curses.color_pair(2) | curses.A_BOLD)
    stdscr.addstr(y + 2, x - 30, f"Alte Notiz: {notes}", curses.color_pair(2) | curses.A_BOLD)
    stdscr.addstr(y + 6, x - 30, f"Altes Passwort: {password}", curses.color_pair(2) | curses.A_BOLD)
    stdscr.refresh()
    while go2:
        while go:
            stdscr.addstr(y - 5, x - 30, "Neuer Name:", curses.color_pair(pair_number[0]) | curses.A_BOLD)
            stdscr.addstr(y - 1, x - 30, "Neuer Link:", curses.color_pair(pair_number[1]) | curses.A_BOLD)
            stdscr.addstr(y + 3, x - 30, "Neue Notiz:", curses.color_pair(pair_number[2]) | curses.A_BOLD)
            stdscr.addstr(y + 7, x - 30, "Neues Passwort:", curses.color_pair(pair_number[3]) | curses.A_BOLD)
            stdscr.addstr(y + 10, x - 30, "Speichern", curses.color_pair(pair_number[4]) | curses.A_BOLD)
            stdscr.addstr(y + 12, x - 30, "Zurück", curses.color_pair(pair_number[5]) | curses.A_BOLD)
            stdscr.refresh()
            ky, pair_number, go = choice_function(stdscr, ky, pair_number, go)
        if ky == 5:
            go2 = False
            show_password(stdscr, data, mail, data_to_be_shown, y, x, height, width)
        elif ky == 4:
            go2 = False
            data = safe_changed_data(mail, name, url, notes, password, old_name, is_name_changed)
            show_password(stdscr, data, mail, data_to_be_shown, y, x, height, width)
        else:
            go = True
            is_password = True
            if ky == 0:
                input_y, input_x = y - 5, x - 28 + len("Neuer Name:")
                stdscr.move(input_y, input_x)
                is_password = False
            elif ky == 1:
                input_y, input_x = y - 1, x - 28 + len("Neuer Link:")
                stdscr.move(input_y, input_x)
                is_password = False
            elif ky == 2:
                input_y, input_x = y + 3, x - 28 + len("Neue Notiz:")
                stdscr.move(input_y, input_x)
                is_password = False
            elif ky == 3:
                input_y, input_x = y + 7, x - 28 + len("Neues Passwort:")
                stdscr.addstr(y + 8, x - 30, " " * width)
                stdscr.move(input_y, input_x)
                is_password = True
            curses.curs_set(1)
            user_input = input_function(stdscr, input_y, input_x, is_password)
            curses.curs_set(0)
            if ky == 0:
                new_name = user_input
                if new_name != name:
                    old_name = name
                    name = new_name
                    is_name_changed = True
            elif ky == 1:
                new_url = user_input
                if new_url != url:
                    url = new_url
            elif ky == 2:
                new_notes = user_input
                if new_notes != notes:
                    notes = new_notes
            elif ky == 3:
                new_password = user_input
                if new_password in data["accounts"][mail]["passwords"][name]["oldpasswordlist"]:
                    stdscr.addstr(y + 8, x - 30, "Passwort schon mal verwendet", curses.color_pair(3))
                    stdscr.refresh()
                elif is_password_correct(new_password):
                    password = new_password
                else:
                    stdscr.addstr(y + 8, x - 30, "Passwort unsicher", curses.color_pair(3))
                    stdscr.refresh()
    stdscr.getch()

def safe_changed_data(mail: str, name: str, url: str, notes: str, password: str, old_name: str, is_name_changed: bool) -> Any:
    """
    Updates account data in 'data.json' with new information for a given password entry.
    
    If the name of the entry has changed, updates the entry with a new name and transfers
    old password history. If the name hasn't changed, only updates the URL, notes, and password.
    Also updates the date of the last change.
    
    Args:
        mail (str): The email associated with the account.
        name (str): The new or existing name of the password entry.
        url (str): The updated URL associated with the entry.
        notes (str): The updated notes for the entry.
        password (str): The updated password for the entry.
        old_name (str): The old name of the password entry (used if the name has changed).
        is_name_changed (bool): Flag indicating if the entry name has changed.
        
    Returns:
        dict: The updated data structure from 'data.json'.
    """
    with open('./data.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    if is_name_changed:
        old_password_list = data["accounts"][mail]["passwords"][old_name]["oldpasswordlist"]
        data["accounts"][mail]["passwords-list"].remove(old_name)
        data["accounts"][mail]["passwords-list"].append(name)
        new_name: dict[str, dict[str, Any]] = {}
        new_name = {
            name: {
                "name": name,
                "password": password,
                "url": url,
                "text": notes,
                "oldpasswordlist": []
                }
            }
        for password_in_old_password_list in old_password_list:
            new_name[name]["oldpasswordlist"].append(password_in_old_password_list)
        if password not in old_password_list:
            new_name[name]["oldpasswordlist"].append(password)
        del data["accounts"][mail]["passwords"][old_name]
        data["accounts"][mail]["passwords"].update(new_name)
    else:
        old_password_list = data["accounts"][mail]["passwords"][name]["oldpasswordlist"]
        new_url = { "url": url }
        new_notes = { "text": notes }
        new_password = { "password": password }
        data["accounts"][mail]["passwords"][name].update(new_url)
        data["accounts"][mail]["passwords"][name].update(new_notes)
        data["accounts"][mail]["passwords"][name].update(new_password)
        if password not in old_password_list:
            data["accounts"][mail]["passwords"][name]["oldpasswordlist"].append(password)
    new_date_of_last_change = datetime.datetime.now()
    new_date_of_last_change_format = new_date_of_last_change.strftime("%d.%m.%Y %H:%M")
    new_date_of_last_change_format_to_dic = { "dateoflastchange": new_date_of_last_change_format }
    data["accounts"][mail]["passwords"][name].update(new_date_of_last_change_format_to_dic)
    with open('./data.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent = 4)
    return data



def safe_register_data(mail: str, password: str) -> None:
    """
    Registers a new account by adding it to the JSON data file.

    Hashes the provided password, creates a new account entry, and updates
    the 'data.json' file with this new account information.

    Args:
        mail (str): The email address associated with the new account.
        password (str): The master password for the new account.

    Returns:
        None
    """
    hashed_password = hash_password(password)
    new_data = {
        mail: {
            "mail": mail,
            "master-password": hashed_password,
            "passwords-list": [],
            "passwords": { 
            }
        }
    }
    with open('./data.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    data["accounts"].update(new_data)
    with open('./data.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent = 4)

def read_data_json() -> Any:
    """
    Reads and returns the data from the JSON file.

    Opens the 'data.json' file, loads its contents into a Python dictionary, 
    and returns the dictionary.

    Returns:
        dict: The data loaded from 'data.json'.
    """
    with open('./data.json', 'r', encoding = 'utf-8') as json_file:
        data = json.load(json_file)
    return data

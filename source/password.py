"""
This module provides following functions:
 - add a new password
 - safe the new password data
 - show a specific password
 - delete a specific password
 - hash a password
"""
import curses
import json
import hashlib
import datetime
from typing import Any
from source.validation import is_password_correct
from main import password_manager



def add_new_password(stdscr: curses.window, mail: str, height: int, width: int, y: int, x: int) -> None:
    from source.password_manager_framework import choice_function, input_function
    """
    Allows the user to add a new password entry through a terminal interface.

    Prompts for and collects details including name, URL, notes, and password.
    Validates the input and saves the new entry if all required fields are filled.

    Args:
        stdscr: The curses window object used for displaying and capturing user input.
        data (dict): The current account data loaded from the JSON file.
        mail (str): The email associated with the account.
        height (int): The height of the terminal window.
        width (int): The width of the terminal window.
        y (int): The vertical position in the terminal to start displaying input fields.
        x (int): The horizontal position in the terminal to start displaying input fields.

    Returns:
        None
    """
    stdscr.clear()
    text1 = "Name:"
    text2 = "URL:"
    text3 = "Notiz:"
    text4 = "Passwort:"
    text5 = "Neues Passwort anlegen:"
    pair_number = [1, 2, 2, 2, 2, 2]
    go, go2 = True, True
    ky = 0
    url, notes = "", ""
    name: str = ""
    password: str = ""
    name_available, password_available = False, False
    stdscr.addstr(y - 10, x - (len(text5) //2), text5, curses.color_pair(2) | curses.A_BOLD)
    stdscr.refresh()
    while go2:
        while go:
            stdscr.addstr(y - 6, x - 20, text1, curses.color_pair(pair_number[0]) | curses.A_BOLD)
            stdscr.addstr(y - 4, x - 20, text2, curses.color_pair(pair_number[1]) | curses.A_BOLD)
            stdscr.addstr(y - 2, x - 20, text3, curses.color_pair(pair_number[2]) | curses.A_BOLD)
            stdscr.addstr(y, x - 20, text4, curses.color_pair(pair_number[3]) | curses.A_BOLD)
            stdscr.addstr(y + 4, x - 20, "Speichern", curses.color_pair(pair_number[4]) | curses.A_BOLD)
            stdscr.addstr(y + 10, x - 20, "Zurück", curses.color_pair(pair_number[5]) | curses.A_BOLD)
            stdscr.refresh()
            ky, pair_number, go = choice_function(stdscr, ky, pair_number, go)
        if ky == 5:
            password_manager(stdscr, height, width, mail)
        elif ky == 4 and name_available and password_available:
            go2 = False
            time_of_access = datetime.datetime.now()
            time_of_access_format = time_of_access.strftime("%d.%m.%Y %H:%M")
            new_data: dict[str, dict[str, Any]] = {}
            new_data = {
                name: {
                    "name": name,
                    "password": password,
                    "url": url,
                    "text": notes,
                    "oldpasswordlist": [],
                    "dateoffirstaccess": time_of_access_format,
                    "dateoflastchange": time_of_access_format
                }
            }
            new_data[name]["oldpasswordlist"].append(password)
            safe_new_password_data(new_data, mail, name)
            password_manager(stdscr, height, width, mail)
        else:
            go = True
            if ky == 0:
                input_y, input_x = y - 6, x - 18 + len(text1)
                stdscr.move(input_y, input_x)
                is_password = False
            elif ky == 1:
                input_y, input_x = y - 4, x - 18 + len(text2)
                stdscr.move(input_y, input_x)
                is_password = False
            elif ky == 2:
                input_y, input_x = y - 2, x - 18 + len(text3)
                stdscr.move(input_y, input_x)
                is_password = False
            elif ky == 3:
                input_y, input_x = y, x - 18 + len(text4)
                stdscr.move(input_y, input_x)
                is_password = True
            curses.curs_set(1)
            user_input = input_function(stdscr, input_y, input_x, is_password)
            curses.curs_set(0)
            if ky == 0:
                name = user_input
                name_available = True
            elif ky == 1:
                url = user_input
            elif ky == 2:
                notes = user_input
            elif ky == 3:
                password = user_input
                if is_password_correct(password):
                    password_available = True

def safe_new_password_data(new_data: dict, mail: str, name: str) -> None:
    """
    Adds a new password entry to the account data and updates 'data.json'.

    Args:
        new_data (dict): The new password entry data to be added.
        mail (str): The email associated with the account.
        name (str): The name of the new password entry.

    Returns:
        None
    """
    with open('./data.json', 'r') as json_file:
        data = json.load(json_file)
    data["accounts"][mail]["passwords-list"].append(name)
    data["accounts"][mail]["passwords"].update(new_data)
    with open('./data.json', 'w') as json_file:
        json.dump(data, json_file, indent = 4)

def show_password(stdscr: curses.window, data: dict, mail: str, data_to_be_shown: str, y: int, x: int, height: int, width: int) -> None:
    from source.data import change_data
    from source.password_manager_framework import choice_function, input_function
    """
    Displays detailed information about a specific password entry and provides options
    to show the password, copy it, modify it, or delete it.

    Args:
        stdscr: The curses window object used for displaying information and capturing user input.
        data (dict): The account data loaded from the JSON file.
        mail (str): The email associated with the account.
        data_to_be_shown (str): The name of the password entry to display.
        y (int): The vertical position in the terminal to start displaying information.
        x (int): The horizontal position in the terminal to start displaying information.
        height (int): The height of the terminal window.
        width (int): The width of the terminal window.

    Returns:
        None
    """
    stdscr.clear()
    pair_number = [1, 2, 2, 2, 2]
    go, go2 = True, True
    ky = 0
    name = data['accounts'][mail]['passwords'][data_to_be_shown]['name']
    url = data['accounts'][mail]['passwords'][data_to_be_shown]['url']
    notes = data['accounts'][mail]['passwords'][data_to_be_shown]['text']
    password = data["accounts"][mail]["passwords"][data_to_be_shown]["password"]
    date_of_first_access = data['accounts'][mail]['passwords'][data_to_be_shown]['dateoffirstaccess']
    date_of_last_change = data['accounts'][mail]['passwords'][data_to_be_shown]['dateoflastchange']
    stdscr.addstr(y - 10, x - 30, f"Erstellt: {date_of_first_access}", curses.color_pair(4))
    stdscr.addstr(y - 10, x, f"Letzte Änderung: {date_of_last_change}", curses.color_pair(4))
    stdscr.addstr(y - 8, x - 10, f"Name: {name}", curses.color_pair(2) | curses.A_BOLD)
    stdscr.addstr(y - 2, x - 10, f"Link: {url}", curses.color_pair(2) | curses.A_BOLD)
    stdscr.addstr(y, x - 10, f"Notiz: {notes}", curses.color_pair(2) | curses.A_BOLD)
    stdscr.refresh()
    while go2:
        while go:
            stdscr.addstr(y - 6, x - 10, "Passwort anzeigen:", curses.color_pair(pair_number[0]) | curses.A_BOLD)
            stdscr.addstr(y - 4, x - 10, "Passwort kopieren", curses.color_pair(pair_number[1]) | curses.A_BOLD)
            stdscr.addstr(y + 4, x - 10, "Enträge ändern", curses.color_pair(pair_number[2]) | curses.A_BOLD)
            stdscr.addstr(y + 6, x - 10, "Enträge löschen", curses.color_pair(pair_number[3]) | curses.A_BOLD)
            stdscr.addstr(y + 8, x - 10, "Zurück", curses.color_pair(pair_number[4]) | curses.A_BOLD)
            ky, pair_number, go = choice_function(stdscr, ky, pair_number, go)
        if ky == 0:
            stdscr.addstr(y - 6, x - 10 + len("Passwort anzeigen") + 2, password)
            stdscr.refresh()
        if ky == 1:
            stdscr.addstr(y - 4, x - 10 + len("Passwort kopieren") + 2, "Passwort in Zwischenablage kopiert")
        elif ky == 2:
            go2 = False
            change_data(stdscr, height, width, mail, name, url, notes, password, data_to_be_shown, data)
        elif ky == 3:
            go2 = False
            delete_password(mail, data_to_be_shown)
            password_manager(stdscr, height, width, mail)
        elif ky == 4:
            go2 = False
            password_manager(stdscr, height, width, mail)
        go = True
    stdscr.getch()

def delete_password(mail: str, data_to_be_shown: str) -> None:
    """
    Deletes a specified password entry from the JSON data file.
    
    Removes the password entry and its name from the account's password list in 'data.json'.
    
    Args:
        mail (str): The email associated with the account.
        data_to_be_shown (str): The name of the password entry to be deleted.
    
    Returns:
        None
    """
    with open('./data.json', 'r') as json_file:
        data = json.load(json_file)
    del data["accounts"][mail]["passwords"][data_to_be_shown]
    data["accounts"][mail]["passwords-list"].remove(data_to_be_shown)
    with open('./data.json', 'w') as json_file:
        json.dump(data, json_file, indent = 4)

def hash_password(password: str) -> str:
    """
    Hashes the given password using SHA-256 and returns the hexadecimal digest.
    Args:password (str): The password to hash.
    Returns: str: The SHA-256 hash of the password.
    """
    sha_signature = hashlib.sha256(password.encode()).hexdigest()
    return sha_signature

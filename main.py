"""
This module is main.py
"""

import curses
import re
import sys
import json
import hashlib
import os
import datetime
from typing import Any
from source.password_validation import is_password_correct


def start_screen(stdscr: curses.window, height: int, width: int) -> str:
    """
    Displays the start screen of the application, allowing the user to either sign in, register a new account, or exit.

    The function sets up the initial menu with options for signing in, registering a new account, or exiting the application.
    It handles user input to navigate between options and select one. Based on the selection, it either calls the
    `signIn` function, the `register` function, or exits the program.

    Args:
        stdscr (curses.window): The curses window object used for displaying text and capturing user input.
        height (int): The height of the terminal window.
        width (int): The width of the terminal window.

    Returns:
        str: The email address of the user if they choose to sign in or register.
              This will be returned from the `signIn` or `register` functions.
              If the user chooses to exit, the function will terminate the program.
    """
    curses.curs_set(0)
    stdscr.clear()
    pair_number = [1, 2, 2]
    ky = 0
    text1 = "Anmelden"
    text2 = "Neuen Account anlegen"
    y = height // 2
    x = width
    #exit_text(stdscr, height, width)
    go = True
    while go:
        stdscr.addstr(y, (x - len(text1)) // 2, text1, curses.color_pair(pair_number[0]) | curses.A_BOLD)
        stdscr.addstr(y + 5, (x - len(text2)) // 2, text2, curses.color_pair(pair_number[1]) | curses.A_BOLD)
        stdscr.addstr(y + 8, (x - len("Beenden")) // 2, "Beenden", curses.color_pair(pair_number[2]) | curses.A_BOLD)
        stdscr.refresh()
        ky, pair_number, go = choice_function(stdscr, ky, pair_number, go)
    if ky == 0:
        mail = signIn(stdscr, height, width)
    elif ky == 1:
        mail = register(stdscr, height, width)
        start_screen(stdscr, height, width)
    elif ky == 2:
        sys.exit(0)
    return mail

def choice_function(stdscr: curses.window, ky: int, pair_number: list, go: bool) -> tuple:
    """
    Handles user input for navigation and selection in a menu.

    This function processes user input to navigate through menu options using arrow keys or to
    select an option using the Enter key. It updates the highlight state of menu items and
    determines whether to proceed based on user input.

    Args:
        stdscr (curses.window): The curses window object for capturing user input.
        ky (int): The index of the currently selected menu item.
        pair_number (list of int): A list representing the highlight state of each menu item.
        go (bool): A flag indicating whether the function should continue running.

    Returns:
        tuple: A tuple containing the updated index (ky), the updated highlight states (pair_number),
               and the updated flag (go).
    """
    ky_max = len(pair_number) - 1
    ky_min = 0
    key = stdscr.getch()
    if key == curses.KEY_DOWN and ky < ky_max: #ky -> key_y
        pair_number[ky] = 2
        pair_number[ky + 1] = 1
        ky += 1
    elif key == curses.KEY_UP and ky > ky_min:
        pair_number[ky - 1] = 1
        pair_number[ky] = 2
        ky -= 1
    elif key == 27:
        is_sure_to_exit_program(stdscr)
    elif key in [10, 13]: #Entertaste
        go = False
    #elif key == ord('q'):
        #break
    return ky, pair_number, go

def register(stdscr: curses.window, height: int, width: int) -> str:
    """
    Handles the user registration process for a new account.

    This function facilitates the creation of a new account by collecting and validating user input
    for email and master password. It ensures that the provided email is valid and the passwords
    meet the security criteria. Upon successful validation, the new account details are saved to
    the 'data.json' file.

    Args:
        stdscr (curses.window): The curses window object for rendering text.
        height (int): The height of the terminal window.
        width (int): The width of the terminal window.

    Returns:
        str: The email address associated with the newly registered account.
    """
    stdscr.clear()
    pair_number = [1, 2, 2, 2]
    ky = 0
    go = True
    text1 = "Neuen Account anlegen:"
    text2 = "E-Mail-Adresse:"
    text3 = "Master-Passwort:"
    text4 = "Master-Passwort nochmal eingeben:"
    text5 = "Zurück"
    y = height // 2
    x = width // 2
    stdscr.addstr(y - 8, x - (len(text1) // 2), text1, curses.color_pair(2) | curses.A_BOLD)
    go2 = True
    password1_available = False
    password2_available = False
    mail_correct = False
    password1_correct = False
    password2_correct = False
    exit_text(stdscr, height, width)
    while go2:
        while go:
            stdscr.addstr(y - 4, x - len(text2) - 8, text2, curses.color_pair(pair_number[0]) | curses.A_BOLD)
            stdscr.addstr(y, x - len(text3) - 8, text3, curses.color_pair(pair_number[1]) | curses.A_BOLD)
            stdscr.addstr(y + 4, x - len(text4) - 8, text4, curses.color_pair(pair_number[2]) | curses.A_BOLD)
            stdscr.addstr(y + 8, x - len(text5) - 8, text5, curses.color_pair(pair_number[3]) | curses.A_BOLD)
            stdscr.refresh()
            ky, pair_number, go = choice_function(stdscr, ky, pair_number, go)
        if ky == 3:
            go2 = False
            start_screen(stdscr, height, width)
        else:
            if ky == 0:
                stdscr.move(y - 4, x - 6)
                input_y, input_x = y - 4, x - 6
                is_password = False
            elif ky == 1:
                stdscr.move(y, x - 6)
                input_y, input_x = y, x - 6
                is_password = True
            elif ky == 2:
                stdscr.move(y + 4, x - 6)
                input_y, input_x = y + 4, x - 6
                is_password = True
            curses.curs_set(1)
            user_input = input_function(stdscr, input_y, input_x, is_password)
            curses.curs_set(0)
            if ky == 0:
                mail = user_input
                if is_mail_correct(mail):
                    mail_correct = True
                    stdscr.addstr(y - 4, x - 6 + len(mail) + 2, '\u2713')
                    stdscr.addstr(y - 3, x - 6, ' ' * len("Eingabe nicht korrekt!"))
                else:
                    mail_correct = False
                    stdscr.addstr(y - 3, x - 6, "Eingabe nicht korrekt!", curses.color_pair(3))
                    stdscr.addstr(y - 4, x - 6 + len(mail), ' ' * (width - x - 6 + len(mail)))
            elif ky == 1:
                password = user_input
                password1_available = True
            elif ky == 2:
                password2 = user_input
                password2_available = True
            if password1_available:
                word = password
                if not is_password_correct(word):
                    stdscr.addstr(y + 1, x, "Passwort muss 8 Zeichen lang, Klein-, Großbuchstaben, Zahlen, Sonderzeichen beinhalten", curses.color_pair(3))
                else:
                    password1_correct = True
            if password2_available:
                word = password2
                if not is_password_correct(word):
                    stdscr.addstr(y + 5, x, "Passwort muss 8 Zeichen lang, Klein-, Großbuchstaben, Zahlen, Sonderzeichen beinhalten", curses.color_pair(3))
                else:
                    password2_correct = True
            if mail_correct and password1_correct and password2_correct:
                go2 = False
            else:
                go = True
            stdscr.refresh()
            safe_register_data(mail, password)
    return mail

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
    with open('./data.json', 'r') as json_file:
        data = json.load(json_file)
    data["accounts"].update(new_data)
    with open('./data.json', 'w') as json_file:
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

def signIn(stdscr: curses.window, height: int, width: int) -> str:
    """
    Handles the user sign-in process by verifying email and master password.

    Displays prompts for email and master password, and validates the credentials
    against the stored data. Provides feedback on incorrect credentials and navigates 
    to the start screen if the user chooses to go back.

    Args:
        stdscr: The curses window object used for displaying and capturing user input.
        height (int): The height of the terminal window.
        width (int): The width of the terminal window.

    Returns:
        str: The email address if sign-in is successful, or the original email input.
    """
    stdscr.clear()
    data = read_data_json()
    text1 = "Anmelden:"
    text2 = "E-Mail-Adresse:"
    text3 = "Master-Passwort:"
    text4 = "Zurück"
    y = height // 2
    x = width // 2
    pair_number = [1, 2, 2]
    go, go2 = True, True
    ky = 0
    mail_correct, password_correct = False, False
    stdscr.addstr(y - 8, x - len(text1), text1, curses.color_pair(2) | curses.A_BOLD)
    exit_text(stdscr, height, width)
    stdscr.refresh()
    while go2:
        while go:
            stdscr.addstr(y - 4, x - len(text2) - 8, text2, curses.color_pair(pair_number[0]) | curses.A_BOLD)
            stdscr.addstr(y, x - len(text3) - 8, text3, curses.color_pair(pair_number[1]) | curses.A_BOLD)
            stdscr.addstr(y + 4, x - len(text4) - 8, text4, curses.color_pair(pair_number[2]) | curses.A_BOLD)
            stdscr.refresh()
            ky, pair_number, go = choice_function(stdscr, ky, pair_number, go)
        if ky == 2:
            go2 = False
            start_screen(stdscr, height, width)
        else:
            if ky == 0:
                stdscr.move(y - 4, x - 6)
                input_y, input_x = y - 4, x - 6
                is_password = False
            elif ky == 1:
                stdscr.move(y, x - 6)
                input_y, input_x = y, x - 6
                is_password = True
            curses.curs_set(1)
            user_input = input_function(stdscr, input_y, input_x, is_password)
            curses.curs_set(0)
            if ky == 0:
                mail = user_input
                if mail in data["accounts"]["accounts-list"]:
                    mail_correct = True
                else:
                    mail_correct = False
            if ky == 1:
                password = user_input
                hashed_password = hash_password(password)
                if hashed_password == data['accounts'][mail]['master-password']:
                    password_correct = True
                else:
                    password_correct = False
            if mail_correct and password_correct:
                go2 = False
                return mail
            else:
                go = True
                stdscr.addstr(y + 6, x - 20, "E-Mail oder Passwort nicht korrekt", curses.color_pair(4))
            stdscr.refresh()
    return mail

def password_manager(stdscr: curses.window, height: int, width: int, mail: str) -> None:
    """
    Manages the display and selection of password entries for a specific account.

    Shows a list of existing passwords and provides options to view details of a selected
    password or to add a new password entry.

    Args:
        stdscr: The curses window object used for displaying and capturing user input.
        height (int): The height of the terminal window.
        width (int): The width of the terminal window.
        mail (str): The email associated with the account whose passwords are being managed.

    Returns:
        None
    """
    stdscr.clear()
    y = height // 2
    x = width // 2
    ky = 0
    go = True
    data = read_data_json()
    passwords_list = data["accounts"][mail]["passwords-list"]
    passwords_list_sorted = sorted(passwords_list)
    pair_number = [1, 2]
    text1 = "Passwörter:"
    text2 = "neues Passwort hinzufügen"
    text3 = "Passwort anzeigen:"
    stdscr.addstr(y - 10, x - (len(text1) //2), text1, curses.color_pair(2) | curses.A_BOLD | curses.A_UNDERLINE)
    a = -4
    b = 1
    x_new = 5
    for passwords in passwords_list_sorted:
        stdscr.addstr(y + a, x_new, data["accounts"][mail]["passwords"][passwords]["name"], curses.color_pair(2) | curses.A_BOLD)
        a += 2
        b += 1
        if a == 20:
            x_new = 20
        stdscr.refresh()
    line = "-" * width
    stdscr.addstr(y - 5, 0, line)
    while go:
        stdscr.addstr(y - 8, x - len(text3) - 10, text3, curses.color_pair(pair_number[0]) | curses.A_BOLD)
        stdscr.addstr(y - 6, x - len(text2) - 10, text2, curses.color_pair(pair_number[1]) | curses.A_BOLD)
        ky, pair_number, go = choice_function(stdscr, ky, pair_number, go)
        stdscr.refresh()
    if ky == 0:
        is_password = False
        input_y, input_x = y - 8, x - 8
        stdscr.move(input_y, input_x)
        curses.curs_set(1)
        data_to_be_shown = input_function(stdscr, input_y, input_x, is_password)
        curses.curs_set(0)
        try:
            go = False
            show_password(stdscr, data, mail, data_to_be_shown, y, x, height, width)
        except KeyError:
            password_manager(stdscr, height, width, mail)
    else:
        add_new_password(stdscr, mail, height, width, y, x)


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
    with open('./data.json', 'r') as json_file:
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
    with open('./data.json', 'w') as json_file:
        json.dump(data, json_file, indent = 4)
    return data

def exit_text(stdscr: curses.window, height: int, width: int) -> None:
    """
    Prompts an exit text for the user
    """
    pass
    #stdscr.addstr(height - 1, 0, ' ' * width)
    #stdscr.refresh()
    #stdscr.addstr(height - 1, 2, "Drücke \"Esc\" zum beenden", curses.color_pair(2))
    #stdscr.refresh()


def is_mail_correct(mail: str) -> bool:
    """
    Validates if the provided email address matches a standard email pattern.
    
    Returns True if the email is valid, False otherwise.
    """
    pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    return bool(pattern.match(mail))

def input_function(stdscr: curses.window, input_y: int, input_x: int, is_password: bool) -> str:
    """
    Captures user input at a specific terminal position. 
    Supports normal and password (masked) input. 
    Handles navigation, backspace, and exit confirmation.
    
    Returns the entered input as a string.
    """
    beginx = input_x
    user_input = ""
    go = True
    while go:
        inp = stdscr.getch()
        if inp in [10, 13]:
            go = False
        elif inp == curses.KEY_BACKSPACE:
            if input_x > beginx:
                stdscr.addch(input_y, input_x - 1, ' ')
                stdscr.move(input_y, input_x - 1)
                stdscr.refresh()
                user_input = user_input[:-1]
                input_x -= 1
        elif inp == curses.KEY_RIGHT:
            if input_x < beginx + len(user_input):
                input_x += 1
                stdscr.move(input_y, input_x)
                stdscr.refresh()
        elif inp == curses.KEY_LEFT:
            if input_x > beginx:
                input_x -= 1
                stdscr.move(input_y, input_x)
                stdscr.refresh()
        elif inp == curses.KEY_UP or inp == curses.KEY_DOWN:
            pass
        elif inp == 27:
            is_sure_to_exit_program(stdscr)
        else:
            if not is_password:
                stdscr.addch(input_y, input_x, chr(inp))
                stdscr.refresh()
                user_input += chr(inp)
                input_x += 1
            elif is_password:
                stdscr.addch(input_y, input_x, '*')
                stdscr.refresh()
                user_input += chr(inp)
                input_x += 1
    return user_input

def is_sure_to_exit_program(stdscr: curses.window) -> None:
    """
    Displays an exit confirmation prompt to the user.
    Exits the program if 'Enter' is pressed, or cancels if 'Esc' is pressed.
    """
    height, width = stdscr.getmaxyx()
    text = "Sicher, dass Sie das Programm beenden wollen? \"Enter\":beenden | \"Esc\":abbrechen"
    stdscr.addstr(height - 1, 2, ' ' * len("Drücke \"Esc\" zum beenden"))
    stdscr.refresh()
    stdscr.addstr(height - 1, (width - len(text)) // 2, text, curses.color_pair(2))
    stdscr.refresh()
    exit_input = stdscr.getch()
    if exit_input == [10, 13]:
        sys.exit(0)
    elif exit_input == 27:
        exit_text(stdscr, width, height)

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
        with open('./data.json', 'w') as file:
            json.dump(data, file, ensure_ascii = False, indent = 4)

def main(stdscr: curses.window) -> None:
    """
    Main function in which screen options are declared, ...
    """
    #curses.resize_term(30, 50)
    self_grey = 1
    curses.start_color()
    curses.init_color(self_grey, 400, 400, 400)
    curses.init_pair(1, curses.COLOR_GREEN, self_grey) #Schriftfarbe: Grün, Hintergrundfarbe: Hellgrau
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK) #Schriftfarbe: Grün, Hintergrundfarbe: Schwarz
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK) #Schriftfarbe: Rot, Hintergrundfarbe: Schwarz
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
    height, width = stdscr.getmaxyx()
    create_accounts_file()
    mail = start_screen(stdscr, height, width)
    password_manager(stdscr, height, width, mail)

if __name__ == "__main__":
    curses.wrapper(main)
    
"""
This module is main.py
"""

import curses
from source.data import read_data_json, create_accounts_file
from source.password_manager_framework import choice_function, input_function, start_screen
from source.password import show_password, add_new_password

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
    
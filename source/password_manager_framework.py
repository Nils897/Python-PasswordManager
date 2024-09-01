"""
This module provides the interface for the start screen and user authentication processes in a terminal-based application. 
It includes functions to display the start screen, navigate the menu, handle user input for signing in, registering new accounts.

Functions:

- start_screen: Displays the initial start screen with options to sign in, register, or exit the application.
- choice_function: Handles user navigation through menu options and selection based on keypresses.
- register: Facilitates user registration by collecting and validating email and password inputs, and saving the new account to a JSON file.
- signIn: Manages the sign-in process by verifying the provided email and master password against stored data.

This module leverages the curses library for terminal screen management and user input handling.
"""
import curses
import sys

from source.validation import is_password_correct, is_mail_correct
from source.password import hash_password

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

def exit_text(stdscr: curses.window, height: int, width: int) -> None:
    """
    Prompts an exit text for the user
    """
    pass
    #stdscr.addstr(height - 1, 0, ' ' * width)
    #stdscr.refresh()
    #stdscr.addstr(height - 1, 2, "Drücke \"Esc\" zum beenden", curses.color_pair(2))
    #stdscr.refresh()

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

def register(stdscr: curses.window, height: int, width: int) -> str:
    from source.data import safe_register_data, read_data_json
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

def signIn(stdscr: curses.window, height: int, width: int) -> str:
    from source.data import safe_register_data, read_data_json
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

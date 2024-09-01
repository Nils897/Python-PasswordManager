"""
This module is main.py
"""
import curses
from source.password_manager import password_manager, create_accounts_file, start_screen

def main(stdscr: curses.window) -> None:
    """
    Main function in which screen options are declared and the passwort manager function gets executed
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
    
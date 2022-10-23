from src.interactive_cli.prints import print_introduction, print_menu


def init_interactive_cli(stdscr):
    current_row_idx = 0
    menu_navigator(stdscr, current_row_idx)


def menu_navigator(stdscr, current_row_idx):
    print_menu(stdscr, current_row_idx)
    navigate_menu(stdscr, current_row_idx)


def navigate_menu(stdscr, current_row_idx):
    pass

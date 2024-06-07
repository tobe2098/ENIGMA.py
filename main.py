# main.py
import argparse

from utils.utils import my_quit_fn
from utils.utils_cli import printOutput

is_cli_mode = False
is_gui_mode = False


def get_is_cli_mode():
    return is_cli_mode


def get_is_gui_mode():
    return is_gui_mode


def main():
    parser = argparse.ArgumentParser(
        description="Emulates the ENIGMA machine with some modifications"
    )
    parser.add_argument("--gui", action="store_true", help="Run in GUI mode")
    args = parser.parse_args()

    is_gui_mode = args.gui
    if is_gui_mode:
        print(printOutput("I am very sorry, but for now there is no GUI"))
        my_quit_fn()
    else:
        is_cli_mode = True
        print(printOutput("Running in CLI mode"))

    # ... Use other functions from utils.py
    # (e.g., cli_mode = utils.get_cli_mode())  # Can use get_cli_mode now


if __name__ == "__main__":
    main()
    # ... Use other functions from utils.py
    # (e.g., cli_mode = utils.get_cli_mode())  # Can use get_cli_mode now

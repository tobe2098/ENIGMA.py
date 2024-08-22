import json

from utils.utils import Constants, get_charlist_dict
from ...utils.utils_cli import (
    get_a_charlist_and_name_from_user,
    printError,
    printListOfOptions,
)


def load_a_machine():
    pass


def create_a_new_machine_from_scratch():
    pass


def create_a_new_random_machine():
    pass


def edit_an_existing_rotor():
    pass


def edit_an_existing_reflector():
    pass


def edit_an_existing_plugboard():
    pass


###


def _print_charlist_collection(dictionary=None):
    if not dictionary:
        dictionary = get_charlist_dict()
    name_list = list(dictionary.keys())
    printListOfOptions(name_list)


def _store_and_return_a_new_charlist():
    charlist, name = get_a_charlist_and_name_from_user()
    dictionary = get_charlist_dict()
    dictionary[name] = charlist
    with open(Constants.CHARLISTS_FILE_PATH) as file:
        json.dump(dictionary, file, indent=2)
    return charlist  # Only to be used if called with that intention


def _delete_a_charlist():
    # Make sure the default ones are not deleted or are added every time you ask for a charlist
    pass


def _retrieve_a_charlist():
    pass


def _get_a_charlist_from_storage():
    dictionary = get_charlist_dict()
    if not dictionary:
        printError("There are no stored charlists, json file was removed ")
    _print_charlist_collection(dictionary=dictionary)

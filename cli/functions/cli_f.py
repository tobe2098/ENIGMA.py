import json

from cli.functions.machines_f import _load_machine
from utils.utils import Constants, get_charlist_dict, save_charlist_dict
from ...utils.utils_cli import (
    askingInput,
    checkInputValidity,
    get_a_charlist_and_name_from_user,
    printListOfOptions,
    printOutput,
    printWarning,
    returningToMenu,
    runNodeMenu,
)


def load_a_machine():
    machine_ref = _load_machine()
    runNodeMenu(machine_ref, machine_menu)


def create_a_new_machine_from_scratch():
    pass


def create_a_new_random_machine():
    pass


def edit_an_existing_rotor():
    pass


def edit_an_existing_reflector():
    pass


###


def _print_charlist_collection(dictionary=None):
    if not dictionary:
        dictionary = get_charlist_dict()
    name_list = list(dictionary.keys())
    printListOfOptions(name_list)
    return name_list


def _store_and_return_a_new_charlist():
    charlist, name = get_a_charlist_and_name_from_user()
    dictionary = get_charlist_dict()
    dictionary[name] = charlist
    with open(Constants.CHARLISTS_FILE_PATH) as file:
        json.dump(dictionary, file, indent=2)
    return charlist  # Only to be used if called with that intention


def _delete_a_charlist():
    dictionary = get_charlist_dict()
    name_list = _print_charlist_collection(dictionary=dictionary)
    printWarning("Default character lists cannot be deleted")
    name_index = askingInput("Input the index of the character list to be deleted")
    if not name_index:
        returningToMenu()
    name_list = checkInputValidity(name_index, int, (0, len(name_list)))
    while not name_list:
        name_index = askingInput("Input a valid index")
        if not name_index:
            returningToMenu()
        name_list = checkInputValidity(name_index, int, (0, len(name_list)))
    dictionary.pop(name_list[name_index])
    save_charlist_dict(dictionary=dictionary)
    returningToMenu("Character list was deleted")


def _print_a_particular_character_list():
    printOutput(_get_a_charlist_from_storage())


def _get_a_charlist_from_storage():
    dictionary = get_charlist_dict()
    name_list = _print_charlist_collection(dictionary=dictionary)
    name_index = askingInput("Input the index of the desired character list")
    if not name_index:
        returningToMenu()
    name_list = checkInputValidity(name_index, int, (0, len(name_list)))
    while not name_list:
        name_index = askingInput("Input a valid index")
        if not name_index:
            returningToMenu()
        name_list = checkInputValidity(name_index, int, (0, len(name_list)))
    return dictionary[name_list[name_index]]

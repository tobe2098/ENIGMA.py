from utils.utils_cli import exitMenu
from ..functions.cli_f import (
    _delete_a_charlist,
    _print_a_particular_character_list,
    _store_and_return_a_new_charlist,
    _print_charlist_collection,
    edit_an_existing_plugboard,
    edit_an_existing_reflector,
    edit_an_existing_rotor,
    load_a_machine,
    create_a_new_machine_from_scratch,
    create_a_new_random_machine,
)


_charlist_dict_menu = {
    "1": (
        "Print the names of currently saved character lists",
        _print_charlist_collection,
    ),
    "2": ("Print out a particular character list", _print_a_particular_character_list),
    "3": ("Delete a character list", _delete_a_charlist),
    "4": (
        "Store a custom character list",
        _store_and_return_a_new_charlist,
    ),
    "0": ("Exit menu", exitMenu),
}

_outer_cli_menu = {
    "1": (
        "Access character list menu",
        _print_charlist_collection,
    ),
    "2": ("Print out a particular character list", _print_a_particular_character_list),
    "3": ("Delete a character list", _delete_a_charlist),
    "4": (
        "Store a custom character list",
        _store_and_return_a_new_charlist,
    ),
    "0": ("Exit menu", exitMenu),
}

from utils.utils_cli import exitMenu, exitProgram
from ..menus.rotors_m import _load_saved_rotor_for_editing
from ..menus.reflectors_m import _load_saved_reflector_for_editing
from ..functions.cli_f import (
    _delete_a_charlist,
    _print_a_particular_character_list,
    _store_and_return_a_new_charlist,
    _print_charlist_collection,
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
_menu_cli_options = {}

_outer_cli_menu = {  # Here we have to be able to delete saved machines
    "1": (
        "Access character list menu",
        _charlist_dict_menu,
    ),
    "2": ("Load an existing machine", load_a_machine),
    "3": ("Create a new machine from scratch", create_a_new_machine_from_scratch),
    "4": ("Create a new random machine", create_a_new_random_machine),
    "5": ("Load a saved rotor for editing", _load_saved_rotor_for_editing),
    "6": ("Load a saved reflector for editing", _load_saved_reflector_for_editing),
    "7": ("Configuration menu", _menu_cli_options),
    "0": ("Exit", exitProgram),
}

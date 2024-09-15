from utils.utils_cli import exitMenu
from ..menus.rotors_m import _load_saved_rotor_for_editing
from ..menus.reflectors_m import _load_saved_reflector_for_editing
from ..functions.cli_f import (
    _delete_a_charlist,
    _print_a_particular_character_list,
    _store_and_return_a_new_charlist,
    _print_charlist_collection,
    load_a_machine,
    create_a_new_machine_from_scratch_and_use,
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
_denigma_menu = {
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
_menu_cli_misc = {
    # Unset and set machine
    "0": ("Exit menu", exitMenu),
}

_outer_cli_menu = {  # Here we have to be able to delete saved machines
    "1": (
        "Access character list menu",
        _charlist_dict_menu,
    ),
    "2": ("Edit an existing reflector", _print_a_particular_character_list),
    "2": ("Edit an existing rotor", _print_a_particular_character_list),
    "2": ("Edit an existing", _print_a_particular_character_list),
    "3": ("Delete a character list", _delete_a_charlist),
    "4": (
        "Store a custom character list",
        _store_and_return_a_new_charlist,
    ),
    "0": ("Exit menu", exitMenu),
}

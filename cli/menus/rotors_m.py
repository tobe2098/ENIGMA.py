import os

from utils.exceptions import FileIOErrorException
from ...core import rotors
from ...utils import utils_cli
from ...utils import utils
from ..functions.rotors_f import (
    _change_rotor_name_rt,
    _change_position_rt,
    _change_notches_rt,
    _choose_connection_to_delete_rt,
    _create_a_connection_single_choice_rt,
    _randomize_name_rt,
    _randomize_notches_rt,
    _randomize_position_rt,
    _reset_and_randomize_connections_rt,
    _reset_and_streamline_connections_by_pairs_rt,
    _exitMenu_rt,
    _form_all_connections_rt,
    _load_saved_rotor,
    _save_rotor_in_its_folder,
    _show_config_rt,
    _swap_connections_rt,
)


_menu_rotor_name_options = {
    "1": ("Change name", _change_rotor_name_rt),
    "2": ("Randomize name", _randomize_name_rt),
    "0": ("Exit menu", utils_cli.exitMenu),
}

_menu_rotor_position_and_notches_options = {
    "1": ("Change character position", _change_position_rt),
    "2": ("Randomize character position", _randomize_position_rt),
    "3": ("Change notches", _change_notches_rt),
    "4": ("Randomize notches", _randomize_notches_rt),
    "0": ("Exit menu", utils_cli.exitMenu),
}

_menu_rotor_connections_options = {
    "1": ("Delete a single connection", _choose_connection_to_delete_rt),
    "2": ("Create a single connection", _create_a_connection_single_choice_rt),
    "3": ("Form all connections left", _form_all_connections_rt),
    "4": ("Swap two connections", _swap_connections_rt),
    "5": (
        "Reset and form max. connections",
        _reset_and_streamline_connections_by_pairs_rt,
    ),
    "6": ("Reset and randomize connections", _reset_and_randomize_connections_rt),
    "0": ("Exit menu", utils_cli.exitMenu),
}


def _load_saved_rotor_for_editing():
    rotor = _load_saved_rotor()
    utils_cli.runNodeMenu(rotor, _menu_rotor)
    while True:
        try:
            _save_rotor_in_its_folder(rotor)
            # utils_cli.returningToMenu() #Previous line has the exception inside
        except FileIOErrorException as e:
            utils_cli.printOutput(e)
            flag = ""
            while flag != "n" and flag != "y":
                flag = utils_cli.askingInput(
                    "Do you want to discard the rotor and exit?[y/n]"
                ).lower()
            if flag == "y":
                utils_cli.returningToMenu(f"Rotor {rotor.get_name()} was discarded")


_menu_rotor = {
    "1": ("Show current rotor setup", _show_config_rt),
    "2": ("Save rotor", _save_rotor_in_its_folder),
    "3": ("Naming menu", _menu_rotor_name_options),
    "4": ("Connections options menu", _menu_rotor_connections_options),
    "5": (
        "Notches and position options menu",
        _menu_rotor_position_and_notches_options,
    ),
    # "6": ("Edit a previously saved rotor", _load_saved_rotor_for_editing) This somewhere else,
    "0": ("Exit menu", _exitMenu_rt),
}

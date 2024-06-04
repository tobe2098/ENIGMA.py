import os
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
    _save_in_current_directory_rt,
    _show_config_rt,
    _swap_connections_rt,
)


_menu_rotor_name_options = {
    "1": ("Change name", _change_rotor_name_rt),
    "2": ("Randomize name", _randomize_name_rt),
    "0": ("Exit menu", utils_cli.exitMenu),
}

_menu_rotor_position_and_notches_options = {
    "1": ("Change position", _change_position_rt),
    "2": ("Randomize position", _randomize_position_rt),
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


def _load_saved_rotor_for_editing(rotor: rotors.Rotor = None, recursive: bool = False):
    if not recursive:
        rotor = _load_saved_rotor()
    utils_cli.runNodeMenu(rotor, _menu_rotor)
    try:
        _save_in_current_directory_rt(rotor)
        utils_cli.returningToMenu()
    except utils_cli.MenuExitException:
        current_path = os.getcwd()
        new_folder = utils.ROTORS_FILE_HANDLE
        path = os.path.join(current_path, new_folder)
        if not utils_cli.checkIfFileExists(path, rotor._name, "rotor"):
            utils_cli.printOutput("A file with the rotor's name was not detected")
            accbool = ""
            while not accbool == "n" or not accbool == "y":
                accbool = input(
                    utils_cli.askingInput("Do you want to exit anyway?[y/n]")
                ).lower()
            if accbool == "n":
                _load_saved_rotor_for_editing(rotor, True)
            utils_cli.returningToMenu(
                utils_cli.formatAsWarning((f"rotor {rotor.name} was discarded"))
            )
    # Conda activation: conda info --envs, conda activate {}


_menu_rotor = {
    "1": ("Show current rotor setup", _show_config_rt),
    "2": ("Save rotor", _save_in_current_directory_rt),
    "3": ("Naming menu", _menu_rotor_name_options),
    "4": ("Connections options menu", _menu_rotor_connections_options),
    "5": (
        "Notches and position options menu",
        _menu_rotor_position_and_notches_options,
    ),
    # "6": ("Edit a previously saved rotor", _load_saved_rotor_for_editing) This somewhere else,
    "0": ("Exit menu", _exitMenu_rt),
}

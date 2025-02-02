# from tkinter import Menubutton
from denigma.utils import utils_cli
from denigma.utils.utils import Constants
from denigma.cli.functions.plugboards_f import (
    _show_config_pb,
    _choose_connection_to_delete_pb,
    _create_a_single_connection_pb,
    _reset_and_form_n_connections_pb,
    _reset_and_randomize_connections_pb,
    _reset_connections_pb,
)


_menu_plugboard = {
    Constants.menu_id_string: "Plugboard",
    "1": ("Show current plugboard setup", _show_config_pb),
    "2": ("Delete a single connection", _choose_connection_to_delete_pb),
    "3": ("Create a single connection", _create_a_single_connection_pb),
    "4": (
        "Reset current connections and form n connections",
        _reset_and_form_n_connections_pb,
    ),
    "5": ("Reset and randomize connections", _reset_and_randomize_connections_pb),
    "6": ("Reset connections", _reset_connections_pb),
    "0": ("Exit menu", utils_cli.exitMenu),
}

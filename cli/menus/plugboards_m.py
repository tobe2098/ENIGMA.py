# from tkinter import Menubutton
from ...core import machines
from ...utils.utils_cli import *
from ..functions.plugboards_f import (
    _show_config_pb,
    _choose_connection_to_delete_pb,
    _create_a_connection_single_choice_pb,
    _form_numbered_connections_pb,
    _reset_and_form_n_connections_pb,
    _reset_and_form_all_connections_by_pairs_pb,
    _reset_and_randomize_connections_pb,
    _reset_connections_pb,
)


_menu_plugboard = {
    "1": ("Show current plugboard setup", _show_config_pb),
    "2": ("Delete a single connection", _choose_connection_to_delete_pb),
    "3": ("Create a single connection", _create_a_connection_single_choice_pb),
    "4": ("Form n connections", _form_numbered_connections_pb),
    "5": (
        "Reset current connections and form n connections",
        _reset_and_form_n_connections_pb,
    ),
    "6": (
        "Reset and form max. connections",
        _reset_and_form_all_connections_by_pairs_pb,
    ),
    "7": ("Reset and randomize connections", _reset_and_randomize_connections_pb),
    "8": ("Reset connections", _reset_connections_pb),
    "0": ("Exit menu", exitMenu),
}


def main_plugboard_menu(machine_ref: machines.Machine):
    while True:
        regular_menu_call(machine_ref._plugboard, _menu_plugboard)

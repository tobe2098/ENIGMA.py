# from tkinter import Menubutton
from numpy import isin
from ...core import machines
from ...core import plugboards
from ...core import utils
from .utils_m import *


def _show_config_pb(plugboard_ref: plugboards.PlugBoard):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
    """

    plugboard_ref._show_config()
    returningToMenuNoMessage()


def _choose_connection_to_delete_pb(plugboard_ref: plugboards.PlugBoard):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
    """
    paired_df, _ = utils.simplify_dictionary_paired_unpaired(plugboard_ref._board_dict)

    if paired_df.shape[0] == 0:
        returningToMenuMessage("There are no available connections.")

    print(stringOutput("Current connections are:"), paired_df)
    row = input(askingInput("Choose a connection to delete (by index): "))

    if isinstance(row, int) and row > 0 and row < paired_df.shape[0]:
        _delete_a_connection_pb(plugboard_ref=plugboard_ref, connIndex=row)
        returningToMenuMessage("Connection was deleted.")
    else:
        returningToMenuMessage("Index invalid.")


def _delete_a_connection_pb(plugboard_ref: plugboards.PlugBoard, connIndex):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
        connIndex (_type_): _description_
    """
    paired_df, _ = utils.simplify_dictionary_paired_unpaired(plugboard_ref._board_dict)
    for entry in paired_df.iloc[connIndex]:
        # del plugboard_ref._board_dict[entry] #Requires testing
        plugboard_ref[entry] = entry

    plugboard_ref._update_dicts()
    # del d['k2']


def _create_a_connection_single_choice_pb(plugboard_ref: plugboards.PlugBoard):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
    """
    _, unpaired_list = utils.simplify_dictionary_paired_unpaired(
        plugboard_ref._board_dict
    )
    if len(unpaired_list) < 2:
        returningToMenuMessage(
            "There are no letters left to pair (one or fewer left unconnected)."
        )
    print(">Unpaired letters:", unpaired_list)
    letter1 = input(askingInput("Choose a letter to pair:")).upper()
    if letter1 not in unpaired_list:
        returningToMenuMessage("Invalid input.")
    print(stringOutput("Remaining letters:"), list(set(unpaired_list) - set(letter1)))
    letter2 = input(askingInput("Choose the second letter:")).upper()
    if letter2 not in list(set(unpaired_list) - set(letter1)):
        returningToMenuMessage("Invalid input.")
    plugboard_ref._board_dict[letter1] = letter2
    plugboard_ref._board_dict[letter2] = letter1
    plugboard_ref._update_dicts()
    returningToMenuMessage("The connection was formed.")


# First get a letter, show unconnected again, then choose to connect. If wrong choice, go back to start


def _connect_two_letters_pb(plugboard_ref: plugboards.PlugBoard):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
    """
    _, unpaired_list = utils.simplify_dictionary_paired_unpaired(
        plugboard_ref._board_dict
    )
    if len(unpaired_list) < 2:
        returningToMenuMessage(
            "There are no letters left to pair (one or fewer left unconnected)."
        )
    while True:
        print(stringOutput("Unpaired letters:"), unpaired_list)
        print(stringOutput("If you want to stop configurating the board, press Enter."))
        letters = input(askingInput("Input two letters to pair:")).strip().upper()
        if letters.isalpha() and len(letters) == 2:
            pass
        elif not letters:
            returningToMenuNoMessage("No input.")
        else:
            print("Error: Input 2 letters please")
            continue
        letters = list(letters)
        if not all(map(lambda v: v in letters, unpaired_list)):
            print(stringOutput("One of the letters is already connected."))
            continue
        break
    plugboard_ref._board_dict[letters[0]] = letters[1]
    plugboard_ref._board_dict[letters[1]] = letters[0]
    print(stringOutput("Connection formed."))


def _form_numbered_connections_pb(plugboard_ref: plugboards.PlugBoard):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
    """
    _show_config_pb(plugboard_ref)
    _, unpaired_list = utils.simplify_dictionary_paired_unpaired(
        plugboard_ref._board_dict
    )
    connections = input(
        askingInput(
            f"How many connections do you want to create (Max. {len(unpaired_list)})? "
        )
    )
    if connections > len(unpaired_list):
        returningToMenuMessage("Number exceeds the maximum.")
    _form_n_extra_connections_pb(plugboard_ref, connections)


def _reset_and_form_n_connections_pb(plugboard_ref: plugboards.PlugBoard):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
    """
    _reset_connections_pb(plugboard_ref)
    _form_numbered_connections_pb(plugboard_ref)


def _form_n_extra_connections_pb(plugboard_ref: plugboards.PlugBoard, connections: int):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
        connections (int): _description_
    """
    for i in range(connections):
        clearScreenConvenience()
        print(stringOutput(f"Creating connection {i+1} of {connections}"))
        _connect_two_letters_pb(plugboard_ref)


def _reset_and_streamline_connections_by_pairs_pb(plugboard_ref: plugboards.PlugBoard):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
    """
    _reset_connections_pb(plugboard_ref)
    while True:
        accbool = input(askingInput("Do you still want to make changes?[y/n]")).lower()
        if accbool == "n":
            returningToMenuNoMessage()
        elif accbool == "y":
            break
    while True:
        _connect_two_letters_pb(plugboard_ref)


## The board is fully connected (one or fewer letters left unconnected). If wrong choice, go back to start


def _reset_and_randomize_connections_pb(plugboard_ref: plugboards.PlugBoard):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
    """
    seed = input(
        askingInput(
            "Introduce a positive integer as a seed to randomize the plugboard connections: "
        )
    )
    if not isinstance(seed, int) and seed > 0:
        returningToMenuMessage("Number is not a positive integer.")
    plugboard_ref._reset_dictionaries()
    plugboard_ref.random_setup(seed)


def _reset_connections_pb(plugboard_ref: plugboards.PlugBoard):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
    """
    plugboard_ref._reset_dictionaries()


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
        _reset_and_streamline_connections_by_pairs_pb,
    ),
    "7": ("Reset and randomize connections", _reset_and_randomize_connections_pb),
    "8": ("Reset connections", _reset_connections_pb),
    "0": ("Exit menu", exitMenu),
}


def main_plugboard_menu(machine_ref: machines.Machine):
    while True:
        clearScreenSafety()
        try:
            for key in sorted(_menu_plugboard.keys()):
                print(menuOption(key + ":" + _menu_plugboard[key][0]))

            answer = str(input(askForMenuOption()))
            _menu_plugboard.get(answer, [None, invalidChoice])[1](
                machine_ref._plugboard
            )
        except ReturnToMenuException:
            print(ReturnToMenuException.message)
        except MenuExitException:
            raise MenuExitException()

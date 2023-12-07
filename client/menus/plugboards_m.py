# from tkinter import Menubutton
from click import clear
from ...core import plugboards
from ...core import utils
from .utils_m import *


def show_board_config(plugboard_ref: plugboards.PlugBoard):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
    """

    plugboard_ref.show_config()
    returningToMenuNoMessage()


def choose_connection_to_delete(plugboard_ref: plugboards.PlugBoard):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
    """
    paired_df, _ = utils.simplify_board_dict(plugboard_ref._board_dict)

    if paired_df.shape[0] == 0:
        returningToMenuMessage("There are no available connections.")

    print(stringOutput("Current connections are:"), paired_df)
    row = input(askingInput("Choose a connection to delete (by index): "))

    if isinstance(row, int) and row > 0 and row < paired_df.shape[0]:
        delete_a_connection(plugboard_ref=plugboard_ref, connIndex=row)
        returningToMenuMessage("Connection was deleted.")
    else:
        returningToMenuMessage("Index invalid.")


def delete_a_connection(plugboard_ref: plugboards.PlugBoard, connIndex):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
        connIndex (_type_): _description_
    """
    paired_df, _ = utils.simplify_board_dict(plugboard_ref._board_dict)
    for entry in paired_df.iloc[connIndex]:
        # del plugboard_ref._board_dict[entry] #Requires testing
        plugboard_ref[entry] = entry

    plugboard_ref._update_dicts()
    # del d['k2']


def create_a_connection_single_choice(plugboard_ref: plugboards.PlugBoard):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
    """
    _, unpaired_list = utils.simplify_board_dict(plugboard_ref._board_dict)
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


def connect_two_letters(plugboard_ref: plugboards.PlugBoard):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
    """
    _, unpaired_list = utils.simplify_board_dict(plugboard_ref._board_dict)
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


def form_numbered_connections(plugboard_ref: plugboards.PlugBoard):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
    """
    show_board_config(plugboard_ref)
    _, unpaired_list = utils.simplify_board_dict(plugboard_ref._board_dict)
    connections = input(
        askingInput(
            f"How many connections do you want to create (Max. {len(unpaired_list)})? "
        )
    )
    if connections > len(unpaired_list):
        returningToMenuMessage("Number exceeds the maximum.")
    form_n_extra_connections(plugboard_ref, connections)


def reset_and_form_n_connections(plugboard_ref: plugboards.PlugBoard):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
    """
    reset_connections(plugboard_ref)
    form_numbered_connections(plugboard_ref)


def form_n_extra_connections(plugboard_ref: plugboards.PlugBoard, connections: int):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
        connections (int): _description_
    """
    for i in range(connections):
        clearScreenConvenience()
        print(stringOutput(f"Creating connection {i+1} of {connections}"))
        connect_two_letters(plugboard_ref)


def reset_and_streamline_connections_by_pairs(plugboard_ref: plugboards.PlugBoard):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
    """
    reset_connections(plugboard_ref)
    while True:
        accbool = input(askingInput("Do you still want to make changes?[y/n]")).lower()
        if accbool == "n":
            returningToMenuNoMessage()
        elif accbool == "y":
            break
    while True:
        connect_two_letters(plugboard_ref)


## The board is fully connected (one or fewer letters left unconnected). If wrong choice, go back to start


def reset_connections(plugboard_ref: plugboards.PlugBoard):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
    """
    plugboard_ref._reset_dictionaries()


_menu_plugboard = {
    "1": ("Show current plugboard setup", show_board_config),
    "2": ("Delete a single connection", choose_connection_to_delete),
    "3": ("Create a single connection", create_a_connection_single_choice),
    "4": ("Form n connections", form_numbered_connections),
    "5": (
        "Reset current connections and form n connections",
        reset_and_form_n_connections,
    ),
    "6": ("Reset and form max. connections", reset_and_streamline_connections_by_pairs),
    "7": ("Reset connections", reset_connections),
    "0": ("Exit menu", exitMenu),
}


def main_plugboard_menu(plugboard_ref: plugboards.PlugBoard):
    while True:
        clearScreenSafety()
        try:
            for key in sorted(_menu_plugboard.keys()):
                print(menuOption(key + ":" + _menu_plugboard[key][0]))

            answer = str(input(askingInput("Make A Choice:")))
            _menu_plugboard.get(answer, [None, invalidChoice])[1](plugboard_ref)
        except ReturnToMenuException:
            print(ReturnToMenuException.message)
        except MenuExitException:
            raise MenuExitException()

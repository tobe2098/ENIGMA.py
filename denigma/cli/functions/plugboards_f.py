# from tkinter import Menubutton
# from ast import unparse
from denigma.core import plugboards
from denigma.utils.utils_cli import returningToMenu,askingInput,checkInputValidity,clearScreenConvenienceCli,getSeedFromUser
from denigma.utils.utils import (
    simplify_simple_dictionary_paired_unpaired,
)
from denigma.utils.formatting import printOutput,printError


def _show_config_pb(plugboard_ref: plugboards.PlugBoard):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
    """

    paired_df, unpaired_list = simplify_simple_dictionary_paired_unpaired(
        plugboard_ref._board_dict
    )
    printOutput("Paired characters:\n", paired_df)
    printOutput("Unpaired characters: ", unpaired_list)
    printOutput(
        "Number of connections: ",
        int((len(plugboard_ref.get_charlist()) - len(unpaired_list)) / 2),
    )
    returningToMenu()


def _choose_connection_to_delete_pb(plugboard_ref: plugboards.PlugBoard):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
    """
    paired_df, _ = simplify_simple_dictionary_paired_unpaired(
        plugboard_ref._board_dict
    )

    if paired_df.shape[0] == 0:
        returningToMenu("There are no available connections")

    printOutput("Current connections are:\n", paired_df)
    row = askingInput("Choose a connection to delete (by index)")
    row = checkInputValidity(row, int, rangein=(0, paired_df.shape[0]))

    if row!=None:
        _delete_a_connection_pb(
            plugboard_ref=plugboard_ref,
            character1=paired_df.iloc[row].iloc[0],
        )
        returningToMenu("Connection was deleted")
    else:
        returningToMenu("Index invalid", output_type="e")


def _delete_a_connection_pb(plugboard_ref: plugboards.PlugBoard, character1: str):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
        connIndex (_type_): _description_
    """
    plugboard_ref._board_dict[plugboard_ref._board_dict[character1]]=plugboard_ref._board_dict[character1]
    plugboard_ref._board_dict[character1]=character1

    plugboard_ref._update_dicts()
    # del d['k2']


def _create_a_single_connection_pb(plugboard_ref: plugboards.PlugBoard):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
    """
    _, unpaired_list = simplify_simple_dictionary_paired_unpaired(
        plugboard_ref._board_dict
    )
    if len(unpaired_list) < 2:
        returningToMenu(
            "There are no characters left to pair (one or fewer left unconnected)"
        )
    printOutput("Unpaired characters:", unpaired_list)
    character1 = askingInput("Choose a character to pair")
    character1 = checkInputValidity(character1, rangein=unpaired_list)
    if character1==None:
        printError("Invalid input")
        return False
    remaining_characters = list(set(unpaired_list) - set(character1))
    printOutput("Remaining characters:", remaining_characters)
    character2 = askingInput("Choose the second character")
    character2 = checkInputValidity(character2, rangein=remaining_characters)
    if character2==None:
        printError("Invalid input")
        return False
    plugboard_ref._board_dict[character1] = character2
    plugboard_ref._board_dict[character2] = character1
    plugboard_ref._update_dicts()
    printOutput("The connection was formed")
    return True


# First get a character, show unconnected again, then choose to connect. If wrong choice, go back to start


# def _connect_two_characters_pb(plugboard_ref: plugboards.PlugBoard):
#     """_summary_

#     Args:
#         plugboard_ref (plugboards.PlugBoard): _description_
#     """
#     _, unpaired_list = simplify_simple_dictionary_paired_unpaired(
#         plugboard_ref._board_dict
#     )
#     if len(unpaired_list) < 2:
#         returningToMenu(
#             "There are no characters left to pair (one or fewer left unconnected)"
#         )
#     while True:
#         printOutput("Unpaired characters:", (unpaired_list))
#         printOutput(
#             "If you want to stop configurating the board, press Enter"
#         )
#         characters = askingInput("Input two characters to pair:").strip().upper()
#         if characters.isalpha() and len(characters) == 2:
#             pass
#         elif not characters:
#             # returningToMenu("No input")
#             return
#         else:
#             print("Error: Input 2 characters please")
#             continue
#         characters = list(characters)
#         for i in range(2):
#             characters[i] = checkInputValidity(characters[i], _range=unpaired_list)
#         if not all(characters):
#             # if not all(map(lambda v: v in characters, unpaired_list)):
#             printOutput("One of the characters is already connected")
#             continue
#         break
#     plugboard_ref._board_dict[characters[0]] = characters[1]
#     plugboard_ref._board_dict[characters[1]] = characters[0]
#     printOutput("Connection formed")


def _form_numbered_connections_pb(plugboard_ref: plugboards.PlugBoard):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
    """
    _show_config_pb(plugboard_ref)
    _, unpaired_list = simplify_simple_dictionary_paired_unpaired(
        plugboard_ref._board_dict
    )
    connections = input(
        askingInput(
            f"How many connections do you want to create (Max. {len(unpaired_list)/2})?"
        )
    )
    if connections > len(unpaired_list) / 2:
        returningToMenu("Number exceeds the maximum", "e")
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
    c = 0
    while connections - c:
        clearScreenConvenienceCli()
        printOutput(f"Creating connection {c+1} of {connections}")
        if _create_a_single_connection_pb(plugboard_ref):
            c += 1


# def _reset_and_form_all_connections_by_pairs_pb(plugboard_ref: plugboards.PlugBoard):
#     """_summary_

#     Args:
#         plugboard_ref (plugboards.PlugBoard): _description_
#     """
#     _reset_connections_pb(plugboard_ref)
#     while True:
#         accbool = askingInput(
#             "Do you want to keep making changes?[y/n]"
#         ).lower()
#         if accbool == "n":
#             returningToMenu()
#         elif accbool == "y":
#             _create_a_single_connection_pb(plugboard_ref)


## The board is fully connected (one or fewer characters left unconnected). If wrong choice, go back to start


def _reset_and_randomize_connections_pb(plugboard_ref: plugboards.PlugBoard):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
    """
    seed = getSeedFromUser()
    plugboard_ref._reset_dictionaries()
    plugboard_ref.random_setup(seed)
    printOutput("Board random setup is done")


def _reset_connections_pb(plugboard_ref: plugboards.PlugBoard):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
    """
    plugboard_ref._reset_dictionaries()

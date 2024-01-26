# from tkinter import Menubutton
# from ast import unparse
from ...core import plugboards
from ...utils import utils
from ...utils import utils_cli
from ...utils.utils import simplify_simple_dictionary_paired_unpaired


def _show_config_pb(plugboard_ref: plugboards.PlugBoard):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
    """

    paired_df, unpaired_list = simplify_simple_dictionary_paired_unpaired(
        plugboard_ref._board_dict
    )
    utils_cli.printOutput("Paired letters: ")
    print(paired_df)
    utils_cli.printOutput("Unpaired letters: ")
    print(unpaired_list)
    utils_cli.returningToMenuNoMessage()


def _choose_connection_to_delete_pb(plugboard_ref: plugboards.PlugBoard):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
    """
    paired_df, _ = utils.simplify_simple_dictionary_paired_unpaired(
        plugboard_ref._board_dict
    )

    if paired_df.shape[0] == 0:
        utils_cli.returningToMenuMessage("There are no available connections.")

    utils_cli.printOutput("Current connections are:")
    print(paired_df)
    row = utils_cli.askingInput("Choose a connection to delete (by index): ")

    if isinstance(row, int) and row > 0 and row < paired_df.shape[0]:
        _delete_a_connection_pb(plugboard_ref=plugboard_ref, connIndex=row)
        utils_cli.returningToMenuMessage("Connection was deleted.")
    else:
        utils_cli.returningToMenuMessage("Index invalid.")


def _delete_a_connection_pb(plugboard_ref: plugboards.PlugBoard, connIndex):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
        connIndex (_type_): _description_
    """
    paired_df, _ = utils.simplify_simple_dictionary_paired_unpaired(
        plugboard_ref._board_dict
    )
    for entry in paired_df.iloc[connIndex]:
        # del plugboard_ref._board_dict[entry] #Requires testing
        plugboard_ref._board_dict[entry] = entry

    plugboard_ref._update_dicts()
    # del d['k2']


def _create_a_connection_single_choice_pb(plugboard_ref: plugboards.PlugBoard):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
    """
    _, unpaired_list = utils.simplify_simple_dictionary_paired_unpaired(
        plugboard_ref._board_dict
    )
    if len(unpaired_list) < 2:
        utils_cli.returningToMenuMessage(
            "There are no letters left to pair (one or fewer left unconnected)."
        )
    utils_cli.printOutput("Unpaired letters:" + str(unpaired_list))
    letter1 = utils_cli.askingInput("Choose a letter to pair:").upper()
    if letter1 not in unpaired_list:
        utils_cli.returningToMenuMessage("Invalid input.")
    utils_cli.printOutput("Remaining letters:"), list(set(unpaired_list) - set(letter1))
    letter2 = utils_cli.askingInput("Choose the second letter:").upper()
    if letter2 not in list(set(unpaired_list) - set(letter1)):
        utils_cli.returningToMenuMessage("Invalid input.")
    plugboard_ref._board_dict[letter1] = letter2
    plugboard_ref._board_dict[letter2] = letter1
    plugboard_ref._update_dicts()
    utils_cli.returningToMenuMessage("The connection was formed.")


# First get a letter, show unconnected again, then choose to connect. If wrong choice, go back to start


def _connect_two_letters_pb(plugboard_ref: plugboards.PlugBoard):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
    """
    _, unpaired_list = utils.simplify_simple_dictionary_paired_unpaired(
        plugboard_ref._board_dict
    )
    if len(unpaired_list) < 2:
        utils_cli.returningToMenuMessage(
            "There are no letters left to pair (one or fewer left unconnected)."
        )
    while True:
        utils_cli.printOutput("Unpaired letters:" + str(unpaired_list))
        utils_cli.printOutput("If you want to stop configurating the board, press Enter.")
        letters = utils_cli.askingInput("Input two letters to pair:").strip().upper()
        if letters.isalpha() and len(letters) == 2:
            pass
        elif not letters:
            # utils_cli.returningToMenuNoMessage("No input.")
            return
        else:
            print("Error: Input 2 letters please.")
            continue
        letters = list(letters)
        if not all(map(lambda v: v in letters, unpaired_list)):
            utils_cli.printOutput("One of the letters is already connected.")
            continue
        break
    plugboard_ref._board_dict[letters[0]] = letters[1]
    plugboard_ref._board_dict[letters[1]] = letters[0]
    utils_cli.printOutput("Connection formed.")


def _form_numbered_connections_pb(plugboard_ref: plugboards.PlugBoard):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
    """
    _show_config_pb(plugboard_ref)
    _, unpaired_list = utils.simplify_simple_dictionary_paired_unpaired(
        plugboard_ref._board_dict
    )
    connections = input(
        utils_cli.askingInput(
            f"How many connections do you want to create (Max. {len(unpaired_list)})?"
        )
    )
    if connections > len(unpaired_list):
        utils_cli.returningToMenuMessage("Number exceeds the maximum.")
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
        utils_cli.clearScreenConvenience()
        utils_cli.printOutput(f"Creating connection {i+1} of {connections}")
        _create_a_connection_single_choice_pb(plugboard_ref)


def _reset_and_form_all_connections_by_pairs_pb(plugboard_ref: plugboards.PlugBoard):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
    """
    _reset_connections_pb(plugboard_ref)
    while True:
        accbool = utils_cli.askingInput("Do you want to keep making changes?[y/n]").lower()
        if accbool == "n":
            utils_cli.returningToMenuNoMessage()
        elif accbool == "y":
            _connect_two_letters_pb(plugboard_ref)


## The board is fully connected (one or fewer letters left unconnected). If wrong choice, go back to start


def _reset_and_randomize_connections_pb(plugboard_ref: plugboards.PlugBoard):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
    """
    seed = input(
        utils_cli.askingInput(
            "Introduce a positive integer as a seed to randomize the plugboard connections:"
        )
    )
    if not isinstance(seed, int) and seed > 0:
        utils_cli.returningToMenuMessage("Number is not a positive integer.")
    plugboard_ref._reset_dictionaries()
    plugboard_ref.random_setup(seed)


def _reset_connections_pb(plugboard_ref: plugboards.PlugBoard):
    """_summary_

    Args:
        plugboard_ref (plugboards.PlugBoard): _description_
    """
    plugboard_ref._reset_dictionaries()

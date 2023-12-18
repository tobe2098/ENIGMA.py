from ...core import machines
from ...core import reflectors
from ...core import utils
from .utils_f import *
import pickle
from ...core.utils import simplify_dictionary_paired_unpaired


def _show_config_rf(reflector_ref: reflectors.Reflector):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
    """

    printOutput("Reflector name: " + reflector_ref._name)
    paired_df, unpaired_list = simplify_dictionary_paired_unpaired(
        reflector_ref._reflector_dict
    )
    printOutput("Reflector pairs:")
    print(paired_df)
    printOutput("Reflector unpaired:")
    print(unpaired_list)
    returningToMenuNoMessage()


def _choose_connection_to_delete_rf(reflector_ref: reflectors.Reflector):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
    """
    paired_df, _ = utils.simplify_dictionary_paired_unpaired(reflector_ref._board_dict)

    if paired_df.shape[0] == 0:
        returningToMenuMessage("There are no available connections.")

    printOutput("Current connections are:")
    print(paired_df)
    row = askingInput("Choose a connection to delete (by index):")

    if isinstance(row, int) and row > 0 and row < paired_df.shape[0]:
        _delete_a_connection_rf(reflector_ref=reflector_ref, connIndex=row)
        returningToMenuMessage("Connection was deleted.")
    else:
        returningToMenuMessage("Index invalid.")


def _delete_a_connection_rf(reflector_ref: reflectors.Reflector, connIndex):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
        connIndex (_type_): _description_
    """
    paired_df, _ = utils.simplify_dictionary_paired_unpaired(reflector_ref._board_dict)
    for entry in paired_df.iloc[connIndex]:
        # del reflector_ref._board_dict[entry] #Requires testing
        reflector_ref[entry] = entry

    reflector_ref._update_dicts()
    # del d['k2']


def _create_a_connection_single_choice_rf(reflector_ref: reflectors.Reflector):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
    """
    _, unpaired_list = utils.simplify_dictionary_paired_unpaired(
        reflector_ref._board_dict
    )
    if len(unpaired_list) < 2:
        returningToMenuMessage(
            "There are no letters left to pair (one or fewer left unconnected)."
        )
    print(">Unpaired letters:", unpaired_list)
    letter1 = askingInput("Choose a letter to pair:").upper()
    if letter1 not in unpaired_list:
        returningToMenuMessage("Invalid input.")
    printOutput("Remaining letters:"), list(set(unpaired_list) - set(letter1))
    letter2 = askingInput("Choose the second letter:").upper()
    if letter2 not in list(set(unpaired_list) - set(letter1)):
        returningToMenuMessage("Invalid input.")
    reflector_ref._board_dict[letter1] = letter2
    reflector_ref._board_dict[letter2] = letter1
    reflector_ref._update_dicts()
    returningToMenuMessage("The connection was formed.")


# First get a letter, show unconnected again, then choose to connect. If wrong choice, go back to start


def _connect_two_letters_rf(reflector_ref: reflectors.Reflector):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
    """
    _, unpaired_list = utils.simplify_dictionary_paired_unpaired(
        reflector_ref._board_dict
    )
    if len(unpaired_list) < 2:
        returningToMenuMessage(
            "There are no letters left to pair (one or fewer left unconnected)."
        )
    while True:
        printOutput("Unpaired letters:"), unpaired_list
        printOutput("If you want to stop configurating the board, press Enter.")
        letters = askingInput("Input two letters to pair:").strip().upper()
        if letters.isalpha() and len(letters) == 2:
            pass
        elif not letters:
            returningToMenuNoMessage("No input.")
        else:
            print("Error: Input 2 letters please.")
            continue
        letters = list(letters)
        if not all(map(lambda v: v in letters, unpaired_list)):
            printOutput("One of the letters is already connected.")
            continue
        break
    reflector_ref._board_dict[letters[0]] = letters[1]
    reflector_ref._board_dict[letters[1]] = letters[0]
    printOutput("Connection formed.")


def _form_all_connections_rf(reflector_ref: reflectors.Reflector):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
    """
    _show_config_rf(reflector_ref)
    _, unpaired_list = utils.simplify_dictionary_paired_unpaired(
        reflector_ref._board_dict
    )
    _form_n_connections_rf(reflector_ref, int(len(unpaired_list) / 2))
    returningToMenuMessage(
        "There are no letters left to pair (one or fewer left unconnected)."
    )


# def reset_and_form_all_connections(reflector_ref: reflectors.Reflector):
#     """_summary_

#     Args:
#         reflector_ref (reflectors.Reflector): _description_
#     """
#     reset_connections(reflector_ref)
#     form_all_connections(reflector_ref)


def _form_n_connections_rf(reflector_ref: reflectors.Reflector, connections: int):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
        connections (int): _description_
    """
    for i in range(connections):
        clearScreenConvenience()
        printOutput(f"Creating connection {i+1} of {connections}")
        _connect_two_letters_rf(reflector_ref)


def _reset_and_streamline_connections_by_pairs_rf(reflector_ref: reflectors.Reflector):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
    """
    _reset_connections_rf(reflector_ref)
    while True:
        accbool = askingInput("Do you still want to make changes?[y/n]").lower()
        if accbool == "n":
            returningToMenuNoMessage()
        elif accbool == "y":
            break
    while True:
        _connect_two_letters_rf(reflector_ref)


## The board is fully connected (one or fewer letters left unconnected). If wrong choice, go back to start


def _reset_and_randomize_connections_rf(reflector_ref: reflectors.Reflector):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
    """
    seed = input(
        askingInput(
            "Introduce a positive integer as a seed to randomize the plugboard connections: "
        )
    )
    if not isinstance(seed, int) and seed > 0:
        returningToMenuMessage("Number is not a positive integer.")
    reflector_ref._reset_dictionaries()
    reflector_ref.random_setup(seed)


def _reset_connections_rf(reflector_ref: reflectors.Reflector):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
    """
    reflector_ref._reset_dictionaries()


def _print_name_rf(reflector_ref: reflectors.Reflector):
    printOutput("REFLECTOR NAME: " + reflector_ref._name)


def _change_reflector_name_rf(reflector_ref: reflectors.Reflector):
    new_name = str(askingInput("Input a new name for the reflector:"))
    while any(not c.isalnum() for c in new_name) or not new_name:
        printOutput("Input only alphanumerical.")
        new_name = str(askingInput("Input a new name for the reflector:"))
    reflector_ref._change_name(new_name)
    returningToMenuMessage("Reflector name changed to: " + reflector_ref._name)


def _randomize_name_rf(reflector_ref: reflectors.Reflector):
    reflector_ref.random_name()
    returningToMenuMessage("NEW NAME: " + reflector_ref.name)


def _save_in_current_directory_rf(reflector_ref: reflectors.Reflector):
    while (
        reflector_ref.name == "name"
        or reflector_ref.name == ""
        or any(not c.isalnum() for c in reflector_ref.name)
    ):
        reflector_ref._change_name(
            askingInput("Please assign a new name to the reflector:")
        ).strip()
    current_path = os.getcwd()
    new_folder = "SAVED_REFLECTORS"
    path = os.path.join(current_path, new_folder)
    if not os.path.exists(path):
        os.mkdir(path)
        printOutput("Directory '% s' created" % path)
    if checkIfFileExists(path, reflector_ref._name, "reflector"):
        printOutput("A reflector with this name already exists.")
        accbool = ""
        while not accbool == "n" or not accbool == "y":
            accbool = input(
                askingInput("Do you want to overwrite the saved reflector? [y/n]")
            ).lower()
        if accbool == "n":
            returningToMenuNoMessage()
    save_file = open(r"{}\\{}.reflector".format(path, reflector_ref._name), "wb")
    pickle.dump(reflector_ref, save_file)
    returningToMenuMessage(
        (
            "{} has been saved into {}.reflector in {}".format(
                reflector_ref.name, reflector_ref.name, path
            )
        )
    )


def _load_saved_reflector():
    current_path = os.path.dirname(__file__)
    new_folder = "SAVED_REFLECTORS"
    path = os.path.join(current_path, new_folder)
    if not os.path.exists(path):
        returningToMenuMessage("There is no {} folder.".format(path))
    list_of_files = [element.rsplit((".", 1)[0])[0] for element in os.listdir(path)]
    if len(list_of_files) == 0:
        returningToMenuMessage("There are no reflectors saved.")
    printOutput("Your available reflectors are: {}".format(list_of_files))
    reflector = askingInput("Input reflector's position in the list: ")
    while (
        not isinstance(reflector, int)
        or reflector > len(list_of_files) - 1
        or reflector < 0
    ):
        printOutput("Please input a valid index.")
        reflector = askingInput("Input reflector's position in the list:")
    filehandler = open(
        r"{}\\{}.reflector".format(path, list_of_files[reflector - 1]), "rb"
    )
    return pickle.load(filehandler)


def _exitMenu_rf(reflector_ref: reflectors.Reflector):
    _, unpaired_list = utils.simplify_dictionary_paired_unpaired(
        reflector_ref._reflector_dict
    )
    if len(unpaired_list) > 1:
        returningToMenuMessage(
            "To avoid self-sabotage, a partially connected reflector is discouraged."
        )
    exitMenu()

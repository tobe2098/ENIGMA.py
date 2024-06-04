# from ast import unparse
# from ...core import machines
import os
from ...core import reflectors
from ...utils import utils
from ...utils import utils_cli
import pickle


def _show_config_rf(reflector_ref: reflectors.Reflector):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
    """

    utils_cli.printOutput("Reflector name: ", reflector_ref._name)
    paired_df, unpaired_list = utils.simplify_simple_dictionary_paired_unpaired(
        reflector_ref._reflector_dict
    )
    utils_cli.printOutput("Reflector pairs:")
    print(paired_df)
    utils_cli.printOutput("Reflector unpaired:")
    print(unpaired_list)
    utils_cli.returningToMenu()


def _choose_connection_to_delete_rf(reflector_ref: reflectors.Reflector):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
    """
    paired_df, _ = utils.simplify_simple_dictionary_paired_unpaired(
        reflector_ref._reflector_dict
    )

    if paired_df.shape[0] == 0:
        utils_cli.returningToMenu("There are no available connections")

    utils_cli.printOutput("Current connections are:")
    print(paired_df)
    row = utils_cli.askingInput("Choose a connection to delete (by index):")

    if isinstance(row, int) and row > 0 and row < paired_df.shape[0]:
        __delete_a_connection_rf(reflector_ref=reflector_ref, connIndex=row)
        utils_cli.returningToMenu("Connection was deleted")
    else:
        utils_cli.returningToMenu("Index invalid")


def __delete_a_connection_rf(reflector_ref: reflectors.Reflector, connIndex):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
        connIndex (_type_): _description_
    """
    paired_df, _ = utils.simplify_simple_dictionary_paired_unpaired(
        reflector_ref._reflector_dict
    )
    for entry in paired_df.iloc[connIndex]:
        # del reflector_ref._reflector_dict[entry] #Requires testing
        reflector_ref._reflector_dict[entry] = entry

    reflector_ref._update_dicts()
    # del d['k2']


def _create_a_connection_single_choice_rf(reflector_ref: reflectors.Reflector):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
    """
    _, unpaired_list = utils.simplify_simple_dictionary_paired_unpaired(
        reflector_ref._reflector_dict
    )
    if len(unpaired_list) < 2:
        utils_cli.returningToMenu(
            "There are no letters left to pair (one or fewer left unconnected)"
        )
    utils_cli.printOutput("Unpaired letters:", (unpaired_list))
    letter1 = utils_cli.askingInput("Choose a letter to pair:").upper()
    if letter1 not in unpaired_list:
        utils_cli.returningToMenu("Invalid input")
    utils_cli.printOutput("Remaining letters:"), list(set(unpaired_list) - set(letter1))
    letter2 = utils_cli.askingInput("Choose the second letter:").upper()
    if letter2 not in list(set(unpaired_list) - set(letter1)):
        utils_cli.returningToMenu("Invalid input")
    reflector_ref._reflector_dict[letter1] = letter2
    reflector_ref._reflector_dict[letter2] = letter1
    reflector_ref._update_dicts()
    utils_cli.returningToMenu("The connection was formed")


# First get a letter, show unconnected again, then choose to connect. If wrong choice, go back to start


def __connect_all_letters_rf(reflector_ref: reflectors.Reflector):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
    """
    # _, unpaired_list = utils.simplify_simple_dictionary_paired_unpaired(
    #     reflector_ref._reflector_dict
    # )
    # if len(unpaired_list) < 2:
    #     utils_cli.returningToMenuMessage(
    #         "There are no letters left to pair (one or fewer left unconnected)"
    #     )
    while True:
        _, unpaired_list = utils.simplify_simple_dictionary_paired_unpaired(
            reflector_ref._reflector_dict
        )
        if len(unpaired_list) < 2:
            utils_cli.returningToMenu(
                "There are no letters left to pair (one or fewer left unconnected)"
            )
        utils_cli.printOutput("Unpaired letters:", (unpaired_list))
        utils_cli.printOutput(
            "If you want to stop configurating the board, press Enter"
        )
        letters = utils_cli.askingInput("Input two letters to pair:").strip().upper()
        if letters.isalpha() and len(letters) == 2:
            pass
        elif not letters:
            return
        else:
            print("Error: Input 2 letters please")
            continue
        letters = list(letters)
        if not all(map(lambda v: v in letters, unpaired_list)):
            utils_cli.printOutput("One of the letters is already connected")
            continue
        # break
        reflector_ref._reflector_dict[letters[0]] = letters[1]
        reflector_ref._reflector_dict[letters[1]] = letters[0]
        utils_cli.printOutput("Connection formed")


def _form_all_connections_rf(reflector_ref: reflectors.Reflector):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
    """
    _show_config_rf(reflector_ref)
    # _, unpaired_list = utils.simplify_simple_dictionary_paired_unpaired(
    #     reflector_ref._reflector_dict
    # )
    __connect_all_letters_rf(reflector_ref)
    utils_cli.returningToMenu("You exited without forming all connections!")


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
        utils_cli.clearScreenConvenienceCli()
        utils_cli.printOutput(f"Creating connection {i+1} of {connections}")
        _create_a_connection_single_choice_rf(reflector_ref)


def _reset_and_form_all_connections_by_pairs_rf(reflector_ref: reflectors.Reflector):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
    """
    _reset_connections_rf(reflector_ref)
    while True:
        accbool = utils_cli.askingInput(
            "Do you still want to make changes?[y/n]"
        ).lower()
        if accbool == "n":
            utils_cli.returningToMenu()
        elif accbool == "y":
            break
    __connect_all_letters_rf(reflector_ref)


## The board is fully connected (one or fewer letters left unconnected). If wrong choice, go back to start


def _reset_and_randomize_connections_rf(reflector_ref: reflectors.Reflector):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
    """
    seed = input(
        utils_cli.askingInput(
            "Introduce a positive integer as a seed to randomize the reflector connections: "
        )
    )
    if not isinstance(seed, int) and seed > 0:
        utils_cli.returningToMenu("Number is not a positive integer")
    reflector_ref._reset_dictionaries()
    reflector_ref._random_setup(seed)


def _reset_connections_rf(reflector_ref: reflectors.Reflector):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
    """
    reflector_ref._reset_dictionaries()


def _print_name_rf(reflector_ref: reflectors.Reflector):
    utils_cli.printOutput("REFLECTOR NAME: ", reflector_ref._name)


def _change_reflector_name_rf(reflector_ref: reflectors.Reflector):
    new_name = str(utils_cli.askingInput("Input a new name for the reflector:"))
    while any(not c.isalnum() for c in new_name) or not new_name:
        utils_cli.printOutput("Input only alphanumerical characters or underscore")
        new_name = str(utils_cli.askingInput("Input a new name for the reflector:"))
    reflector_ref._change_name(new_name)
    utils_cli.returningToMenu("Reflector name changed to: ", reflector_ref._name)


def _randomize_name_rf(reflector_ref: reflectors.Reflector):
    reflector_ref._random_name()
    utils_cli.returningToMenu("NEW NAME: ", reflector_ref.name)


def _save_in_current_directory_rf(reflector_ref: reflectors.Reflector):
    while (
        reflector_ref.name == "name"
        or reflector_ref.name == ""
        or any(not c.isalnum() for c in reflector_ref.name)
    ):
        reflector_ref._change_name(
            utils_cli.askingInput("Please assign a new name to the reflector:")
        ).strip()
    current_path = os.getcwd()
    new_folder = utils.REFLECTORS_FILE_HANDLE
    path = os.path.join(current_path, new_folder)
    if not os.path.exists(path):
        os.mkdir(path)
        utils_cli.printOutput("Directory '% s' created" % path)
    if utils_cli.checkIfFileExists(path, reflector_ref._name, "reflector"):
        utils_cli.printOutput("A reflector with this name already exists")
        accbool = ""
        while not accbool == "n" or not accbool == "y":
            accbool = input(
                utils_cli.askingInput(
                    "Do you want to overwrite the saved reflector? [y/n]"
                )
            ).lower()
        if accbool == "n":
            utils_cli.returningToMenu()
    save_file = open(r"{}\\{}.reflector".format(path, reflector_ref._name), "wb")
    pickle.dump(reflector_ref, save_file)
    utils_cli.returningToMenu(
        (
            "{} has been saved into {}.reflector in {}".format(
                reflector_ref.name, reflector_ref.name, path
            )
        )
    )


def _load_saved_reflector():
    current_path = os.path.dirname(__file__)
    new_folder = utils.REFLECTORS_FILE_HANDLE
    path = os.path.join(current_path, new_folder)
    if not os.path.exists(path):
        utils_cli.returningToMenu("There is no {} folder".format(path))
    list_of_files = [element.rsplit((".", 1)[0])[0] for element in os.listdir(path)]
    if len(list_of_files) == 0:
        utils_cli.returningToMenu("There are no reflectors saved")
    utils_cli.printOutput("Your available reflectors are:")
    utils_cli.printListOfOptions(list_of_files)
    reflector = utils_cli.askingInput("Input reflector's position in the list: ")
    while (
        not isinstance(reflector, int)
        or reflector > len(list_of_files) - 1
        or reflector < 0
    ):
        utils_cli.printOutput("Please input a valid index")
        reflector = utils_cli.askingInput("Input reflector's position in the list:")
    filehandler = open(r"{}\\{}.reflector".format(path, list_of_files[reflector]), "rb")
    return pickle.load(filehandler)


def _exitMenu_rf(reflector_ref: reflectors.Reflector):
    _, unpaired_list = utils.simplify_simple_dictionary_paired_unpaired(
        reflector_ref._reflector_dict
    )
    if len(unpaired_list) > 1:
        utils_cli.returningToMenu(
            "To avoid self-sabotage, a partially connected reflector is discouraged"
        )
    utils_cli.exitMenu()

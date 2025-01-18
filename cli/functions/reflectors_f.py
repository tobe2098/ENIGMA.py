# from ast import unparse
# from ...core import machines
import os
import string


from utils.exceptions import FileIOErrorException
from utils.types_utils import getLowerCaseName
from ...core import reflectors
from ...utils import utils
from ...utils import utils_cli
import pickle


def _show_config_rf(reflector_ref: reflectors.Reflector):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
    """

    utils_cli.printOutput("Reflector name:", reflector_ref._name)
    paired_df, unpaired_list = utils.simplify_simple_dictionary_paired_unpaired(
        reflector_ref._reflector_dict
    )
    utils_cli.printOutput("Reflector pairs:\n", paired_df)
    utils_cli.printOutput("Reflector unpaired:", unpaired_list)
    if len(unpaired_list) < 2:
        reflector_ref.lacks_connections = False
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
        utils_cli.returningToMenu("There are no available connections to delete")

    utils_cli.printOutput("Current connections are:\n", paired_df)
    row = utils_cli.askingInput("Choose a connection to delete (by index)")
    row = utils_cli.checkInputValidity(row, int, rangein=(0, paired_df.shape[0]))
    if row:
        # if isinstance(row, int) and row > 0 and row < paired_df.shape[0]:
        __delete_a_connection_rf(
            reflector_ref=reflector_ref, character1=paired_df.iloc[row][0]
        )
        reflector_ref.lacks_connections = True
        utils_cli.returningToMenu("Connection was deleted")
    else:
        utils_cli.returningToMenu("Index invalid", output_type="e")


def __delete_a_connection_rf(reflector_ref: reflectors.Reflector, character1: str):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
        connIndex (_type_): _description_
    """

    # del reflector_ref._reflector_dict[entry] #Requires testing
    (
        reflector_ref._reflector_dict[character1],
        reflector_ref._reflector_dict[reflector_ref._reflector_dict[character1]],
    ) = (
        reflector_ref._reflector_dict[reflector_ref._reflector_dict[character1]],
        reflector_ref._reflector_dict[character1],
    )
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
        reflector_ref.lacks_connections = False
        utils_cli.returningToMenu(
            "There are no characters left to pair (one or fewer left unconnected)"
        )
    utils_cli.printOutput("Unpaired characters:", unpaired_list)
    character1 = utils_cli.askingInput("Choose a character to pair")
    character1 = utils_cli.checkInputValidity(character1, rangein=unpaired_list)
    if not character1:
        # if character1 not in unpaired_list:
        utils_cli.printError("Invalid input")
        return False
        # utils_cli.returningToMenu("Invalid input", output_type="e")
    utils_cli.printOutput(
        "Remaining characters:", list(set(unpaired_list) - set(character1))
    )
    character2 = utils_cli.askingInput("Choose the second character:")
    character2 = utils_cli.checkInputValidity(
        character2, rangein=list(set(unpaired_list) - set(character1))
    )
    if not character2:
        # if character2 not in list(set(unpaired_list) - set(character1)):
        utils_cli.printError("Invalid input")
        return False
        # utils_cli.returningToMenu("Invalid input", output_type="e")
    reflector_ref._reflector_dict[character1] = character2
    reflector_ref._reflector_dict[character2] = character1
    reflector_ref._update_dicts()
    utils_cli.printOutput("The connection was formed")
    return True
    # utils_cli.returningToMenu("The connection was formed")


# First get a character, show unconnected again, then choose to connect. If wrong choice, go back to start


def __connect_all_characters_rf(reflector_ref: reflectors.Reflector):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
    """
    # _, unpaired_list = utils.simplify_simple_dictionary_paired_unpaired(
    #     reflector_ref._reflector_dict
    # )
    # if len(unpaired_list) < 2:
    #     utils_cli.returningToMenuMessage(
    #         "There are no characters left to pair (one or fewer left unconnected)"
    #     )
    while True:
        _, unpaired_list = utils.simplify_simple_dictionary_paired_unpaired(
            reflector_ref._reflector_dict
        )
        if len(unpaired_list) < 2:
            reflector_ref.lacks_connections = False
            utils_cli.returningToMenu(
                "There are no characters left to pair (one or fewer left unconnected)"
            )
        utils_cli.printOutput("Unpaired characters:", unpaired_list)
        utils_cli.printOutput(
            "If you want to stop configurating the board, press Enter"
        )
        characters = utils_cli.askingInput("Input two characters to pair").strip(
            chars=string.whitespace
        )
        if characters.isalpha() and len(characters) == 2:
            pass
        elif not characters:
            utils_cli.returningToMenu()
        else:
            utils_cli.printError("Input 2 characters please")
            continue
        characters = list(characters)
        for i in range(2):
            characters[i] = utils_cli.checkInputValidity(
                characters[i], rangein=unpaired_list
            )
        if not all(characters):
            # if not all(map(lambda v: v in characters, unpaired_list)):
            utils_cli.printOutput("One of the characters is already connected")
            continue
        # break
        reflector_ref._reflector_dict[characters[0]] = characters[1]
        reflector_ref._reflector_dict[characters[1]] = characters[0]
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
    __connect_all_characters_rf(reflector_ref)
    utils_cli.returningToMenu(
        "You exited without forming all connections!", output_type="w"
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
    c = 0
    while connections - c:
        # for i in range(connections):
        utils_cli.clearScreenConvenienceCli()
        utils_cli.printOutput(f"Creating connection {c+1} of {connections}")
        if _create_a_connection_single_choice_rf(reflector_ref):
            c += 1


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
    __connect_all_characters_rf(reflector_ref)


## The board is fully connected (one or fewer characters left unconnected). If wrong choice, go back to start


def _reset_and_randomize_connections_rf(reflector_ref: reflectors.Reflector):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
    """
    seed = utils_cli.getSeedFromUser()
    reflector_ref._reset_dictionaries()
    reflector_ref._random_setup(seed)


def _reset_connections_rf(reflector_ref: reflectors.Reflector):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
    """
    reflector_ref._reset_dictionaries()


def _print_name_rf(reflector_ref: reflectors.Reflector):
    utils_cli.printOutput("Reflector name:", reflector_ref._name)


def _change_reflector_name_rf(reflector_ref: reflectors.Reflector):
    new_name = utils_cli.askingInput("Input a new name for the reflector")
    while not reflector_ref._is_name_valid(new_name):
        # while any(not c.isalnum() for c in new_name) or not new_name:
        utils_cli.printOutput("Input only alphanumerical characters or underscore")
        new_name = utils_cli.askingInput("Input a new name for the reflector")
    reflector_ref._change_name(new_name)
    utils_cli.returningToMenu("Reflector name changed to:", reflector_ref._name)


def _randomize_name_rf(reflector_ref: reflectors.Reflector):
    reflector_ref._random_name()
    utils_cli.returningToMenu("Reflector's new name:", reflector_ref.name)


def _save_reflector_in_its_folder(reflector_ref: reflectors.Reflector):
    accbool = ""
    while not accbool == "n" or not accbool == "y":
        accbool = utils_cli.askingInput(
            f"Would you like to save the machine in use? If not, unsaved changes will be discarded. [y/n]"
        ).lower()
    if accbool == "n":
        utils_cli.returningToMenu()
    new_name = reflector_ref.get_name()
    while not reflector_ref._is_name_valid(new_name):
        new_name = utils_cli.askingInput(
            f"Please assign a new name to the {getLowerCaseName(reflector_ref)}"
        ).strip(chars=string.whitespace)
    reflector_ref._change_name(new_name)

    path = utils.Constants.REFLECTOR_FILE_PATH
    if not os.path.exists(path):
        os.mkdir(path)
        utils_cli.printOutput(f"Directory '{path}' created")
    if utils_cli.checkIfFileExists(
        path, reflector_ref._name, getLowerCaseName(reflector_ref)
    ):
        utils_cli.printOutput(
            f"A {getLowerCaseName(reflector_ref)} with this name already exists"
        )
        accbool = ""
        while not accbool == "n" or not accbool == "y":
            accbool = utils_cli.askingInput(
                f"Do you want to overwrite the saved {getLowerCaseName(reflector_ref)}? [y/n]"
            ).lower()
        if accbool == "n":
            utils_cli.returningToMenu(
                f"You discarded changes to the {getLowerCaseName(reflector_ref)}"
            )
    file_path = os.path.join(
        path, f"{reflector_ref._name}.{getLowerCaseName(reflector_ref)}"
    )
    try:
        save_file = open(file_path, "wb")
        pickle.dump(reflector_ref, save_file)
        save_file.close()
    except Exception as e:
        raise FileIOErrorException(
            f"Failed to save the {getLowerCaseName(reflector_ref)} at {file_path}:{e}"
        )
    utils_cli.returningToMenu(
        f"{reflector_ref._name} has been saved into {reflector_ref._name}.{getLowerCaseName(reflector_ref)} in {path}"
    )


def _load_saved_reflector(reflector_id: reflectors.Reflector | None = None):
    if reflector_id and reflector_id.is_set_up():
        _save_reflector_in_its_folder(reflector_ref=reflector_id)
    path = utils.Constants.REFLECTOR_FILE_PATH
    if not os.path.exists(path):
        utils_cli.returningToMenu("There is no {} folder".format(path), output_type="e")
    list_of_files = [
        element.rsplit(".", 1)[0]
        for element in os.listdir(path)
        # if element.rsplit(".", 1)[1] == "reflector"
    ]
    if not list_of_files:
        utils_cli.returningToMenu(f"There are no reflectors saved at {path}", "e")
    utils_cli.printOutput("Your available reflectors are:")
    utils_cli.printListOfOptions(list_of_files)
    reflector_id = utils_cli.askingInput("Input reflector's position in the list:")
    reflector_id = utils_cli.checkInputValidity(
        reflector_id, int, rangein=(0, len(list_of_files))
    )
    while not reflector_id:
        # while not isinstance(rotor, int) or rotor > len(list_of_files) - 1 or rotor < 0:
        utils_cli.printError("Please input a valid index")
        utils_cli.printListOfOptions(list_of_files)
        reflector_id = utils_cli.askingInput("Input reflector's position in the list:")
        if not reflector_id:
            utils_cli.returningToMenu()
        reflector_id = utils_cli.checkInputValidity(
            reflector_id, int, rangein=(0, len(list_of_files))
        )
    try:
        filehandler = open(
            os.path.join(path, f"{list_of_files[reflector_id]}.rotor")(
                path, list_of_files[reflector_id]
            ),
            "rb",
        )
        reflector_ref = pickle.load(filehandler)
        filehandler.close()
    except Exception as e:
        utils_cli.returningToMenu(
            f"Failed to read the file at {filehandler}:{e}", output_type="e"
        )
    if isinstance(reflector_ref, reflectors.Reflector):
        return reflector_ref
    else:
        utils_cli.returningToMenu(
            f"A non-reflector type was loaded:{type(reflector_ref)}", output_type="e"
        )


def _exitMenu_rf(reflector_ref: reflectors.Reflector):
    # _, unpaired_list = utils.simplify_simple_dictionary_paired_unpaired(
    #     reflector_ref._reflector_dict
    # )
    if not reflector_ref.is_set_up():
        utils_cli.returningToMenu(
            "To avoid self-sabotage, an improper reflector is discouraged"
        )
    utils_cli.exitMenu()

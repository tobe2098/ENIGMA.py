## New seeds for standalone generated rotors, reflectors and boards
### EACH OBJECT SET OF MENUS TAKES THE REFERENCE FROM THE MACHINE, AND THEN OPERATES ON IT, EFFECTIVELY NOT TOUCHING THE MACHINE ITSELF BUT ITS OBJECTS
### EXCEPT FOR LOADING!!!!!! LOADING OF ITEMS HAS TO BE DONE DIRECTLY IN THE MACHINE MENU
### ALSO EXCEPT ALL GENERALISTIC CONFIG CALLS
### PUT WARNING IN ALL MENUING RELATED TO JUMP (IN RANDOM JUMP IS ALWAYS 1?)never zero or no_chars%jump==0!!, write explanation of interplay between notches and jump
# Intern setup functions
from utils.exceptions import FileIOErrorException
from utils.types_utils import getLowerCaseName, isDashedObject
from ...core import rotors
from ...utils import utils
from ...utils import utils_cli
import random
import os
import pickle

# from copy import copy


def _show_config_rt(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    (paired_df, unpaired, unformed, _) = (
        utils.simplify_rotor_dictionary_paired_unpaired(
            rotor_ref._forward_dict, rotor_ref._backward_dict
        )
    )
    unpaired.extend(unformed)
    utils_cli.printOutput(
        "Rotor character position :",
        str(rotor_ref._conversion_in_use[rotor_ref._position]),
    )
    utils_cli.printOutput("Rotor character jumps:", str(rotor_ref._jump))
    notchlist = [rotor_ref._conversion_in_use[i] for i in rotor_ref._notches]
    utils_cli.printOutput("Rotor notches:", str(notchlist))
    utils_cli.printOutput("Forward connections in the rotor:\n", paired_df)
    utils_cli.printOutput("Bad connections (self or none) in the rotor:", str(unpaired))

    # utils_cli.printOutput(
    #     "Backward connections in the rotor:", str(rotor_ref._backward_dict)
    # )
    utils_cli.printOutput("Rotor name:", str(rotor_ref._name))
    (
        _,
        unpaired,
        unformed,
        _,
    ) = utils.simplify_rotor_dictionary_paired_unpaired(
        rotor_ref._forward_dict, rotor_ref._backward_dict
    )
    if not unformed:
        rotor_ref.lacks_connections = False
    if len(unpaired) > 0:
        utils_cli.printWarning(
            "One or more connections are self-connections. This may go against proper practice"
        )
    utils_cli.returningToMenu()


# For now, in text, there will be no connection deletion? Or will there?
def _choose_connection_to_delete_rt(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    paired_df, _, _, _ = utils.simplify_rotor_dictionary_paired_unpaired(
        rotor_ref._forward_dict, rotor_ref._backward_dict
    )

    if paired_df.shape[0] == 0:
        utils_cli.returningToMenu("There are no available connections")

    utils_cli.printOutput("Current connections are:\n", paired_df)
    row = utils_cli.askingInput("Choose a connection to delete (by index)")

    row = utils_cli.checkInputValidity(row, int, rangein=(0, paired_df.shape[0]))

    if row:
        # if isinstance(row, int) and row > 0 and row < paired_df.shape[0]:
        _delete_a_connection_rt(rotor_ref=rotor_ref, char1=paired_df.iloc[row][0])
        utils_cli.returningToMenu("Connection was deleted")
    else:
        utils_cli.returningToMenu("Index invalid", output_type="e")


def _delete_a_connection_rt(rotor_ref: rotors.Rotor, char1: str):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
        connIndex (_type_): _description_
    """
    rotor_ref._backward_dict[rotor_ref._forward_dict[char1]] = ""
    # del rotor_ref._board_dict[entry] #Requires testing
    rotor_ref._forward_dict[char1] = ""
    rotor_ref.lacks_connections = True
    rotor_ref._update_dicts()
    # del d['k2']


def _create_a_connection_single_choice_rt(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    (
        _,
        _,
        front_unformed,
        back_unformed,
    ) = utils.simplify_rotor_dictionary_paired_unpaired(
        rotor_ref._forward_dict, rotor_ref._backward_dict
    )
    if len(front_unformed) == 0 and len(back_unformed) == 0:
        rotor_ref.lacks_connections = False
        utils_cli.returningToMenu(
            "There are no characters left to pair (one or fewer left unconnected)",
        )
    utils_cli.printOutput("Unpaired character in front side:", front_unformed)

    character1 = utils_cli.askingInput("Choose a character to pair from front side")
    character1 = utils_cli.checkInputValidity(character1, rangein=front_unformed)
    if not character1:
        # if character1 not in front_unformed:
        utils_cli.returningToMenu("Invalid input", output_type="e")
    utils_cli.printOutput("Unpaired characters in back side:", back_unformed)
    character2 = utils_cli.askingInput("Choose the second character from the back side")
    character2 = utils_cli.checkInputValidity(character2, rangein=back_unformed)
    if not character2:
        # if character2 not in back_unformed:
        utils_cli.returningToMenu("Invalid input", output_type="e")
    rotor_ref._forward_dict[character1] = character2
    rotor_ref._backward_dict[character2] = character1
    rotor_ref._update_dicts()
    utils_cli.returningToMenu("The connection was formed")
    if len(front_unformed) - 1 == 0 and len(back_unformed) - 1 == 0:
        rotor_ref.lacks_connections = False


# First get a character, show unconnected again, then choose to connect. If wrong choice, go back to start


def _connect_all_characters_rt(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    # (
    #     _,
    #     _,
    #     front_unformed,
    #     back_unformed,
    # ) = utils.simplify_rotor_dictionary_paired_unpaired(
    #     rotor_ref._forward_dict, rotor_ref._backward_dict
    # )
    # if len(front_unformed) == 0 and len(back_unformed) == 0:
    #     rotor_ref.lacks_conn = True
    #     utils_cli.returningToMenuMessage(
    #         "There are no characters left to pair (one or fewer left unconnected)"
    #     )
    while True:
        (
            _,
            _,
            front_unformed,
            back_unformed,
        ) = utils.simplify_rotor_dictionary_paired_unpaired(
            rotor_ref._forward_dict, rotor_ref._backward_dict
        )
        if len(front_unformed) == 0 and len(back_unformed) == 0:
            rotor_ref.lacks_connections = False
            utils_cli.returningToMenu(
                "There are no characters left to pair (one or fewer left unconnected)",
            )
        utils_cli.printOutput("Unpaired characters in front side:", (front_unformed))
        utils_cli.printOutput("Unpaired characters in back side:", (back_unformed))
        utils_cli.printOutput(
            "If you want to stop configurating the board, just press Enter"
        )
        characters = utils_cli.askingInput(
            "Input one character from front side, one from back side (in order)"
        ).strip()
        characters = list(characters)
        if len(characters) == 2 and all(
            character in utils.get_character_list_from_obj(rotor_ref)
            for character in characters
        ):
            pass
        elif not characters:
            return
        else:
            utils_cli.printError("Input only two allowed characters")
            continue
        characters[0] = utils_cli.checkInputValidity(
            characters[0], rangein=front_unformed
        )
        characters[1] = utils_cli.checkInputValidity(
            characters[1], rangein=back_unformed
        )
        if not all(characters):
            # if characters[0] not in front_unformed or characters[1] not in back_unformed:
            utils_cli.printError("One or more characters are already connected")
            continue
        # break
        rotor_ref._forward_dict[characters[0]] = characters[1]
        rotor_ref._backward_dict[characters[1]] = characters[0]
        utils_cli.printOutput("Connection formed")


def _form_all_connections_rt(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    _show_config_rt(rotor_ref)
    # _, unpaired_list = utils.simplify_simple_dictionary_paired_unpaired(
    #     rotor_ref._board_dict
    # )
    _connect_all_characters_rt(rotor_ref)
    rotor_ref.lacks_connections = True
    utils_cli.returningToMenu(
        "You exited without forming all connections!", output_type="w"
    )

    # utils_cli.returningToMenuMessage(
    #     "There are no characters left to pair (one or fewer left unconnected)"
    # )


# def reset_and_form_all_connections(rotor_ref: rotors.Rotor):
#     """_summary_

#     Args:
#         rotor_ref (rotors.Rotor): _description_
#     """
#     reset_connections(rotor_ref)
#     form_all_connections(rotor_ref)


def _swap_two_connections_rt(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
        connections (int): _description_
    """
    (paired_df, _, _, _) = utils.simplify_rotor_dictionary_paired_unpaired(
        rotor_ref._forward_dict, rotor_ref._backward_dict
    )
    utils_cli.printOutput("Current connections are:\n", paired_df)
    character1 = utils_cli.askingInput("Choose a frontside connection by the index")
    character1 = utils_cli.checkInputValidity(
        character1, int, rangein=(0, paired_df.shape[0])
    )
    # character1 = utils_cli.checkInputValidity(character1, _range=rotor_ref._characters_in_use)
    if not character1:
        # if character1 not in rotor_ref._characters_in_use:
        utils_cli.printError("Invalid input")
        return
    character2 = utils_cli.askingInput(
        "Choose a second frontside connection by the index to swap"
    )
    character2 = utils_cli.checkInputValidity(
        character2, int, rangein=(0, paired_df.shape[0])
    )
    # character2 = utils_cli.checkInputValidity(character2, _range=rotor_ref._characters_in_use)
    if not character2:
        # if character2 not in rotor_ref._characters_in_use:
        utils_cli.printError("Invalid input")
        return
    (
        rotor_ref._backward_dict[rotor_ref._forward_dict[character1]],
        rotor_ref._backward_dict[rotor_ref._forward_dict[character2]],
    ) = (
        rotor_ref._backward_dict[rotor_ref._forward_dict[character2]],
        rotor_ref._backward_dict[rotor_ref._forward_dict[character1]],
    )
    rotor_ref._forward_dict[character1], rotor_ref._forward_dict[character2] = (
        rotor_ref._forward_dict[character2],
        rotor_ref._forward_dict[character1],
    )
    rotor_ref._update_dicts()
    utils_cli.printOutput("The connection was swapped")


def _swap_connections_rt(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    while True:
        accbool = utils_cli.askingInput(
            "If you do not want to continue swapping, enter n"
        ).lower()
        if accbool == "n":
            utils_cli.returningToMenu()
        _swap_two_connections_rt(rotor_ref=rotor_ref)

    # utils_cli.returningToMenuMessage(
    #     "There are no characters left to pair (one or fewer left unconnected)."
    # )


def _reset_connections_rt(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    rotor_ref._reset_dictionaries()
    rotor_ref.lacks_connections = True


def _reset_and_streamline_connections_by_pairs_rt(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    _reset_connections_rt(rotor_ref)
    # while True:
    #     accbool = utils_cli.utils_cli.askingInput("Do you still want to make changes?[y/n]").lower()
    #     if accbool == "n":
    #         utils_cli.returningToMenu()
    #     elif accbool == "y":
    #         break
    _connect_all_characters_rt(rotor_ref)
    rotor_ref.lacks_connections = True
    utils_cli.returningToMenu(
        "You exited without forming all connections!", output_type="w"
    )


def _reset_and_randomize_connections_rt(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    seed = utils_cli.getSeedFromUser()

    # rotor_ref._reset_dictionaries() Necessary?
    rotor_ref._randomize_dictionaries(seed)
    utils_cli.returningToMenu("Rotor connections established")


def _print_name_rt(rotor_ref: rotors.Rotor):
    utils_cli.printOutput("Current rotor name:", rotor_ref._name)


def _change_rotor_name_rt(rotor_ref: rotors.Rotor):
    _print_name_rt(rotor_ref)
    new_name = utils_cli.askingInput("Input a new name for the rotor")
    while not rotor_ref._is_name_valid(new_name):
        utils_cli.printOutput("Input only alphanumerical characters or underscores")
        new_name = utils_cli.askingInput("Input a new name for the rotor")
    rotor_ref._change_name(new_name)
    utils_cli.returningToMenu("Rotor name changed to:", rotor_ref._name)


def _randomize_name_rt(rotor_ref: rotors.Rotor):
    seed = utils_cli.getSeedFromUser()
    rotor_ref._random_name(seed)
    utils_cli.returningToMenu("Rotor name changed to:", rotor_ref._name)


def _change_notches_rt(rotor_ref: rotors.Rotor):
    utils_cli.printOutput("Rotor notches:", rotor_ref.get_notchlist_characters())
    positions = [
        i
        for i in utils_cli.askingInput(
            "Input new notches separated by a space (empty to skip)"
        ).split()
    ]
    if not positions:
        utils_cli.returningToMenu()
    while not rotor_ref._are_notches_invalid(positions):
        utils_cli.printError("Input invalid")
        positions = [
            i
            for i in utils_cli.askingInput(
                "Input new notches separated by a space (empty to skip)"
            ).split()
        ]
        if not positions:
            utils_cli.returningToMenu()

    rotor_ref._define_notches(positions)


def _randomize_notches_rt(rotor_ref: rotors.Rotor):
    seed = utils_cli.getSeedFromUser()
    rotor_ref._randomize_notches(seed=seed)
    utils_cli.printOutput("New rotor notches:", rotor_ref.get_notchlist_characters())
    utils_cli.returningToMenu("Rotor notches established")


def _change_position_rt(rotor_ref: rotors.Rotor):
    new_position = utils_cli.askingInput(
        "Input a single allowed character to set the rotor to a new position"
    )
    while rotor_ref._is_position_invalid(new_position):
        utils_cli.printError("Input only allowed characters")
        utils_cli.printOutput(utils.get_character_list_from_obj(rotor_ref))
        new_position = utils_cli.askingInput(
            "Input a single allowed character to set the rotor to a new position"
        )
    rotor_ref._define_position(new_position)
    utils_cli.returningToMenu("Rotor position set to:", rotor_ref.get_position())


def _randomize_position_rt(rotor_ref: rotors.Rotor):
    seed = utils_cli.getSeedFromUser()
    rotor_ref._randomize_position(seed)
    utils_cli.returningToMenu("Rotor position set to:", rotor_ref.get_position())


def _save_rotor_in_its_folder(rotor_ref: rotors.Rotor):
    new_name = rotor_ref.get_name()
    while not rotor_ref._is_name_valid(new_name):
        new_name = utils_cli.askingInput(
            f"Please assign a new name to the {getLowerCaseName(rotor_ref)}"
        ).strip()
    rotor_ref._change_name(new_name)

    path = utils.Constants.ROTOR_FILE_PATH
    if not os.path.exists(path):
        os.mkdir(path)
        utils_cli.printOutput(f"Directory '{path}' created")
    if utils_cli.checkIfFileExists(path, rotor_ref._name, getLowerCaseName(rotor_ref)):
        utils_cli.printOutput(
            f"A {getLowerCaseName(rotor_ref)} with this name already exists"
        )
        accbool = ""
        while not accbool == "n" or not accbool == "y":
            accbool = utils_cli.askingInput(
                f"Do you want to overwrite the saved {getLowerCaseName(rotor_ref)}? [y/n]"
            ).lower()
        if accbool == "n":
            utils_cli.returningToMenu(
                f"You discarded changes to the {getLowerCaseName(rotor_ref)}"
            )
    file_path = os.path.join(path, f"{rotor_ref._name}.{getLowerCaseName(rotor_ref)}")
    try:
        save_file = open(file_path, "wb")
        pickle.dump(rotor_ref, save_file)
        save_file.close()
    except Exception as e:
        raise FileIOErrorException(
            f"Failed to save the {getLowerCaseName(rotor_ref)} at {file_path}:{e}"
        )
    utils_cli.returningToMenu(
        f"{rotor_ref._name} has been saved into {rotor_ref._name}.{getLowerCaseName(rotor_ref)} in {path}"
    )


def _load_saved_rotor():
    path = utils.Constants.ROTOR_FILE_PATH
    if not os.path.exists(path):
        utils_cli.returningToMenu("There is no {} folder".format(path), output_type="e")
    list_of_files = [element.rsplit((".", 1)[0])[0] for element in os.listdir(path)]
    if not list_of_files:
        utils_cli.returningToMenu(f"There are no rotors saved at {path}", "e")
    utils_cli.printOutput("Your available rotors are:")
    utils_cli.printListOfOptions(list_of_files)
    rotor = utils_cli.askingInput("Input rotor's position in the list:")
    rotor = utils_cli.checkInputValidity(rotor, int, rangein=(0, len(list_of_files)))
    while not rotor:
        # while not isinstance(rotor, int) or rotor > len(list_of_files) - 1 or rotor < 0:
        utils_cli.printError("Please input a valid index")
        utils_cli.printListOfOptions(list_of_files)
        rotor = utils_cli.askingInput("Input rotor's position in the list:")
        if not rotor:
            utils_cli.returningToMenu()
        rotor = utils_cli.checkInputValidity(
            rotor, int, rangein=(0, len(list_of_files))
        )
    try:
        filehandler = open(
            os.path.join(path, f"{list_of_files[rotor]}.rotor")(
                path, list_of_files[rotor]
            ),
            "rb",
        )
        rotor_ref = pickle.load(filehandler)
        filehandler.close()
    except Exception as e:
        utils_cli.returningToMenu(
            f"Failed to read the file at {filehandler}:{e}", output_type="e"
        )
    return rotor_ref


def _exitMenu_rt(rotor_ref: rotors.Rotor):
    # (
    #     _,
    #     _,
    #     front_unformed,
    #     _,
    # ) = utils.simplify_rotor_dictionary_paired_unpaired(
    #     rotor_ref._forward_dict, rotor_ref._backward_dict
    # )
    if not rotor_ref.is_set_up():
        utils_cli.returningToMenu(
            "Due to implementation reasons, an improperly setup rotor is not allowed",
            "e",
        )
    utils_cli.exitMenu()

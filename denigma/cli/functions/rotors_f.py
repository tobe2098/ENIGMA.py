## New seeds for standalone generated rotors, reflectors and boards
### EACH OBJECT SET OF MENUS TAKES THE REFERENCE FROM THE MACHINE, AND THEN OPERATES ON IT, EFFECTIVELY NOT TOUCHING THE MACHINE ITSELF BUT ITS OBJECTS
### EXCEPT FOR LOADING!!!!!! LOADING OF ITEMS HAS TO BE DONE DIRECTLY IN THE MACHINE MENU
### ALSO EXCEPT ALL GENERALISTIC CONFIG CALLS
### PUT WARNING IN ALL MENUING RELATED TO JUMP (IN RANDOM JUMP IS ALWAYS 1?)never zero or no_chars%jump==0!!, write explanation of interplay between notches and jump
# Intern setup functions
from denigma.utils.exceptions import FileIOErrorException
from denigma.utils.types_utils import getLowerCaseName
from denigma.core import rotors
from denigma.utils.utils import simplify_rotor_dictionary_paired_unpaired, Constants
from denigma.utils.utils_cli import checkInputValidity, returningToMenu, askingInput, getSeedFromUser,checkIfFileExists,printListOfOptions, exitMenu
from denigma.utils.formatting import printOutput, printWarning, printError
import string
import os
import pickle

# from copy import copy


def _show_config_rt(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    (paired_df, unpaired, unformed, _) = (
        simplify_rotor_dictionary_paired_unpaired(
            rotor_ref._forward_dict, rotor_ref._backward_dict
        )
    )
    unpaired.extend(unformed)
    printOutput(
        "Rotor character position :",
        str(rotor_ref._conversion_in_use[rotor_ref._position]),
    )
    printOutput("Rotor character jumps:", str(rotor_ref._jump))
    notchlist = [rotor_ref._conversion_in_use[i] for i in rotor_ref._notches]
    printOutput("Rotor notches:", str(notchlist))
    printOutput("Forward connections in the rotor:\n", paired_df)
    printOutput("Bad connections (self or none) in the rotor:", str(unpaired))

    # printOutput(
    #     "Backward connections in the rotor:", str(rotor_ref._backward_dict)
    # )
    printOutput("Rotor name:", str(rotor_ref._name))
    (
        _,
        unpaired,
        unformed,
        _,
    ) = simplify_rotor_dictionary_paired_unpaired(
        rotor_ref._forward_dict, rotor_ref._backward_dict
    )
    if not unformed:
        rotor_ref.lacks_connections = False
    if len(unpaired) > 0:
        printWarning(
            "One or more connections are self-connections. This may go against proper practice"
        )
    returningToMenu()


# For now, in text, there will be no connection deletion? Or will there?
def _choose_connection_to_delete_rt(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    paired_df, _, _, _ = simplify_rotor_dictionary_paired_unpaired(
        rotor_ref._forward_dict, rotor_ref._backward_dict
    )

    if paired_df.shape[0] == 0:
        returningToMenu("There are no available connections")

    printOutput("Current connections are:\n", paired_df)
    row = askingInput("Choose a connection to delete (by index)")

    row = checkInputValidity(row, int, rangein=(0, paired_df.shape[0]))

    if row:
        # if isinstance(row, int) and row > 0 and row < paired_df.shape[0]:
        _delete_a_connection_rt(rotor_ref=rotor_ref, char1=paired_df.iloc[row][0])
        returningToMenu("Connection was deleted")
    else:
        returningToMenu("Index invalid", output_type="e")


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
    ) = simplify_rotor_dictionary_paired_unpaired(
        rotor_ref._forward_dict, rotor_ref._backward_dict
    )
    if len(front_unformed) == 0 and len(back_unformed) == 0:
        rotor_ref.lacks_connections = False
        returningToMenu(
            "There are no characters left to pair (one or fewer left unconnected)",
        )
    printOutput("Unpaired character in front side:", front_unformed)

    character1 = askingInput("Choose a character to pair from front side")
    character1 = checkInputValidity(character1, rangein=front_unformed)
    if not character1:
        # if character1 not in front_unformed:
        returningToMenu("Invalid input", output_type="e")
    printOutput("Unpaired characters in back side:", back_unformed)
    character2 = askingInput("Choose the second character from the back side")
    character2 = checkInputValidity(character2, rangein=back_unformed)
    if not character2:
        # if character2 not in back_unformed:
        returningToMenu("Invalid input", output_type="e")
    rotor_ref._forward_dict[character1] = character2
    rotor_ref._backward_dict[character2] = character1
    rotor_ref._update_dicts()
    returningToMenu("The connection was formed")
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
    # ) = denigma.simplify_rotor_dictionary_paired_unpaired(
    #     rotor_ref._forward_dict, rotor_ref._backward_dict
    # )
    # if len(front_unformed) == 0 and len(back_unformed) == 0:
    #     rotor_ref.lacks_conn = True
    #     returningToMenuMessage(
    #         "There are no characters left to pair (one or fewer left unconnected)"
    #     )
    while True:
        (
            _,
            _,
            front_unformed,
            back_unformed,
        ) = simplify_rotor_dictionary_paired_unpaired(
            rotor_ref._forward_dict, rotor_ref._backward_dict
        )
        if len(front_unformed) == 0 and len(back_unformed) == 0:
            rotor_ref.lacks_connections = False
            returningToMenu(
                "There are no characters left to pair (one or fewer left unconnected)",
            )
        printOutput("Unpaired characters in front side:", (front_unformed))
        printOutput("Unpaired characters in back side:", (back_unformed))
        printOutput(
            "If you want to stop configurating the board, just press Enter"
        )
        characters = askingInput(
            "Input one character from front side, one from back side (in order)"
        ).strip(string.whitespace)
        characters = list(characters)
        if len(characters) == 2 and all(
            character in rotor_ref.get_charlist() for character in characters
        ):
            pass
        elif not characters:
            return
        else:
            printError("Input only two allowed characters")
            continue
        characters[0] = checkInputValidity(
            characters[0], rangein=front_unformed
        )
        characters[1] = checkInputValidity(
            characters[1], rangein=back_unformed
        )
        if not all(characters):
            # if characters[0] not in front_unformed or characters[1] not in back_unformed:
            printError("One or more characters are already connected")
            continue
        # break
        rotor_ref._forward_dict[characters[0]] = characters[1]
        rotor_ref._backward_dict[characters[1]] = characters[0]
        printOutput("Connection formed")


def _form_all_connections_rt(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    _show_config_rt(rotor_ref)
    # _, unpaired_list = denigma.simplify_simple_dictionary_paired_unpaired(
    #     rotor_ref._board_dict
    # )
    _connect_all_characters_rt(rotor_ref)
    rotor_ref.lacks_connections = True
    returningToMenu(
        "You exited without forming all connections!", output_type="w"
    )

    # returningToMenuMessage(
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
    (paired_df, _, _, _) = simplify_rotor_dictionary_paired_unpaired(
        rotor_ref._forward_dict, rotor_ref._backward_dict
    )
    printOutput("Current connections are:\n", paired_df)
    character1 = askingInput("Choose a frontside connection by the index")
    character1 = checkInputValidity(
        character1, int, rangein=(0, paired_df.shape[0])
    )
    # character1 = checkInputValidity(character1, _range=rotor_ref._charlist)
    if character1==None:
        # if character1 not in rotor_ref._charlist:
        printError("Invalid input")
        return
    character2 = askingInput(
        "Choose a second frontside connection by the index to swap"
    )
    character2 = checkInputValidity(
        character2, int, rangein=(0, paired_df.shape[0])
    )
    # character2 = checkInputValidity(character2, _range=rotor_ref._charlist)
    if character2==None:
        # if character2 not in rotor_ref._charlist:
        printError("Invalid input")
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
    printOutput("The connection was swapped")


def _swap_connections_rt(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    while True:
        accbool = askingInput(
            "If you do not want to continue swapping, enter n"
        ).lower()
        if accbool == "n":
            returningToMenu()
        _swap_two_connections_rt(rotor_ref=rotor_ref)

    # returningToMenuMessage(
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
    #     accbool = askingInput("Do you still want to make changes?[y/n]").lower()
    #     if accbool == "n":
    #         returningToMenu()
    #     elif accbool == "y":
    #         break
    _connect_all_characters_rt(rotor_ref)
    rotor_ref.lacks_connections = True
    returningToMenu(
        "You exited without forming all connections!", output_type="w"
    )


def _reset_and_randomize_connections_rt(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    seed = getSeedFromUser()

    # rotor_ref._reset_dictionaries() Necessary?
    rotor_ref._randomize_dictionaries(seed)
    returningToMenu("Rotor connections established")


def _print_name_rt(rotor_ref: rotors.Rotor):
    printOutput("Current rotor name:", rotor_ref._name)


def _change_rotor_name_rt(rotor_ref: rotors.Rotor):
    _print_name_rt(rotor_ref)
    new_name = askingInput("Input a new name for the rotor")
    while not rotor_ref._is_name_valid(new_name):
        printOutput("Input only alphanumerical characters or underscores")
        new_name = askingInput("Input a new name for the rotor")
    rotor_ref._change_name(new_name)
    returningToMenu("Rotor name changed to:", rotor_ref._name)


def _randomize_name_rt(rotor_ref: rotors.Rotor):
    seed = getSeedFromUser()
    rotor_ref._random_name(seed)
    returningToMenu("Rotor name changed to:", rotor_ref._name)


def _change_notches_rt(rotor_ref: rotors.Rotor):
    printOutput("Rotor notches:", rotor_ref.get_notchlist_characters())
    positions = [
        i
        for i in askingInput(
            "Input new notches separated by a space (empty to skip)"
        ).split()
    ]
    if not positions:
        returningToMenu()
    while not rotor_ref._are_notches_invalid(positions):
        printError("Input invalid")
        positions = [
            i
            for i in askingInput(
                "Input new notches separated by a space (empty to skip)"
            ).split()
        ]
        if not positions:
            returningToMenu()

    rotor_ref._define_notches(positions)


def _randomize_notches_rt(rotor_ref: rotors.Rotor):
    seed = getSeedFromUser()
    rotor_ref._randomize_notches(seed=seed)
    printOutput("New rotor notches:", rotor_ref.get_notchlist_characters())
    returningToMenu("Rotor notches established")


def _change_position_rt(rotor_ref: rotors.Rotor):
    new_position = askingInput(
        "Input a single allowed character to set the rotor to a new position"
    )
    while rotor_ref._is_position_invalid(new_position):
        printError("Input only allowed characters")
        printOutput(rotor_ref.get_charlist())
        new_position = askingInput(
            "Input a single allowed character to set the rotor to a new position"
        )
    rotor_ref._define_position(new_position)
    returningToMenu("Rotor position set to:", rotor_ref.get_charposition())


def _randomize_position_rt(rotor_ref: rotors.Rotor):
    seed = getSeedFromUser()
    rotor_ref._randomize_position(seed)
    returningToMenu("Rotor position set to:", rotor_ref.get_charposition())


def _save_rotor_in_its_folder(rotor_ref: rotors.Rotor):
    accbool = ""
    while not accbool == "n" or not accbool == "y":
        accbool = askingInput(
            f"Would you like to save the machine in use? If not, unsaved changes will be discarded. [y/n]"
        ).lower()
    if accbool == "n":
        returningToMenu()
    new_name = rotor_ref.get_name()
    while not rotor_ref._is_name_valid(new_name):
        new_name = askingInput(
            f"Please assign a new name to the {getLowerCaseName(rotor_ref)}"
        ).strip(string.whitespace)
    rotor_ref._change_name(new_name)

    path = Constants.ROTOR_FILE_PATH
    if not os.path.exists(path):
        os.mkdir(path)
        printOutput(f"Directory '{path}' created")
    if checkIfFileExists(path, rotor_ref._name, getLowerCaseName(rotor_ref)):
        printOutput(
            f"A {getLowerCaseName(rotor_ref)} with this name already exists"
        )
        accbool = ""
        while not accbool == "n" or not accbool == "y":
            accbool = askingInput(
                f"Do you want to overwrite the saved {getLowerCaseName(rotor_ref)}? [y/n]"
            ).lower()
        if accbool == "n":
            returningToMenu(
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
    returningToMenu(
        f"{rotor_ref._name} has been saved into {rotor_ref._name}.{getLowerCaseName(rotor_ref)} in {path}"
    )


def _load_saved_rotor(rotor_id: rotors.Rotor | None = None):
    if rotor_id and rotor_id.is_set_up():
        _save_rotor_in_its_folder(rotor_ref=rotor_id)
    path = Constants.ROTOR_FILE_PATH
    if not os.path.exists(path):
        returningToMenu("There is no {} folder".format(path), output_type="e")
    list_of_files = [
        element.rsplit(".", 1)[0]
        for element in os.listdir(path)
        # if element.rsplit(".", 1)[1] == "rotor"
    ]
    if not list_of_files:
        returningToMenu(f"There are no rotors saved at {path}", "e")
    printOutput("Your available rotors are:")
    printListOfOptions(list_of_files)
    rotor_id = askingInput("Input rotor's position in the list:")
    if rotor_id=="":
        returningToMenu()
    rotor_id = checkInputValidity(
        rotor_id, int, rangein=(0, len(list_of_files))
    )
    while rotor_id==None:
        # while not isinstance(rotor, int) or rotor > len(list_of_files) - 1 or rotor < 0:
        printError("Please input a valid index")
        printListOfOptions(list_of_files)
        rotor_id = askingInput("Input rotor's position in the list:")
        if rotor_id=="":
            returningToMenu()
        rotor_id = checkInputValidity(
            rotor_id, int, rangein=(0, len(list_of_files))
        )
    try:
        filehandler = open(
            os.path.join(path, f"{list_of_files[rotor_id]}.rotor")(
                path, list_of_files[rotor_id]
            ),
            "rb",
        )
        rotor_ref = pickle.load(filehandler)
        filehandler.close()
    except Exception as e:
        returningToMenu(
            f"Failed to read the file at {filehandler}:{e}", output_type="e"
        )

    if isinstance(rotor_ref, rotors.Rotor):
        return rotor_ref
    else:
        returningToMenu(
            f"A non-rotor type was loaded:{type(rotor_ref)}", output_type="e"
        )


def _exitMenu_rt(rotor_ref: rotors.Rotor):
    # (
    #     _,
    #     _,
    #     front_unformed,
    #     _,
    # ) = denigma.simplify_rotor_dictionary_paired_unpaired(
    #     rotor_ref._forward_dict, rotor_ref._backward_dict
    # )
    if not rotor_ref.is_set_up():
        returningToMenu(
            "Due to implementation reasons, an improperly setup rotor is not allowed",
            "e",
        )
    exitMenu()

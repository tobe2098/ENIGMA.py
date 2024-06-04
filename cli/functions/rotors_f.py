## New seeds for standalone generated rotors, reflectors and boards
### EACH OBJECT SET OF MENUS TAKES THE REFERENCE FROM THE MACHINE, AND THEN OPERATES ON IT, EFFECTIVELY NOT TOUCHING THE MACHINE ITSELF BUT ITS OBJECTS
### EXCEPT FOR LOADING!!!!!! LOADING OF ITEMS HAS TO BE DONE DIRECTLY IN THE MACHINE MENU
### ALSO EXCEPT ALL GENERALISTIC CONFIG CALLS
### PUT WARNING IN ALL MENUING RELATED TO JUMP (IN RANDOM JUMP IS ALWAYS 1?)never zero or no_chars%jump==0!!, write explanation of interplay between notches and jump
# Intern setup functions
from utils.types import isDashedObject
from ...core import rotors
from ...utils import utils
from ...utils import utils_cli
import random
import os
import pickle
from copy import copy


def _show_config_rt(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    utils_cli.printOutput(
        "Rotor letter position :",
        str(rotor_ref._conversion_in_use[rotor_ref._position]),
    )
    utils_cli.printOutput("Rotor letter jumps:", str(rotor_ref._jump))
    notchlist = [rotor_ref._conversion_in_use[i] for i in rotor_ref._notches]
    utils_cli.printOutput("Rotor notches:", str(notchlist))
    utils_cli.printOutput(
        "Forward connections in the rotor:", (rotor_ref._forward_dict)
    )
    utils_cli.printOutput(
        "Backward connections in the rotor:", str(rotor_ref._backward_dict)
    )
    utils_cli.printOutput("Rotor name:", str(rotor_ref._name))
    (
        _,
        unpaired,
        _,
        _,
    ) = utils.simplify_rotor_dictionary_paired_unpaired(
        rotor_ref._forward_dict, rotor_ref._backward_dict
    )
    if len(unpaired) > 0:
        utils_cli.printOutput(
            "One or more connections are self-connections. This may go against proper practice"
        )
    utils_cli.returningToMenuNoMessage()


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
        utils_cli.returningToMenuMessage("There are no available connections")

    utils_cli.printOutput("Current connections are:")
    print(paired_df)
    row = utils_cli.askingInput("Choose a connection to delete (by index):")

    if isinstance(row, int) and row > 0 and row < paired_df.shape[0]:
        _delete_a_connection_rt(rotor_ref=rotor_ref, connIndex=row)
        utils_cli.returningToMenuMessage("Connection was deleted")
    else:
        utils_cli.returningToMenuMessage("Index invalid")


def _delete_a_connection_rt(rotor_ref: rotors.Rotor, connIndex):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
        connIndex (_type_): _description_
    """
    paired_df, _, _, _ = utils.simplify_rotor_dictionary_paired_unpaired(
        rotor_ref._forward_dict, rotor_ref._backward_dict
    )
    entry1, entry2 = paired_df.iloc[connIndex]
    # del rotor_ref._board_dict[entry] #Requires testing
    rotor_ref._forward_dict[entry1] = ""
    rotor_ref._backward_dict[entry2] = ""
    rotor_ref.lacks_conn = True
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
        rotor_ref.lacks_conn = False
        utils_cli.returningToMenuMessage(
            "There are no letters left to pair (one or fewer left unconnected)"
        )
    utils_cli.printOutput("Unpaired letters in front side:", (front_unformed))

    letter1 = utils_cli.askingInput("Choose a letter to pair from front side:").upper()
    if letter1 not in front_unformed:
        utils_cli.returningToMenuMessage("Invalid input")
    utils_cli.printOutput("Unpaired letters in back side:", (back_unformed))
    letter2 = utils_cli.askingInput(
        "Choose the second letter from the back side:"
    ).upper()
    if letter2 not in back_unformed:
        utils_cli.returningToMenuMessage("Invalid input")
    rotor_ref._forward_dict[letter1] = letter2
    rotor_ref._backward_dict[letter2] = letter1
    rotor_ref._update_dicts()
    utils_cli.returningToMenuMessage("The connection was formed")
    if len(front_unformed) - 1 == 0 and len(back_unformed) - 1 == 0:
        rotor_ref.lacks_conn = False


# First get a letter, show unconnected again, then choose to connect. If wrong choice, go back to start


def _connect_all_letters_rt(rotor_ref: rotors.Rotor):
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
    #         "There are no letters left to pair (one or fewer left unconnected)"
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
            rotor_ref.lacks_conn = False
            utils_cli.returningToMenuMessage(
                "There are no letters left to pair (one or fewer left unconnected)"
            )
        utils_cli.printOutput("Unpaired letters in front side:", (front_unformed))
        utils_cli.printOutput("Unpaired letters in back side:", (back_unformed))
        utils_cli.printOutput(
            "If you want to stop configurating the board, press Enter"
        )
        letters = (
            utils_cli.askingInput(
                "Input one letter from front side, one from back side (in order):"
            )
            .strip()
            .upper()
        )
        if letters.isalpha() and len(letters) == 2:
            pass
        elif not letters:
            return
        else:
            print("Error: Only 2 letters please")
            continue
        letters = list(letters)
        if letters[0] not in front_unformed or letters[1] not in back_unformed:
            utils_cli.printOutput("One or more letters are already connected")
            continue
        # break
        rotor_ref._forward_dict[letters[0]] = letters[1]
        rotor_ref._backward_dict[letters[1]] = letters[0]
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
    _connect_all_letters_rt(rotor_ref)
    rotor_ref.lacks_conn = True
    utils_cli.returningToMenuMessage("You exited without forming all connections!")

    # utils_cli.returningToMenuMessage(
    #     "There are no letters left to pair (one or fewer left unconnected)"
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
    _show_config_rt(rotor_ref)
    letter1 = utils_cli.askingInput(
        "Choose a frontside connection by the frontside letter to swap:"
    ).upper()
    if letter1 not in rotor_ref._characters_in_use:
        utils_cli.printOutput("Invalid input")
        return
    letter2 = utils_cli.askingInput(
        "Choose a second frontside connection by the frontside letter to swap:"
    ).upper()
    if letter2 not in rotor_ref._characters_in_use:
        utils_cli.printOutput("Invalid input")
        return
    (
        rotor_ref._backward_dict[rotor_ref._forward_dict[letter1]],
        rotor_ref._backward_dict[rotor_ref._forward_dict[letter2]],
    ) = (
        rotor_ref._backward_dict[rotor_ref._forward_dict[letter2]],
        rotor_ref._backward_dict[rotor_ref._forward_dict[letter1]],
    )
    rotor_ref._forward_dict[letter1], rotor_ref._forward_dict[letter2] = (
        rotor_ref._forward_dict[letter2],
        rotor_ref._forward_dict[letter1],
    )
    rotor_ref._update_dicts()
    utils_cli.printOutput("The connection was swapped")


def _swap_connections_rt(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    while True:
        boolean = utils_cli.askingInput(
            "If you do not want to continue swapping, enter N:"
        ).upper()
        if boolean == "N":
            utils_cli.returningToMenuMessage("Returning to menu...")
        _swap_two_connections_rt(rotor_ref=rotor_ref)

    # utils_cli.returningToMenuMessage(
    #     "There are no letters left to pair (one or fewer left unconnected)."
    # )


def _reset_and_streamline_connections_by_pairs_rt(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    _reset_connections_rt(rotor_ref)
    # while True:
    #     accbool = utils_cli.utils_cli.askingInput("Do you still want to make changes?[y/n]").lower()
    #     if accbool == "n":
    #         utils_cli.returningToMenuNoMessage()
    #     elif accbool == "y":
    #         break
    _connect_all_letters_rt(rotor_ref)
    utils_cli.returningToMenuMessage("You exited without forming all connections!")


def _reset_and_randomize_connections_rt(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    seed = utils_cli.getSeedFromUser()

    # rotor_ref._reset_dictionaries() Necessary?
    rotor_ref._randomize_dictionaries(seed)
    utils_cli.returningToMenuMessage("Rotor connections established")


def _reset_connections_rt(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    rotor_ref._reset_dictionaries()
    rotor_ref.lacks_conn = True


def _print_name_rt(rotor_ref: rotors.Rotor):
    utils_cli.printOutput("Current rotor name:", rotor_ref._name)


def _change_rotor_name_rt(rotor_ref: rotors.Rotor):
    _print_name_rt(rotor_ref)
    new_name = utils_cli.askingInput("Input a new name for the rotor:")
    while not rotor_ref._is_name_valid(new_name):
        utils_cli.printOutput("Input only alphanumerical characters or underscore")
        new_name = utils_cli.askingInput("Input a new name for the rotor:")
    rotor_ref._change_name(new_name)
    utils_cli.returningToMenuMessage("Rotor name changed to:", rotor_ref._name)


def _randomize_name_rt(rotor_ref: rotors.Rotor):
    seed = utils_cli.getSeedFromUser()
    rotor_ref._random_name(seed)
    utils_cli.returningToMenuMessage("Rotor name changed to:", rotor_ref._name)


def _change_notches_rt(rotor_ref: rotors.Rotor):
    utils_cli.printOutput("Rotor notches:", rotor_ref.get_notchlist_letters())
    positions = [
        i
        for i in utils_cli.askingInput(
            "Input new notches separated by a space (empty to skip):"
        ).split()
    ]
    if not positions:
        utils_cli.returningToMenuNoMessage()
    while not rotor_ref._are_notches_valid(positions):
        positions = [
            i
            for i in utils_cli.askingInput(
                "Input new notches separated by a space (empty to skip):"
            ).split()
        ]
        if not positions:
            utils_cli.returningToMenuNoMessage()

    rotor_ref._define_notches(positions)


def _randomize_notches_rt(rotor_ref: rotors.Rotor):
    seed = utils_cli.getSeedFromUser()
    random.seed(seed)
    positions = [
        i
        for i in set(
            random.sample(range(0, rotor_ref._no_characters), random.randint(1, 5))
        )
    ]
    rotor_ref._define_notches(positions)
    utils_cli.printOutput("New rotor notches:", rotor_ref.get_notchlist_letters())
    utils_cli.returningToMenuMessage("Rotor notches established")


def _change_position_rt(rotor_ref: rotors.Rotor):
    new_position = utils_cli.askingInput(
        "Input a single letter to set the rotor to a new position:"
    ).upper()
    while rotor_ref._is_position_invalid(new_position):
        if isDashedObject(rotor_ref):
            utils_cli.printOutput("Input only a single letter")
        else:
            utils_cli.printOutput("Input only a single letter or a dash")
        new_position = utils_cli.askingInput(
            "Input a single letter to set the rotor to a new position:"
        ).upper()
    rotor_ref._define_position(new_position)
    utils_cli.returningToMenuMessage("Rotor position set to:", rotor_ref.get_position())


def _randomize_position_rt(rotor_ref: rotors.Rotor, seed: int):
    seed = utils_cli.getSeedFromUser()
    random.seed(seed)
    new_position = random.sample(range(0, rotor_ref._characters_in_use), 1)
    rotor_ref._define_position(new_position)
    utils_cli.returningToMenuMessage("Rotor position set to:", rotor_ref.get_position())


def _save_in_current_directory_rt(rotor_ref: rotors.Rotor):
    new_name = ""
    while not rotor_ref._is_name_valid(rotor_ref.get_name()):
        new_name = utils_cli.askingInput(
            "Please assign a new name to the rotor:"
        ).strip()
    rotor_ref._change_name(new_name)

    current_path = os.getcwd()
    new_folder = utils.ROTORS_FILE_HANDLE
    path = os.path.join(current_path, new_folder)
    if not os.path.exists(path):
        os.mkdir(path)
        utils_cli.printOutput("Directory '% s' created" % path)
    if utils_cli.checkIfFileExists(path, rotor_ref._name, "rotor"):
        utils_cli.printOutput("A rotor with this name already exists")
        accbool = ""
        while not accbool == "n" or not accbool == "y":
            accbool = input(
                utils_cli.askingInput("Do you want to overwrite the saved rotor? [y/n]")
            ).lower()
        if accbool == "n":
            utils_cli.returningToMenuNoMessage()
    save_file = open(r"{}\\{}.rotor".format(path, rotor_ref._name), "wb")
    pickle.dump(rotor_ref, save_file)
    utils_cli.returningToMenuMessage(
        (
            "{} has been saved into {}.rotor in {}".format(
                rotor_ref._name, rotor_ref._name, path
            )
        )
    )


def _load_saved_rotor():
    current_path = os.path.dirname(__file__)
    new_folder = utils.ROTORS_FILE_HANDLE
    path = os.path.join(current_path, new_folder)
    if not os.path.exists(path):
        utils_cli.returningToMenuMessage("There is no {} folder".format(path))
    list_of_files = [element.rsplit((".", 1)[0])[0] for element in os.listdir(path)]
    if len(list_of_files) == 0:
        utils_cli.returningToMenuMessage("There are no rotors saved")
    utils_cli.printOutput("Your available rotors are:")
    utils_cli.printListOfOptions(list_of_files)
    rotor = utils_cli.askingInput("Input reflector's position in the list:")
    while not isinstance(rotor, int) or rotor > len(list_of_files) - 1 or rotor < 0:
        utils_cli.printOutput("Please input a valid index")
        rotor = utils_cli.askingInput("Input reflector's position in the list:")
    filehandler = open(r"{}\\{}.reflector".format(path, list_of_files[rotor]), "rb")
    return pickle.load(filehandler)


def _exitMenu_rt(rotor_ref: rotors.Rotor):
    # (
    #     _,
    #     _,
    #     front_unformed,
    #     _,
    # ) = utils.simplify_rotor_dictionary_paired_unpaired(
    #     rotor_ref._forward_dict, rotor_ref._backward_dict
    # )
    if rotor_ref.lacks_conn:
        utils_cli.returningToMenuMessage(
            "Due to implementation reasons, a partially connected rotor is not allowed"
        )
    utils_cli.exitMenu()

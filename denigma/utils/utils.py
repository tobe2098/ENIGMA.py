"""Module that provides global functions and constants"""

import pandas as pd
import string
import os
import json


def create_dictionary_from_charlist(charlist: list):
    nums = list(range(len(charlist)))
    equivalence_dictionary = dict(zip(charlist, nums))
    equivalence_dictionary.update(
        dict([reversed(i) for i in equivalence_dictionary.items()])
    )
    return equivalence_dictionary


class Constants:
    FILESAFE_CHARS = string.ascii_letters + string.digits + "-_"
    MAX_NO_ROTORS = 1000
    MAX_SEED = 2**2**10
    MAX_NO_BACKSPACES = 1000
    UPP_LETTERS = list(string.ascii_uppercase)
    UPP_LETTERS_key = "ABC"
    UPP_LETTERS_dash = list(string.ascii_uppercase + "-")
    UPP_LETTERS_dash_key = "ABC-"
    ALL_LETTERS = list(string.ascii_letters)
    ALL_LETTERS_key = "AaBbCc"
    ALL_LETTERS_dash = list(string.ascii_letters + "-")
    ALL_LETTERS_dash_key = "AaBbCc-"
    ALPHANUM_dash = list(string.ascii_letters + string.digits + "-")
    ALPHANUM_dash_key = "AaBbCc123-"
    ALPHANUM = list(string.ascii_letters + string.digits + "-")
    ALPHANUM_key = "AaBbCc123-"
    # NUMBERS = list(range(0, len(UPP_LETTERS)))
    # NUMBERS_dash = list(range(0, len(UPP_LETTERS_dash)))
    # EQUIVALENCE_DICT = dict(zip(UPP_LETTERS, NUMBERS))
    # # EQUIVALENCE_DICT[""] = -1  # To manage non-existant connections
    # EQUIVALENCE_DICT.update(dict([reversed(i) for i in EQUIVALENCE_DICT.items()]))
    # EQUIVALENCE_DICT_dash = dict(zip(UPP_LETTERS_dash, NUMBERS_dash))
    # # EQUIVALENCE_DICT_dash[""] = -1  # To manage non-existant connections
    # EQUIVALENCE_DICT_dash.update(
    #     dict([reversed(i) for i in EQUIVALENCE_DICT_dash.items()])
    # )
    ROTORS_FILE_HANDLE = "SAVED_ROTORS"
    REFLECTORS_FILE_HANDLE = "SAVED_REFLECTORS"
    MACHINES_FILE_HANDLE = "SAVED_MACHINES"
    CHARLISTS_HANDLE = "charlists.json"
    CONFIG_HANDLE = "config.json"
    MODULE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ROTOR_FILE_PATH = os.path.join(MODULE_PATH, ROTORS_FILE_HANDLE)
    REFLECTOR_FILE_PATH = os.path.join(MODULE_PATH, REFLECTORS_FILE_HANDLE)
    MACHINE_FILE_PATH = os.path.join(MODULE_PATH, MACHINES_FILE_HANDLE)
    CHARLISTS_FILE_PATH = os.path.join(MODULE_PATH, CHARLISTS_HANDLE)
    CONFIG_FILE_PATH = os.path.join(MODULE_PATH, CONFIG_HANDLE)
    VERSION = "0.1.0"
    SCREEN_CLEAR_CONVENIENCE = True
    SCREEN_CLEAR_SAFETY = True
    is_cli_mode = False
    is_gui_mode = False


def get_is_cli_mode():
    return Constants.is_cli_mode


def get_is_gui_mode():
    return Constants.is_gui_mode


def my_quit_fn():  # This function should be in denigma.utils.py
    raise SystemExit


def simplify_simple_dictionary_paired_unpaired(board_dict):
    """
    The function simplifies the board dictionary such that there is only one copy of each character in the output

    board_dict (dict): board dictionary
    """
    seen_pairs = []
    pairs = []
    unpaired_list = []
    # all_characters=[i for i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
    for character_a, character_b in board_dict.items():
        if character_a in seen_pairs or character_b in seen_pairs:
            continue
        if character_b == character_a:
            unpaired_list.append(character_a)
            continue
        pairs.append([character_a, character_b])
        seen_pairs.append(character_a)
        seen_pairs.append(character_b)
    paired_df = pd.DataFrame(pairs, columns=["Letter A", "Letter B"])
    # board_dict_simpl["Unpaired"]=unpaired
    return paired_df, unpaired_list


def simplify_rotor_dictionary_paired_unpaired(forward_dict, backward_dict):
    """
    The function simplifies the board dictionary such that there is only one copy of each character in the output

    board_dict (dict): board dictionary
    """
    seen = []
    seenb = []
    pairs = []
    unpaired_list = []
    unformed = []
    back_unformed = []
    # all_characters=[i for i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
    for character_a, character_b in forward_dict.items():
        if character_a in seen:
            continue
        elif character_b == character_a:
            unpaired_list.append(character_a)
            pairs.append([character_a, character_a])

        elif character_b == "":
            unformed.append(character_a)

        else:
            pairs.append([character_a, character_b])
        seen.append(character_a)
        seenb.append(character_b)
    for character_a, character_b in backward_dict.items():
        if character_a in seenb:
            continue
        elif character_b == character_a:
            continue
        elif character_b == "":
            back_unformed.append(character_a)
        seenb.append(character_a)
        # seen.append(character_b)
    paired_df = pd.DataFrame(pairs, columns=["Letter A", "Letter B"])
    # board_dict_simpl["Unpaired"]=unpaired
    return paired_df, unpaired_list, unformed, back_unformed


def transform_single_dict(dictionary, conversion: dict):
    """
    The function gets a character or number dictionary and returns the other one

    dictionary (dict): dictionary to swap
    """

    return {conversion[key]: conversion[value] for key, value in dictionary.items()}


def is_valid_seed(seed):
    return isinstance(seed, int) and seed >= 0 and seed < Constants.MAX_SEED


def is_valid_filename(filename):
    return all(i in Constants.FILESAFE_CHARS for i in filename) and filename


# def transform_single_dict_dash(dictionary):
#     """
#     The function gets a character or number (containing dash) dictionary and returns the other one


#     dictionary (dict): dictionary to swap
#     """
#     return {
#         EQUIVALENCE_DICT_dash[key]: EQUIVALENCE_DICT_dash[value]
#         for key, value in dictionary.items()
#     }


def _asign_defaults_to_charlist_json(dictionary: dict):
    dictionary[Constants.UPP_LETTERS_key] = Constants.UPP_LETTERS
    dictionary[Constants.UPP_LETTERS_dash_key] = Constants.UPP_LETTERS_dash
    dictionary[Constants.ALL_LETTERS_key] = Constants.ALL_LETTERS
    dictionary[Constants.ALL_LETTERS_dash_key] = Constants.ALL_LETTERS_dash
    dictionary[Constants.ALPHANUM_key] = Constants.ALPHANUM
    dictionary[Constants.ALPHANUM_dash_key] = Constants.ALPHANUM_dash


def get_charlist_json():
    dictionary = {}
    if os.path.isfile(Constants.CHARLISTS_FILE_PATH):
        with open(Constants.CHARLISTS_FILE_PATH) as file:
            dictionary = json.load(file)
        _asign_defaults_to_charlist_json(dictionary=dictionary)
    else:
        _asign_defaults_to_charlist_json(dictionary=dictionary)
        with open(Constants.CHARLISTS_FILE_PATH, "w") as file:
            json.dump(dictionary, file, indent=2)
    return dictionary


def save_charlist_json(dictionary: dict = None):
    if not os.path.isfile(Constants.CHARLISTS_FILE_PATH) and not dictionary:
        dictionary = {}
        _asign_defaults_to_charlist_json(dictionary=dictionary)

    with open(Constants.CHARLISTS_FILE_PATH, "w") as file:
        json.dump(dictionary, file, indent=2)


def _asign_defaults_to_config_json(dictionary: dict):
    dictionary["is_machine_set"] = False
    dictionary["set_machine"] = None


def get_config_json():
    dictionary = {}
    if os.path.isfile(Constants.CONFIG_FILE_PATH):
        with open(Constants.CONFIG_FILE_PATH) as file:
            dictionary = json.load(file)
    else:
        _asign_defaults_to_config_json(dictionary=dictionary)
        with open(Constants.CONFIG_FILE_PATH, "w") as file:
            json.dump(dictionary, file, indent=2)
    return dictionary


def save_config_json(dictionary: dict = None):
    if not os.path.isfile(Constants.CONFIG_FILE_PATH) and not dictionary:
        dictionary = {}
        _asign_defaults_to_charlist_json(dictionary=dictionary)

    with open(Constants.CONFIG_FILE_PATH, "w") as file:
        json.dump(dictionary, file, indent=2)

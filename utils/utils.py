"""Module that provides global functions and constants"""

import pandas as pd


class Constants:
    MAX_NO_ROTORS = 100
    MAX_SEED = 2**2**10
    MAX_NO_BACKSPACES = 1000
    CHARACTERS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    CHARACTERS_dash = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ-")
    NUMBERS = list(range(0, len(CHARACTERS)))
    NUMBERS_dash = list(range(0, len(CHARACTERS_dash)))
    EQUIVALENCE_DICT = dict(zip(CHARACTERS, NUMBERS))
    # EQUIVALENCE_DICT[""] = -1  # To manage non-existant connections
    EQUIVALENCE_DICT.update(dict([reversed(i) for i in EQUIVALENCE_DICT.items()]))
    EQUIVALENCE_DICT_dash = dict(zip(CHARACTERS_dash, NUMBERS_dash))
    # EQUIVALENCE_DICT_dash[""] = -1  # To manage non-existant connections
    EQUIVALENCE_DICT_dash.update(
        dict([reversed(i) for i in EQUIVALENCE_DICT_dash.items()])
    )
    ROTORS_FILE_HANDLE = "SAVED_ROTORS"
    REFLECTORS_FILE_HANDLE = "SAVED_REFLECTORS"
    MACHINES_FILE_HANDLE = "SAVED_MACHINES"


def my_quit_fn():  # This function should be in utils.py
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


# def transform_single_dict_dash(dictionary):
#     """
#     The function gets a character or number (containing dash) dictionary and returns the other one


#     dictionary (dict): dictionary to swap
#     """
#     return {
#         EQUIVALENCE_DICT_dash[key]: EQUIVALENCE_DICT_dash[value]
#         for key, value in dictionary.items()
#     }


def areUsingSameDicts(obj1, obj2):
    return obj1._conversion_in_use == obj2._conversion_in_use


def get_character_list(obj):
    return obj._characters_in_use

"""Module that provides global functions and constants"""
import pandas as pd


MAX_NO_ROTORS = 100

CHARACTERS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
CHARACTERS_dash = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ-")

NUMBERS = list(range(0, len(CHARACTERS)))
NUMBERS_dash = list(range(0, len(CHARACTERS_dash)))

EQUIVALENCE_DICT = dict(zip(CHARACTERS, NUMBERS))
EQUIVALENCE_DICT.update(dict([reversed(i) for i in EQUIVALENCE_DICT.items()]))

EQUIVALENCE_DICT_dash = dict(zip(CHARACTERS_dash, NUMBERS_dash))
EQUIVALENCE_DICT_dash.update(dict([reversed(i) for i in EQUIVALENCE_DICT_dash.items()]))

# def gen_rnd_26list(seed=None): #Deprecated, random.sample(range(1,27), n) does exactly the same
#     '''
#     The function generates a random list from 1 to 26 (incl.)

#     seed (int): seed for randomization purposes
#     '''
#     if not seed:
#         print("Problem in gen_rnd_26list()'s call")
#     random.seed(seed)
#     poplist=[i+1 for i in range (0,26)]
#     random.shuffle(poplist)
#     return poplist


def simplify_board_dict(board_dict):
    """
    The function simplifies the board dictionary such that there is only one copy of each letter in the output

    board_dict (dict): board dictionary
    """
    seen_pairs = []
    pairs = []
    # all_letters=[i for i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
    for letter_a, letter_b in board_dict.items():
        if letter_a in seen_pairs or letter_b in seen_pairs:
            continue
        if letter_b == letter_a:
            continue
        pairs.append([letter_a, letter_b])
        seen_pairs.append(letter_a)
        seen_pairs.append(letter_b)
    # unpaired=list(set(all_letters)-set(seen_pairs)) #Deprecated for conflict reasons
    board_dict_simpl = pd.DataFrame(pairs, columns=["Letter A", "Letter B"])
    # board_dict_simpl["Unpaired"]=unpaired
    return board_dict_simpl


def transform_single_dict(dictionary, conversion: dict):
    """
    The function gets a letter or number dictionary and returns the other one

    dictionary (dict): dictionary to swap
    """

    return {conversion[key]: conversion[value] for key, value in dictionary.items()}


# def transform_single_dict_dash(dictionary):
#     """
#     The function gets a letter or number (containing dash) dictionary and returns the other one

#     dictionary (dict): dictionary to swap
#     """
#     return {
#         EQUIVALENCE_DICT_dash[key]: EQUIVALENCE_DICT_dash[value]
#         for key, value in dictionary.items()
#     }

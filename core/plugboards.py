import copy
import random

from client.menus.utils_m import stringOutput
from .utils import (
    CHARACTERS,
    CHARACTERS_dash,
    EQUIVALENCE_DICT,
    EQUIVALENCE_DICT_dash,
    transform_single_dict,
    simplify_dictionary_paired_unpaired,
)


class PlugBoard:
    def __init__(self, characters=CHARACTERS, conversion=EQUIVALENCE_DICT) -> None:
        self._characters_in_use = copy.copy(characters)
        self._conversion_in_use = copy.copy(conversion)
        self._board_dict = dict(
            zip(copy.copy(self._characters_in_use), copy.copy(self._characters_in_use))
        )
        self._update_dicts()

    def _update_dicts(self, letter_to_num=True):
        if letter_to_num:
            self._board_num_dict = transform_single_dict(
                self._board_dict, self._conversion_in_use
            )
        else:
            self._board_dict = transform_single_dict(
                self._board_num_dict, self._conversion_in_use
            )

    def _reset_dictionaries(self):
        self._board_dict = dict(
            zip(copy.copy(self._characters_in_use), copy.copy(self._characters_in_use))
        )
        self._update_dicts()

    def _show_config(self):
        paired_df, unpaired_list = simplify_dictionary_paired_unpaired(self.board_dict)
        print(stringOutput("Paired letters: "), paired_df)
        print(stringOutput("Unpaired letters: "), unpaired_list)

    def _input_output(self, number_io):
        return self._board_num_dict[number_io]

    def random_setup(self, seed=None):
        if not seed:
            print(stringOutput("Please input a seed."))
            return
        random.seed(seed)

        # Now set the connections
        ### !!! Make sure board is composed of pairs and is symmetrical!!! It is not as of now.
        num_list = list(range(0, len(self._characters_in_use)))
        random.shuffle(num_list)
        cable_num = random.randint(0, int(len(self._characters_in_use) / 2))
        while cable_num > 0 and len(num_list) > 1:
            letterA = num_list.pop()
            letterB = num_list.pop()
            self._board_num_dict[letterA] = letterB
            self._board_num_dict[letterB] = letterA
            cable_num -= 1

        self._update_dicts(False)
        # Show final configuration
        # print(">>>Board config:\n", simplify_board_dict(self.board_dict))
        print(stringOutput("Board setup is generated."))


class PlugBoardDash(PlugBoard):
    """_summary_

    Args:
        PlugBoard (_type_): _description_
    """

    def __init__(self) -> None:
        super().__init__(CHARACTERS_dash, EQUIVALENCE_DICT_dash)

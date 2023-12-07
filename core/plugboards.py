import copy
import random
from .utils import (
    CHARACTERS,
    CHARACTERS_dash,
    EQUIVALENCE_DICT,
    EQUIVALENCE_DICT_dash,
    transform_single_dict,
    simplify_board_dict,
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

    def show_config(self):
        paired_df, unpaired_list = simplify_board_dict(self.board_dict)
        print("Paired letters:", paired_df)
        print("Unpaired letters:", unpaired_list)

    def input_output(self, number_io):
        return self._board_num_dict[number_io]

    def randomize_board_dict(self, seed=None):
        if not seed:
            print(">Please input a seed")
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

        self._update_dicts(False)
        # Show final configuration
        # print(">>>Board config:\n", simplify_board_dict(self.board_dict))
        print(">Board setup is generated")


class PlugBoardDash(PlugBoard):
    """_summary_

    Args:
        PlugBoard (_type_): _description_
    """

    def __init__(self) -> None:
        super().__init__(CHARACTERS_dash, EQUIVALENCE_DICT_dash)

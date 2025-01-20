import copy
import random

from denigma.core.abstract import AbstractBaseClass
from denigma.utils.exceptions import raiseBadInputException

from denigma.utils.utils import (
    Constants,
    create_dictionary_from_charlist,
    is_valid_seed,
    transform_single_dict,
)


class PlugBoard(AbstractBaseClass):
    def __init__(self, characters=Constants.UPP_LETTERS) -> None:
        super().__init__(charlist=characters)
        self._conversion_in_use = create_dictionary_from_charlist(characters)
        self._board_dict = dict(
            zip(copy.copy(self._charlist), copy.copy(self._charlist))
        )
        self._update_dicts()

    def _update_dicts(self, character_to_num=True):
        if character_to_num:
            self._board_num_dict = transform_single_dict(
                self._board_dict, self._conversion_in_use
            )
        else:
            self._board_dict = transform_single_dict(
                self._board_num_dict, self._conversion_in_use
            )

    def _reset_dictionaries(self):
        self._board_dict = dict(
            zip(copy.copy(self._charlist), copy.copy(self._charlist))
        )
        self._update_dicts()

    def _input_output(self, number_io):
        return self._board_num_dict[number_io]

    def random_setup(self, seed=None):

        if not is_valid_seed(seed):
            raiseBadInputException(seed)
        random.seed(seed)

        # Now set the connections
        ### !!! Make sure board is composed of pairs and is symmetrical!!! It is not as of now.
        num_list = list(range(0, len(self._charlist)))
        random.shuffle(num_list)
        cable_num = random.randint(0, int(len(self._charlist) / 2))
        while cable_num > 0 and len(num_list) > 1:
            characterA = num_list.pop()
            characterB = num_list.pop()
            self._board_num_dict[characterA] = characterB
            self._board_num_dict[characterB] = characterA
            cable_num -= 1

        self._update_dicts(False)
        # Show final configuration
        # print(">>>Board config:\n", simplify_board_dict(self.board_dict))

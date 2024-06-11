import random

# import pickle
# import os
import copy

from ..utils.utils import (
    transform_single_dict,
    Constants,
    is_valid_seed,
)
from ..utils.exceptions import raiseBadInputException


class Rotor:
    def __init__(
        self, characters=Constants.CHARACTERS, conversion=Constants.EQUIVALENCE_DICT
    ):
        # Note: variables can be defined on the fly

        self._name = "name"  # randomly generating a name is going to happen I guess

        self._position = 0  # Can go from 1 to _no_characters
        self.jump = 1  # Jump between positions. Can be changed for extra randomness, but carefully, never zero or 26
        # #Jump implementation will be done last. It can get complicated. Possible future feature
        self._characters_in_use = copy.copy(characters)
        self._conversion_in_use = copy.copy(conversion)
        self._no_characters = len(characters)
        self._notches = [
            self._no_characters - 1
        ]  # self.notch can be a list. When does the next rotor move relative to the notch?
        self._forward_dict = dict(zip(self._characters_in_use, self._characters_in_use))

        self._backward_dict = dict(
            zip(self._characters_in_use, self._characters_in_use)
        )
        self.lacks_conn = False
        self._update_dicts()

    def get_name(self):
        return self._name

    def get_position(self):
        return self._conversion_in_use[self._position]

    def get_notchlist_letters(self):
        return [self._conversion_in_use[i] for i in self._notches]

    def notch_check_move_forward(self):
        if any(
            (notch - self._position) % self._no_characters < self._jump
            for notch in self._notches
        ):  # This was double-checked
            self._position += self._jump
            self._position %= self._no_characters
            return True
        else:
            self._position += self._jump
            self._position %= self._no_characters
            return False

    def backspace(self):
        self._position -= self._jump
        self._position %= self._no_characters
        return any(
            (self._position - notch) % self._no_characters < self._jump
            for notch in self._notches
        )  # This was double-checked

    def forward_pass(self, input_letter_number):
        input_letter_number += self._position
        input_letter_number %= self._no_characters
        output_number = self._forward_num_dict[input_letter_number]
        output_number -= self._position
        output_number %= self._no_characters
        return output_number

    def backward_pass(self, input_letter_number):
        input_letter_number += self._position
        input_letter_number %= self._no_characters
        output_number = self._backward_num_dict[input_letter_number]
        output_number -= self._position
        output_number %= self._no_characters
        return output_number

    def _is_name_valid(self, name):
        return (
            name != "name" and name != "" and all(c.isalnum() or c == "_" for c in name)
        )

    def _change_name(self, new_name):
        """_summary_

        Args:
            new_name (_type_): _description_

        Raises:
            Exception: _description_
        """

        new_name = new_name.strip()
        if not self._is_name_valid(new_name):
            raiseBadInputException()
        self._name = new_name
        # print(">Now name of the reflector is:", self._name)

    def _is_jump_invalid(self, jump):
        return self._characters_in_use % jump == 0

    def _define_rotor_jump(self, jump):
        """Not active for now

        Args:
            jump (int): number of jumps
        """
        if self._is_jump_invalid(jump):
            raiseBadInputException()
        self._jump = jump
        # print(
        #     ">Now rotor jumps ",
        #     jump,
        #     " spaces for every input (not yet implemented in the machine)",
        # )

    # Do dictionaries of str(numbers) to the new number (or the number of the new letter), and do 1 for each direction

    def _is_position_invalid(self, position):
        return len(position) > 1 or position not in self._characters_in_use

    def _define_position(self, position):
        """Sets the position of the rotor to the input value

        Args:
            position (string): A single character to set the position to
        """
        ##DEBUG
        if self._is_position_invalid(position):
            raiseBadInputException()

        self._position = self._conversion_in_use[position]
        # print(
        #     ">Now rotor is in letter position {}".format(
        #         self._conversion_in_use[self._position]
        #     )
        # )

    def _are_notches_valid(self, notches):
        return (
            not notches
            or any(not i.isalpha() for i in notches)
            or any(len(i) > 1 for i in notches)
            or any(i in self._characters_in_use for i in notches)
            or len(notches) >= self._no_characters
        )

    def _define_notches(self, positions):
        """Sets the notches of the rotor to the input list of single characters

        Args:
            positions (list): list of single characters
        """
        ##DEBUG
        if self._are_notches_valid(positions):
            raiseBadInputException()

        notch_list = [
            self._conversion_in_use[notch]
            for notch in positions
            if notch in self._characters_in_use and notch != ""
        ]
        self._notches = notch_list
        # print(
        #     ">Now the rotor has {} notches in positions {}".format(
        #         len(notch_list), position
        #     )
        # )

    def _update_dicts(self, letter_to_num=True):
        if letter_to_num:
            self._forward_num_dict = transform_single_dict(
                self._forward_dict, self._conversion_in_use
            )
            self._backward_num_dict = transform_single_dict(
                self._backward_dict, self._conversion_in_use
            )
        else:
            self._forward_dict = transform_single_dict(
                self._forward_num_dict, self._conversion_in_use
            )
            self._backward_dict = transform_single_dict(
                self._backward_num_dict, self._conversion_in_use
            )

    def _reset_dictionaries(self):
        empty_list = ["" for _ in range(self._no_characters)]
        self._forward_dict = zip(self._characters_in_use, empty_list)
        self._backward_dict = zip(self._characters_in_use, empty_list)
        self._update_dicts()

    def _random_name(self, seed=None):
        if not is_valid_seed(seed):
            raiseBadInputException()
        random.seed(seed)
        # Name generation
        name_list = [
            random.sample(range(0, self._no_characters), 1)[0] for _ in range(0, 13)
        ]
        name_list[0:9] = [self._conversion_in_use[num] for num in name_list[0:9]]
        name_list[9:13] = [str(i % 10) for i in name_list[9:13]]
        string1 = ""
        name = string1.join(name_list)
        self._change_name(name)

    def _randomize_dictionaries(self, seed=None):

        # Once the seed is set, as long as the same operations are performed the same numbers are generated:
        if not is_valid_seed(seed):
            raiseBadInputException()
        random.seed(seed)
        num_list = list(range(0, self._no_characters))
        self._forward_num_dict = dict(
            zip(
                num_list,
                random.sample(range(0, self._no_characters), self._no_characters),
            )
        )
        sorted_dict = dict(sorted(self._forward_num_dict.items(), key=lambda x: x[1]))
        self._backward_num_dict = dict(zip(sorted_dict.values(), sorted_dict.keys()))
        self._update_dicts(False)


class RotorDash(Rotor):
    def __init__(self):
        super().__init__(Constants.CHARACTERS_dash, Constants.EQUIVALENCE_DICT_dash)

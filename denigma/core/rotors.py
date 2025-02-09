import random
import string

from denigma.core.abstract import AbstractBaseClass

from denigma.utils.utils import (
    create_dictionary_from_charlist,
    transform_single_dict,
    Constants,
    is_valid_seed,
    simplify_rotor_dictionary_paired_unpaired
)
from denigma.utils.exceptions import raiseBadInputException


class Rotor(AbstractBaseClass):
    def __init__(self, characters=Constants.UPP_LETTERS):
        # Note: variables can be defined on the fly
        super().__init__(charlist=characters)

        self._position = 0  # Can go from 1 to _no_characters
        self._jump = 1  # Jump between positions. Can be changed for extra randomness, but carefully, never zero or 26
        # #Jump implementation will be done last. It can get complicated. Possible future feature
        self._conversion_in_use = create_dictionary_from_charlist(characters)
        self._no_characters = len(characters)
        self._notches = [
            self._no_characters - 1
        ]  # self.notch can be a list. When does the next rotor move relative to the notch?
        self._forward_dict = dict(zip(self._charlist, self._charlist))

        self._backward_dict = dict(
            zip(self._charlist, self._charlist)
        )
        self.lacks_connections = True
        self._update_dicts()


    def get_charposition(self):
        return self._conversion_in_use[self._position]

    def get_notchlist_characters(self):
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

    def forward_pass(self, input_character_number):
        input_character_number += self._position
        input_character_number %= self._no_characters
        output_number = self._forward_num_dict[input_character_number]
        output_number -= self._position
        output_number %= self._no_characters
        return output_number

    def backward_pass(self, input_character_number):
        input_character_number += self._position
        input_character_number %= self._no_characters
        output_number = self._backward_num_dict[input_character_number]
        output_number -= self._position
        output_number %= self._no_characters
        return output_number
        # print(">Now name of the reflector is:", self._name)

    def _is_jump_invalid(self, jump):
        return jump == 0 or self._no_characters % jump == 0 and jump != 1

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

    # Do dictionaries of str(numbers) to the new number (or the number of the new character), and do 1 for each direction

    def _is_position_invalid(self, position):
        return (type(position)==str and len(position) > 1) or (type(position)==int and position not in range(self._no_characters))

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
        #     ">Now rotor is in character position {}".format(
        #         self._conversion_in_use[self._position]
        #     )
        # )

    def _are_notches_invalid(self, notches):
        return (
            not notches
            or (all(type(i)==str for i in notches) and (any(len(i)>1 for i in notches)))
            or (all (type(i)==int for i in notches) and any(i not in range(self._no_characters) for i in notches))
            or len(notches) >= self._no_characters
        )

    def _define_notches(self, positions):
        """Sets the notches of the rotor to the input list of single characters

        Args:
            positions (list): list of single characters
        """
        ##DEBUG
        if self._are_notches_invalid(positions):
            raiseBadInputException(positions)

        notch_list = [
            self._conversion_in_use[notch]
            for notch in positions
            if notch in self._charlist and notch != ""
        ]
        notch_list=list(set(notch_list))
        self._notches = notch_list
        # print(
        #     ">Now the rotor has {} notches in positions {}".format(
        #         len(notch_list), position
        #     )
        # )

    def _update_dicts(self, character_to_num=True):
        if character_to_num:
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
        self._forward_dict = zip(self._charlist, empty_list)
        self._backward_dict = zip(self._charlist, empty_list)
        self._update_dicts()

    def _random_name(self, seed=None):
        if not is_valid_seed(seed):
            raiseBadInputException()
        random.seed(seed)
        # Name generation
        name=""
        for _ in range(13):
            name+=random.sample(Constants.FILESAFE_CHARS, 1)[0]
        self._change_name(name)

    def _randomize_position(self, seed=None):
        if not is_valid_seed(seed):
            raiseBadInputException()
        random.seed(seed)
        self._define_position(random.sample(self._charlist, 1)[0])

    def _randomize_notches(self, seed=None):
        if not is_valid_seed(seed):
            raiseBadInputException()
        random.seed(seed)
        no_notches = random.randint(1, self._no_characters - 1)
        notchlist = random.sample(self._charlist, no_notches)
        self._define_notches(notchlist)

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

    def is_set_up(self):
        # (_, unpaired, unformed, _) = simplify_rotor_dictionary_paired_unpaired(
        #     self._forward_dict, self._backward_dict
        # )
        # unpaired.extend(unformed)
        (
        _,
        unpaired,
        unformed,
        _,
        ) = simplify_rotor_dictionary_paired_unpaired(
            self._forward_dict, self._backward_dict
        )
        self.lacks_connections=(len(unformed)!=0)
        return not (
            self.lacks_connections
            or self._are_notches_invalid(self._notches)
            or self._is_jump_invalid(self._jump)
            or self._is_position_invalid(self._position)
        )

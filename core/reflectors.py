"""This module contains the rotor classes"""
import random
import copy

from ..utils.utils import (
    CHARACTERS,
    CHARACTERS_dash,
    EQUIVALENCE_DICT,
    EQUIVALENCE_DICT_dash,
    transform_single_dict,
)


class Reflector:
    def __init__(self, characters=CHARACTERS, conversion=EQUIVALENCE_DICT):
        self._name = "name"
        self._characters_in_use = copy.copy(characters)
        self._conversion_in_use = copy.copy(conversion)
        self._reflector_dict = dict(
            zip(copy.copy(self._characters_in_use), copy.copy(self._characters_in_use))
        )
        self._reflector_num_dict = {}
        self._update_dicts()

    def _change_name(self, new_name):
        import re

        self._name = new_name.strip()
        re.sub(r"\W+", "", self._name)

    def reflect(self, input_letter_number):
        # input_letter_number -= prev_rotor_position
        # input_letter_number %= len(self.characters_in_use)
        return self._reflector_num_dict[input_letter_number]

    def _reset_dictionaries(self):
        self._reflector_dict = dict(
            zip(copy.copy(self._characters_in_use), copy.copy(self._characters_in_use))
        )
        self._update_dicts()

    def _update_dicts(self, letter_to_num=True):
        if letter_to_num:
            self._reflector_num_dict = transform_single_dict(
                self._reflector_dict, self._conversion_in_use
            )
        else:
            self._reflector_dict = transform_single_dict(
                self._reflector_num_dict, self._conversion_in_use
            )

    # def export_reflector(self):
    #     # if self.name == "name":
    #     #     print(
    #     #         ">Please assign a new name to the reflector with the function self.configure() or self.change_name()"
    #     #     )
    def random_name(self):
        # if not seed:
        #     stringOutput("Please input a seed."))
        #     return
        # random.seed(seed)
        # Set name
        # !!! Make sure letters do not connect to themselves!!!
        name_list = [random.sample(range(0, 26), 1)[0] for _ in range(0, 10)]
        name_list[0:6] = [chr(num + 65) for num in name_list[0:6]]
        name_list[6:10] = [str(i % 10) for i in name_list[6:10]]
        string1 = ""  # Why is this here? I am not super sure
        new_name = string1.join(name_list)
        self.change_name(new_name)

    def random_setup(self, seed=None, showConfig=False):
        # Now set the connections
        # num_list = [i for i in range(0, 26)]
        random.seed(seed)
        letter_list1 = copy.copy(self._characters_in_use)
        random.shuffle(letter_list1)
        # letter_list2 = copy.copy(self.characters_in_use)
        # random.shuffle(letter_list2)
        while len(letter_list1) > 1:
            letterA = letter_list1.pop()
            letterB = letter_list1.pop()
            self.reflector_dict[letterA] = letterB
            self.reflector_dict[letterB] = letterA
        if len(letter_list1) == 1:
            self.reflector_dict[letter_list1[0]] = letter_list1[0]
        self._update_dicts()
        # Show final configuration
        if showConfig:
            self._show_config()
        # Export
        # self.export_reflector()


class ReflectorDash(Reflector):
    def __init__(self):
        super().__init__(CHARACTERS_dash, EQUIVALENCE_DICT_dash)
        # self.reflector_dict={letter:letter for letter in CHARACTERS_dash}

    # def _update_dicts(self, letter_to_num=True):
    #     if letter_to_num:
    #         self.reflector_num_dict = transform_single_dict_dash(self.reflector_dict)
    #     else:
    #         self.reflector_dict = transform_single_dict_dash(self.reflector_num_dict)

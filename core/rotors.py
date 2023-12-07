import random
import pickle
import os
import copy
from .utils import (
    transform_single_dict,
    CHARACTERS,
    CHARACTERS_dash,
    EQUIVALENCE_DICT,
    EQUIVALENCE_DICT_dash,
)


class Rotor:
    def __init__(self, characters=CHARACTERS, conversion=EQUIVALENCE_DICT):
        # Note: variables can be defined on the fly

        self._name = "name"  # randomly generating a name is going to happen I guess
        self._notches = [
            25
        ]  # self.notch can be a list. When does the next rotor move relative to the notch?
        self._position = 1  # Can go from 1 to 26
        # self.jump=1 #Jump between positions. Can be changed for extra randomness, but carefully, never zero or 26
        # #Jump implementation will be done last. It can get complicated. Possible future feature
        self._characters_in_use = copy.copy(characters)
        self._conversion_in_use = copy.copy(conversion)

        self._forward_dict = dict(zip(self._characters_in_use, self._characters_in_use))

        self._backward_dict = dict(
            zip(self._characters_in_use, self._characters_in_use)
        )

        self._update_dicts()
        print(">Rotor has been created")

    def get_name(self):
        return self._name

    def get_position(self):
        return self._position

    def get_notchlist(self):
        return [self._conversion_in_use[i] for i in self._notches]

    def notch_check_move_forward(self):
        if self._position in self._notches:
            self._position += 1
            self._position %= 26
            return True
        else:
            self._position += 1
            self._position %= 26
            return False

    def backspace(self):
        self._position -= 1
        self._position %= 26
        return self._position in self._notches

    def forward_pass(self, input_letter_number):
        input_letter_number += self._position
        input_letter_number %= len(self._characters_in_use)
        output_number = self._forward_num_dict[input_letter_number]
        output_number -= self._position
        output_number %= len(self._characters_in_use)
        return output_number

    def backward_pass(self, input_letter_number):
        input_letter_number += self._position
        input_letter_number %= len(self._characters_in_use)
        output_number = self._backward_num_dict[input_letter_number]
        output_number -= self._position
        output_number %= len(self._characters_in_use)
        return output_number

    def _change_name(self, new_name):
        import re

        self._name = new_name.strip()
        re.sub(r"\W+", "", self._name)
        print(">Now name of the reflector is:", self._name)

    def _define_rotor_jump(self, jump):
        self.jump = jump
        print(
            ">Now rotor jumps ",
            jump,
            " spaces for every input (not yet implemented in the machine)",
        )

    # Do dictionaries of str(numbers) to the new number (or the number of the new letter), and do 1 for each direction

    def _define_position(self, position):
        self._position = self._conversion_in_use[position]
        print(
            ">Now rotor is in letter position {}".format(
                self._conversion_in_use[self._position]
            )
        )

    def _define_notches(self, position):
        position = [i for i in position]
        notch_list = [
            self._conversion_in_use[notch]
            for notch in position
            if notch in self._characters_in_use
        ]
        if not notch_list:
            return
        self._notches = notch_list
        print(
            ">Now the rotor has {} notches in positions {}".format(
                len(notch_list), position
            )
        )

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

    def export_rotor(self):
        if self._name == "name":
            print(
                ">Please assign a new name to the rotor with the function self.configure() or self.change_name()"
            )
        current_path = os.path.dirname(__file__)
        new_folder = "SAVED_ROTORS"
        path = os.path.join(current_path, new_folder)
        if not os.path.exists(path):
            os.mkdir(path)
            print(">Directory '% s' created" % new_folder)
        save_file = open(r"{}\\{}.rotor".format(path, self._name), "wb")
        pickle.dump(self, save_file)
        print(
            ">{} has been saved into {}.rotor in {}".format(
                self._name, self._name, path
            )
        )
        save_file.close()

    def show_config(
        self,
    ):  # Everything from the rotor, it will be launched from the machine though
        print("Rotor letter position :", self._conversion_in_use[self._position])
        print("Rotor letter jumps:", self.jump)
        notchlist = [self._conversion_in_use[i] for i in self._notches]
        print("Rotor notches:", notchlist)
        print("Forward connections in the rotor:", self._forward_dict)
        print("Backward connections in the rotor:", self._backward_dict)
        print("Rotor name:", self._name)

    def random_setup(self, seed=None, showConfig=True):
        # Randomly generate a rotor and store it in a folder
        # Seed has to be added from the machine calling the function, where the seed is stored/generated
        if not seed:
            print(
                ">>Something went wrong. Make sure development has reached this stage!"
            )
        # Once the seed is set, as long as the same operations are performed the same numbers are generated:
        random.seed(seed)
        # Name generation
        name_list = [
            random.sample(range(0, len(self._characters_in_use)), 1)[0]
            for _ in range(0, 13)
        ]
        name_list[0:9] = [self._conversion_in_use[num] for num in name_list[0:9]]
        name_list[9:13] = [str(i % 10) for i in name_list[9:13]]
        string1 = ""
        name = string1.join(name_list)
        self._change_name(name)
        # Position
        self._define_position(
            self._conversion_in_use[random.randint(0, len(self._characters_in_use))]
        )  # Check in the future whether this setups are correct
        # Notches
        notch_list = [
            self._conversion_in_use[i]
            for i in set(
                random.sample(
                    range(0, len(self._characters_in_use)), random.randint(1, 5)
                )
            )
        ]
        self._define_notches(notch_list)
        # self.define_rotor_jump(random.randint(1,25))
        # Forward dictionary
        num_list = list(range(0, len(self._characters_in_use)))
        self._forward_num_dict = dict(
            zip(
                num_list,
                random.sample(
                    range(0, len(self._characters_in_use)), len(self._characters_in_use)
                ),
            )
        )
        sorted_dict = dict(sorted(self._forward_num_dict.items(), key=lambda x: x[1]))
        self._backward_num_dict = dict(zip(sorted_dict.values(), sorted_dict.keys()))
        print(">Rotor connections established")
        self._update_dicts(False)
        if showConfig:
            self.show_config()
        self.export_rotor()
        return
        # And we use this to generate numbers and lists of numbers from which to derive configurations, notches, positions and names
        # in the case of the connection board, an extra number should be used to determine number of connections, same as notches.


class RotorDash(Rotor):
    def __init__(self):
        super().__init__(CHARACTERS_dash, EQUIVALENCE_DICT_dash)

    # def _update_dicts(self, letter_to_num=True):
    #     if letter_to_num:
    #         self._forward_num_dict = transform_single_dict_dash(self._forward_dict)
    #         self._backward_num_dict = transform_single_dict_dash(self._backward_dict)
    #     else:
    #         self._forward_dict = transform_single_dict_dash(self._forward_num_dict)
    #         self._backward_dict = transform_single_dict_dash(self._backward_num_dict)

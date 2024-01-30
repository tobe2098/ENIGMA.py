# from platform import machine
import random
import pickle
import pandas as pd
import copy

# import sys
import os

from .rotors import Rotor, RotorDash
from ..utils.utils import (
    CHARACTERS,
    CHARACTERS_dash,
    EQUIVALENCE_DICT,
    EQUIVALENCE_DICT_dash,
    MAX_NO_ROTORS,
    MAX_SEED,
)
from .reflectors import Reflector, ReflectorDash
from .plugboards import PlugBoard, PlugBoardDash


class Machine:
    def __init__(
        self, name="name", seed=None, characters=CHARACTERS, conversion=EQUIVALENCE_DICT
    ):
        self._name = name
        # Include seed storages?
        # Write a default config
        self._ref_rotor = Rotor()
        self._set_new_no_rotors(3)
        self._reflector = Reflector()
        self._characters_in_use = copy.copy(characters)
        self._conversion_in_use = copy.copy(conversion)
        if not seed:
            # Number has to be big, but how
            self._seed = random.randint(
                0,
                MAX_SEED,
            )
            print("Seed has been randomly generated, and is now:", self._seed)
        else:
            self._seed = seed
        # For now, default is nothingness
        self._plugboard = PlugBoard()
        self._current_input_size = 0
        # self.board_num_dict=transform_single_dict(self.board_dict)
        print(
            ">WARNING:Machine was just created, but it is NOT recommended for use until further configuration is done"
        )

    # Basic functions
    def get_name_and_seed(self):
        print(
            ">Machine name is {}, and its random seed is {}\n>REMEMBER! Communicating the random seed or further adjsutments for the machine is the weakest link for its usage. \nPlease do it with care, do not leave it written anywhere after the opposite party has a configured machine.".format(
                self._name, self._seed
            )
        )

    def _change_name(self, new_name):
        import re

        self._name = new_name.strip()
        re.sub(r"\W+", "", self._name)
        print(">The machine's name is now:", self._name)

    def _set_new_no_rotors(self, noRotors):
        self._rotors = [copy.copy(self._ref_rotor) for _ in range(noRotors)]

    def _append_rotors(self, noRotors):
        for _ in range(noRotors):
            self._rotors.append(copy.copy(self._ref_rotor))

    # def add_a_rotor(self):
    #     self.rotor4=Rotor()
    #     self.n_rotors=4
    #     print(">>>Fourth rotor added. Use self.rotor4.manual_rotor_setup() to modify or self.rotor4.random_rotor_setup()")
    # Showing configs

    def show_config(self):
        print(">Board config:")
        self._plugboard._show_config()
        print(">Rotor configs:")
        self.show_rotor_config()
        print(">Reflector config:")
        self._reflector._show_config()

    def simple_show_config(self):
        config = pd.DataFrame()
        config["Rotor position"] = list(range(1, len(self._rotors)))
        config["Rotors"] = [rotor.get_name() for rotor in self._rotors]
        config["Letter position"] = [rotor._position for rotor in self._rotors]
        config["Notches"] = [rotor.get_notchlist_letters() for rotor in self._rotors]
        print("Board config:")
        self._plugboard._show_config()
        print("Reflector:", self._reflector.name)
        print("Reflector:", self._reflector.name)
        print("Rotor config:\n", config)
        print("Machine name and seed:", self.get_name_and_seed())
        # return config #Only names, positions, letter positions and notches, and board, reflector name

    # def _single_rotor_setup(self, rotor: Rotor):
    #     rotor.show_config()
    #     rotor.configure()
    #     print(">Rotor setup finished, going back to selection")

    # Pickled functions
    def save_machine(self):
        while self._name.strip() == "name" or self._name.strip() == "":
            self._name = input(">>>Please assign a new name to the machine:")
        current_path = os.path.dirname(__file__)
        new_folder = "SAVED_MACHINES"
        path = os.path.join(current_path, new_folder)
        if not os.path.exists(path):
            os.mkdir(path)
            print("Directory '% s' created" % path)
        save_file = open(r"{}/{}.machine".format(path, self._name), "wb")
        pickle.dump(self, save_file)
        print(
            "{} has been saved into {}.machine in {}".format(
                self._name, self._name, path
            )
        )
        save_file.close()
        # return  # End

    def setup_random_machine(self):
        print(">Randomly generating your ENIGMA machine:")
        noRotors = "a"
        while not isinstance(noRotors, int):
            noRotors = input(">>>Input the number of rotors:")
            if noRotors > MAX_NO_ROTORS:
                noRotors = ""
                print(
                    "Maximum number of rotors allowed is {} (for your own good)".format(
                        MAX_NO_ROTORS
                    )
                )
        self._rotors = [copy.copy(self._ref_rotor) for _ in range(noRotors)]
        random.seed(self._seed)
        jump = random.randint(1, 3000000)
        self._reflector._random_setup(self._seed * jump)
        self._random_conf_rotors(jump)
        self._plugboard.random_setup(self._seed / jump)
        # Generating the name
        name_list = [random.sample(range(0, 26), 1)[0] for _ in range(0, 20)]
        name_list[0:14] = [self._conversion_in_use[num] for num in name_list[0:14]]
        name_list[14:20] = [str(i % 10) for i in name_list[14:20]]
        string1 = ""
        name = string1.join(name_list)
        self._change_name(name)
        self.show_config()
        self.save_machine()
        print(">Machine has been generated, saved and it is ready for use!")

    # Finally, the crypt function
    def encrypt_decrypt(self):
        CALL FOR CHECKS OF PROPER SETUP IN PLACE (AT LEAST ALL REFLECTOR CONNECTED, AT LEAST 1 ROTOR, AT LEAST ONE NOTCH PER ROTOR, SAVED MACHINE)
        # import copy as cp
        print(
            ">Every time you write a message, the machine will return to the configuration it is now. \n>WARNING: Do NOT use spaces, please.\n >>>If you want to stop, press Enter with no input."
        )
        # self.simple_show_config()
        input_var = 1
        while input_var:
            # message_length = 0
            input_var = input(
                ">>>Write Text (only letters and - will be encrypted): "
            ).upper()
            output_message_list = []
            # print(self.rotor1._position)
            for char in input_var:
                if char not in self._characters_in_use:
                    continue
                self._current_input_size += 1
                # First, position changes in rotors.
                for i in range(len(self._rotors)):
                    if not self._rotors[i].notch_check_move_forward():
                        break
                # Now we can perform the current circuit in the ENIGMA machine
                # Raw input converted to numerical.
                forward_output = self._conversion_in_use[char]
                # Board output 1
                forward_output = self._plugboard._input_output(forward_output)
                # forward_output = self._rotors[0].forward_pass(forward_output)
                for i in range(len(self._rotors)):
                    forward_output = self._rotors[i].forward_pass(forward_output)
                backward_output = self._reflector.reflect(forward_output)
                for i in range(len(self._rotors)):
                    backward_output = self._rotors[i].backward_pass(backward_output)
                backward_output = self._plugboard._input_output(backward_output)

                letter_out = self._conversion_in_use[backward_output]
                output_message_list.append(letter_out)
            string1 = ""
            message = string1.join(output_message_list)
            print(message)
            self.backspace(self._current_input_size)

    def type_character(self, character):
        if len(character) > 1:
            raise Exception(
                "Interfacing error, more than one character was not expected"
            )
        if character not in self._characters_in_use:
            return ""
        # First, position changes in rotors.
        self._current_input_size += 1
        for i in range(len(self._rotors)):
            if not self._rotors[i].notch_check_move_forward():
                break
        # Now we can perform the current circuit in the ENIGMA machine
        # Raw input converted to numerical.
        forward_output = self._conversion_in_use[character]
        # Board output 1
        forward_output = self._plugboard._input_output(forward_output)
        # forward_output = self._rotors[0].forward_pass(forward_output)
        for i in range(len(self._rotors)):
            forward_output = self._rotors[i].forward_pass(forward_output)
        backward_output = self._reflector.reflect(forward_output)
        for i in range(len(self._rotors)):
            backward_output = self._rotors[i].backward_pass(backward_output)
        backward_output = self._plugboard._input_output(backward_output)

        letter_out = self._conversion_in_use[backward_output]
        return letter_out

    def backspace(self, no_times=1):
        # For erasing all the input box in GUI, I can keep track of the inputs with an internal variable
        # And call this with internal variable
        for _ in range(no_times):
            for i in range(len(self._rotors)):
                if not self._rotors[i].backspace():
                    break


class MachineDash(Machine):
    def __init__(self, name="name", seed=None):
        super().__init__(name, seed, CHARACTERS_dash, EQUIVALENCE_DICT_dash)
        self._ref_rotor = RotorDash()
        self._reflector = ReflectorDash()
        self._plugboard = PlugBoardDash()
        self._set_new_no_rotors(3)

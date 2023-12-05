# from platform import machine
import random
import pickle
import pandas as pd

# import sys
import os

# path=os.path.dirname(os.path.dirname((__file__)))
# sys.path.append(path)
from .rotors import *
from .utils import *
from .reflectors import *
from .plugboards import *


class ENIGMAmachine:
    def __init__(
        self, name="name", seed=None, characters=CHARACTERS, conversion=EQUIVALENCE_DICT
    ):
        self._name = name
        # Include seed storages?
        # Write a default config
        self._ref_rotor = Rotor()
        self._change_no_rotors(3)
        self._reflector = Reflector()
        self._characters_in_use = copy.copy(characters)
        self._conversion_in_use = copy.copy(conversion)
        if not seed:
            # Number has to be big, but how
            self._seed = random.randint(
                0,
                9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999,
            )
            print("Seed has been randomly generated, and is now:", self._seed)
        else:
            self._seed = seed
        # For now, default is nothingness
        self._plugboard = PlugBoard()
        # self.board_num_dict=transform_single_dict(self.board_dict)
        print(
            ">WARNING:Machine was just created, but it is NOT recommended for use until further configuration is done"
        )

    # Basic functions
    def name_seed(self):
        print(
            ">Machine name is {}, and its random seed is {}\n>REMEMBER! Communicating the random seed or further adjsutments for the machine is the weakest link for its usage. \nPlease do it with care, do not leave it written anywhere after the opposite party has a configured machine.".format(
                self._name, self._seed
            )
        )

    def _change_name(self, new_name):
        self._name = new_name
        print("The machine's name is now:", self._name)

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
    def show_rotor_config(self):
        print("ROTORS START")
        for i in range(len(self._rotors)):
            print("Rotor no. {}:".format(i + 1))
            self._rotors[i].show_config()
        print("ROTORS END")

    def show_config(self):
        print("Board config:")
        self._plugboard.show_config()
        print("Rotor configs:")
        self.show_rotor_config()
        print("Reflector config:")
        self._reflector.show_config()

    def simple_show_config(self):
        config = pd.DataFrame()
        config["Rotor position"] = list(range(1, len(self._rotors)))
        config["Rotors"] = [rotor.get_name() for rotor in self._rotors]
        config["Letter position"] = [rotor._position for rotor in self._rotors]
        config["Notches"] = [rotor.get_notchlist() for rotor in self._rotors]
        print("Board config:")
        self._plugboard.show_config()
        print("Reflector:", self._reflector.name)
        print("Reflector:", self._reflector.name)
        print("Rotor config:\n", config)
        print("Machine name and seed:", self.name_seed())
        # return config #Only names, positions, letter positions and notches, and board, reflector name

    def _single_rotor_setup(self, rotor: Rotor):
        rotor.show_config()
        rotor.configure()
        print(">Rotor setup finished, going back to selection")

    # Manual configs
    def _all_rotor_setup(self):
        self.show_rotor_config()
        raise Exception
        # Maybe client no-gui? Remove editors from here then, bc not compatible with GUI
        # NEED A FULL MENU HERE, WITH ADD R/C/L, REMOVE, RESET AND RANDOMIZE, RESET AND CONFIGURE, LOAD ROTORS IN PLACE
        print("The machine currently has {} rotors".format(len(self._rotors)))
        self._append_rotors(input("Number of rotors to add? "))
        # while True:
        choose = input("Do you want to use only the same rotors?[y/n]:")
        if choose == "y":
            self._tune_loaded_rotors()
            self._rotor_order_change()
            self._change_rotor_letter_position()
            self._change_rotor_notches()
        elif choose == "n":
            choose2 = input(
                "Do you want to import pre-existing rotors that are not in the machine?[y/n]:"
            )
            if choose2 == "y":
                for i in range(input("Input desired number of rotors: ")):
                    print("Choosing a rotor for position no. {}:".format(i))
                    self._rotors[i].import_rotor()
            elif choose2 == "n":
                print(
                    "Rotors will be generated and saved randomly, you can edit them later."
                )
                self.generate_random_rotors()
        print(">Setup of rotors finished, going back to selection")

    def _manual_rotor_setup(self):
        while True:
            raise Exception
            # NEED A FULL MENU HERE, WITH ADD R/C/L, REMOVE, RESET AND RANDOMIZE, RESET AND CONFIGURE, LOAD ROTORS IN PLACE

            actionEnum = (
                input(
                    ">>>Input rotor number to configure the rotor (press 0 to configure all, any higher number to abort):"
                )
                - 1
            )
            if actionEnum == -1:
                self._all_rotor_setup()
            elif actionEnum < len(self._rotors):
                self._single_rotor_setup(self._rotors[actionEnum])
            else:
                break
        print(">Setup of rotors completed.")

    def manual_complete_config(self):
        # MENU HERE TOO
        raise Exception
        # Board
        print(">Configurating the connection board:")
        self._plugboard.manual_board_setup()
        # Rotors
        print(">Configurating rotors:")
        self._manual_rotor_setup()
        # Reflector
        print(">Configurating reflector:")
        self._reflector.configure()
        # Name. IMPORTANT: name is used to save as pickled object.
        # Not changing the name will overwrite previous machine with same name
        print("Machine is ready to go. Changing name is advised.")
        name = input(
            "Input machine name (previous save with the same name will be overwritten):"
        )
        self.change_name(name)
        self.save_machine()

    # Pickled functions
    def save_machine(self):
        if self._name == "name":
            print(
                "Please assign a new name to the machine with the function self.manual_complete_config() or self.change_name(name)"
            )
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

    def load_machine(
        self,
    ):  # THIS LOAD FUNCTION IS DEPRECATED, IT DOES NOT WORK, USE THE ONE THAT IS NOT CLASS DEFINED
        current_path = os.path.dirname(__file__)
        new_folder = "SAVED_MACHINES"
        path = os.path.join(current_path, new_folder)
        if not os.path.exists(path):
            print("There is no {} folder".format(path))
            return
        list_of_files = [element.rsplit((".", 1)[0])[0] for element in os.listdir(path)]
        if len(list_of_files) == 0:
            print("There are no machines saved")
            return
        print("Your available machines are:")
        for i in list_of_files:
            print(i)
        machine = int(input("Input machine's position in the list:"))
        file = os.path.join(path, "{}.machine".format(list_of_files[machine - 1]))
        filehandler = open(file, "rb")
        self = pickle.load(filehandler)
        filehandler.close()
        # return self  # End

    # Intern setup functions
    def _change_rotor_letter_position(self):
        pos1 = input("Letter position for rotor 1:")
        pos2 = input("Letter position for rotor 2:")
        pos3 = input("Letter position for rotor 3:")
        if self.rotor4:
            pos4 = input("Letter position for rotor 4:")
            self.rotor4._define_position(pos4)
        self.rotor1._define_position(pos1)
        self.rotor2._define_position(pos2)
        self.rotor3._define_position(pos3)
        return "Rottor letter positions set"

    def _rotor_order_change(self):
        while True:
            for i in range(len(self._rotors)):
                print("Rotor {}:".format(i + 1), self._rotors[i].get_name())
            selec1 = input(
                "Select rotor to put in a placeholder to get swapped (-1 to exit):"
            )
            selec2 = input(
                "Select rotor to put placeholder's order position and complete swap:"
            )

            if selec1 == -1:
                print("Finished with swaps")
                return
            else:
                selec1 -= 1
                selec2 -= 1
                self._rotors[selec1], self._rotors[selec2] = (
                    self._rotors[selec2],
                    self._rotors[selec1],
                )

    def _change_rotor_notches(self):
        for i in range(len(self._rotors)):
            print("Rotor {} notches:", self._rotors[i].get_notchlist())
            self._rotors[i]._define_notches(input("Input new notches(empty to skip):"))

    def _tune_loaded_rotors(self):
        for i in range(len(self._rotors)):
            print("Configurating rotor {} connections:".format(i))
            self._rotors[i].customize_connections()

    # RNG functions
    def _random_conf_rotors(self, jump):
        for i in range(len(self._rotors)):
            self._rotors[i].random_setup(self._seed + jump, showConfig=False)
            jump += 1
        return ">Rotors and reflector set up and saved."

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
        self._rotors = [Rotor() for _ in range(noRotors)]
        random.seed(self._seed)
        jump = random.randint(1, 3000000)
        self._reflector.random_setup(self._seed * jump)
        self._random_conf_rotors(jump)
        self._plugboard.randomize_board_dict(self._seed / jump)
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
        import copy as cp

        print(
            ">Every time you write a message, the machine will return to the configuration it is now. \n>WARNING: Do NOT use spaces, please.\n >>>If you want to stop, press Enter with no input."
        )
        # self.simple_show_config()
        input_var = 1
        while input_var:
            message_length = 0
            input_var = input(
                ">>>Write Text (only letters and - will be encrypted): "
            ).upper()
            output_message_list = []
            # print(self.rotor1._position)
            for char in input_var:
                if char not in self._characters_in_use:
                    continue
                message_length += 1
                # First, position changes in rotors.
                for i in range(len(self._rotors)):
                    if not self._rotors[i].notch_check_move_forward():
                        break
                # Now we can perform the current circuit in the ENIGMA machine
                # Raw input converted to numerical.
                forward_output = self._conversion_in_use[char]
                # Board output 1
                forward_output = self._plugboard.input_output(forward_output)
                # forward_output = self._rotors[0].forward_pass(forward_output)
                for i in range(len(self._rotors)):
                    forward_output = self._rotors[i].forward_pass(forward_output)
                backward_output = self._reflector.reflect(forward_output)
                for i in range(len(self._rotors)):
                    backward_output = self._rotors[i].backward_pass(backward_output)
                backward_output = self._plugboard.input_output(backward_output)

                letter_out = self._conversion_in_use[backward_output]
                output_message_list.append(letter_out)
            string1 = ""
            message = string1.join(output_message_list)
            print(message)
            self.backspace(message_length)

    def type_character(self, character):
        if len(character) > 1:
            raise Exception(
                "Interfacing error, more than one character was not expected"
            )
        if character not in self._characters_in_use:
            return ""
        # First, position changes in rotors.
        for i in range(len(self._rotors)):
            if not self._rotors[i].notch_check_move_forward():
                break
        # Now we can perform the current circuit in the ENIGMA machine
        # Raw input converted to numerical.
        forward_output = self._conversion_in_use[character]
        # Board output 1
        forward_output = self._plugboard.input_output(forward_output)
        # forward_output = self._rotors[0].forward_pass(forward_output)
        for i in range(len(self._rotors)):
            forward_output = self._rotors[i].forward_pass(forward_output)
        backward_output = self._reflector.reflect(forward_output)
        for i in range(len(self._rotors)):
            backward_output = self._rotors[i].backward_pass(backward_output)
        backward_output = self._plugboard.input_output(backward_output)

        letter_out = self._conversion_in_use[backward_output]
        return letter_out

    def backspace(self, no_times=1):
        for _ in range(no_times):
            for i in range(len(self._rotors)):
                if not self._rotors[i].backspace():
                    break


def load_existing_machine():
    current_path = os.path.dirname(__file__)
    new_folder = "SAVED_MACHINES"
    path = os.path.join(current_path, new_folder)
    if not os.path.exists(path):
        print("There is no {} folder".format(path))
        return
    list_of_files = [element.rsplit((".", 1)[0])[0] for element in os.listdir(path)]
    if len(list_of_files) == 0:
        print("There are no machines saved")
        return
    print("Your available machines are:")
    for i in list_of_files:
        print(i)
    machine = int(input("Input machine's position in the list:"))
    file = os.path.join(path, "{}.machine".format(list_of_files[machine - 1]))
    filehandler = open(file, "rb")
    machine = pickle.load(filehandler)
    filehandler.close()
    return machine

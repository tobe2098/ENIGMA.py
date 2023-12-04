'''This module contains the rotor classes'''
import random
import pickle
import os
import copy
from .utils import CHARACTERS, CHARACTERS_dash, transform_single_dict, transform_single_dict_dash, simplify_board_dict


class Reflector:
    def __init__(self):
        self._name = "name"
        self._characters_in_use = copy.copy(CHARACTERS)
        self._reflector_dict = {
            letter: letter for letter in self.characters_in_use}
        self._reflector_num_dict = {}
        self._update_dicts()

    def _change_name(self, name):
        self.name = name
        print(">Now name of the reflector is:", name)

    def reflect(self, input_letter_number, prev_rotor_position):
        input_letter_number=-prev_rotor_position
        input_letter_number%=len(self.characters_in_use)
        return self.reflector_num_dict[input_letter_number]
    
    def _update_dicts(self, letter_to_num=True):
        if letter_to_num:
            self.reflector_num_dict = transform_single_dict(
                self.reflector_dict)
        else:
            self.reflector_dict = transform_single_dict(
                self.reflector_num_dict)

    def _manual_reflector_config(self):
        # Configuration of the cable reflector
        # PENDING: Make it stop after 26 letters have been assigned
        if self.reflector_dict:
            print(">Current reflector setup is:")
            print(">Connections:\n", simplify_board_dict(self.reflector_dict))
            print(">Name:", self.name)
            accbool = input(
                ">>>Input N if you do NOT want to change the reflector setup:")
            if accbool == "N":
                return
        if self.name == "name":
            print(">Changing the name is necessary for exporting it")
        new_name = input(
            ">>>Input new name for the reflector (Press Enter to skip):")
        if new_name:
            self.change_name(new_name)
        seen_letters = []
        reflector_dict = {letter: letter for letter in self.characters_in_use}
        all_letters = self.characters_in_use
        while True:
            if len(list(set(all_letters)-set(seen_letters))) == 0:
                break
            print(">If you want to stop configurating the reflector, press Enter")
            configpair = input(
                ">>>Enter pair of letters for reflector configuration:").upper()
            if configpair and not configpair.isalpha():
                print(">Error: Input 2 letters please")
                continue
            configpair = [i for i in configpair]
            if len(configpair) == 2:
                pass
            elif len(configpair) == 0:
                break
            else:
                print(">Error: Input 2 letters please")
                continue
            if any(map(lambda v: v in configpair, seen_letters)):
                print(">One of the letters was already plugged")
                continue
            else:
                seen_letters.append(configpair[0])
                seen_letters.append(configpair[1])
                reflector_dict[configpair[0]] = configpair[1]
                reflector_dict[configpair[1]] = configpair[0]
            print(">Current config:\n", simplify_board_dict(reflector_dict))
            remaining_letters=list(set(all_letters)-set(seen_letters))
            print(">Not connected letters:\n", remaining_letters)
        if len(remaining_letters)==1:
            reflector_dict[remaining_letters[0]]=remaining_letters[0]
        self._show_config()
        self.reflector_dict = reflector_dict
        self.update_dicts()
        self.export_reflector()
        print(">Finished")

    def _show_config(self):
        print(">Reflector name:", self.name)
        print(">Reflector config:\n", simplify_board_dict(self.reflector_dict))

    def _export_reflector(self):
        if self.name == "name":
            print(">Please assign a new name to the reflector with the function self.configure() or self.change_name()")
        current_path = os.path.dirname(__file__)
        new_folder = "SAVED_REFLECTORS"
        path = os.path.join(current_path, new_folder)
        if not os.path.exists(path):
            os.mkdir(path)
            print(">Directory '% s' created" % path)
        save_file = open(r'{}\\{}.reflector'.format(path, self.name), 'wb')
        pickle.dump(self, save_file)
        print(">{} has been saved into {}.reflector in {}".format(
            self.name, self.name, path))

    def import_reflector_config(self):
        current_path = os.path.dirname(__file__)
        new_folder = "SAVED_REFLECTORS"
        path = os.path.join(current_path, new_folder)
        if not os.path.exists(path):
            print(">There is no {} folder".format(path))
            return
        list_of_files = [element.rsplit(('.', 1)[0])[0]
                         for element in os.listdir(path)]
        if len(list_of_files) == 0:
            print(">There are no reflectors saved")
            return
        print(">Your available reflectors are: {}".format(list_of_files))
        reflector = input(">>>Input reflector's position in the list:")
        filehandler = open(r"{}\\{}.reflector".format(
            path, list_of_files[reflector-1]), 'rb')
        self = pickle.load(filehandler)

    def random_reflector_setup(self, seed=None, showConfig=True):
        random.seed(seed)
        # Set name
        # !!! Make sure letters do not connect to themselves!!!
        name_list = [random.sample(range(0, 26), 1)[0] for _ in range(0, 10)]
        name_list[0:6] = [chr(num+65) for num in name_list[0:6]]
        name_list[6:10] = [str(i % 10) for i in name_list[6:10]]
        string1 = ""  # Why is this here? I am not super sure
        new_name = string1.join(name_list)
        self.change_name(new_name)
        # Now set the connections
        # num_list = [i for i in range(0, 26)]
        letter_list1 = copy.copy(self.characters_in_use)
        random.shuffle(letter_list1)
        letter_list2 = copy.copy(self.characters_in_use)
        random.shuffle(letter_list2)
        while (len(letter_list1) > 0):
            letterA = letter_list1.pop()
            letterB = letter_list2.pop()
            self.reflector_num_dict[letterA] = letterB
            self.reflector_num_dict[letterB] = letterA
        self.update_dicts()
        # Show final configuration
        if showConfig:
            self._show_config()
        # Export
        self.export_reflector()


class ReflectorDash(Reflector):
    def __init__(self):
        super().__init__()
        self.characters_in_use = CHARACTERS_dash
        # self.reflector_dict={letter:letter for letter in CHARACTERS_dash}

    def update_dicts(self, letter_to_num=True):
        if letter_to_num:
            self.reflector_num_dict = transform_single_dict_dash(
                self.reflector_dict)
        else:
            self.reflector_dict = transform_single_dict_dash(
                self.reflector_num_dict)


def save_n_random_reflectors(n, seed):
    # Create and save into pickle objects 20 randomly generated rotors. Use seed to generate new seed, or simply add numbers
    for i in range(0, n):
        rotor = Reflector()
        rotor.random_reflector_setup(seed+i)
    return ">Done"


def tune_existing_reflector():
    reflector = Reflector()
    reflector.import_reflector_config()
    reflector._manual_reflector_config()
    reflector.export_reflector()
    return ">Reflector was edited and saved"
    # Conda activation: conda info --envs, conda activate {}

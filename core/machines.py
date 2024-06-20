# from platform import machine
import random
import copy

# import sys

from cli.functions.rotors_f import _load_saved_rotor
from utils.exceptions import raiseBadInputException, raiseBadSetupException

from .rotors import Rotor, RotorDash
from ..utils.utils import (
    CHARACTERS,
    CHARACTERS_dash,
    EQUIVALENCE_DICT,
    EQUIVALENCE_DICT_dash,
    MAX_NO_ROTORS,
    MAX_SEED,
    is_valid_seed,
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
        if not self._ref_rotor:
            self._ref_rotor = Rotor()
        self._set_new_no_rotors(3)
        if not self._reflector:
            self._reflector = Reflector()
        self._characters_in_use = copy.copy(characters)
        self._conversion_in_use = copy.copy(conversion)
        if not seed:
            # Number has to be big, but how
            self._seed = random.randint(
                0,
                MAX_SEED,
            )
            # print("Seed has been randomly generated, and is now:", self._seed)
        else:
            self._seed = seed
        # For now, default is nothingness
        if not self._plugboard:
            self._plugboard = PlugBoard()
        self._current_distance_from_original_state = 0
        # self.board_num_dict=transform_single_dict(self.board_dict)
        # print(
            # ">WARNING:Machine was just created, but it is NOT recommended for use until further configuration is done"
        # )


    # Basic functions
    def get_name(self):
        return self._name
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

    def _is_machine_set_up(self):
        return self._reflector.is_set_up() and all([rotor.is_set_up() for rotor in self._rotors]) and len(self._rotors)>0

    def _is_valid_no_rotors(self, noRotors):
        return noRotors>0 and noRotors<MAX_NO_ROTORS

    def _set_new_no_rotors(self, noRotors):
        if self._is_valid_no_rotors(noRotors):
            self._rotors = [copy.copy(self._ref_rotor) for _ in range(noRotors)]
        else:
            raiseBadInputException()

    def _append_rotors(self, noRotors):
        if self._is_valid_no_rotors(len(self._rotors)+noRotors):
            for _ in range(noRotors):
                self._rotors.append(copy.copy(self._ref_rotor))
        else:
            raiseBadInputException()
    def is_rotor_index_valid(self,idx):
        return isinstance(idx, int) and idx>=0 and idx<len(self._rotors)
    
    def _swap_two_rotors_by_index(self, idx1, idx2):
        if self.is_rotor_index_valid(idx1) and self.is_rotor_index_valid(idx2):
           self._rotors[idx1],self._rotors[idx2]=self._rotors[idx2],self._rotors[idx1] 
        else:
            raiseBadInputException()
        
    def _load_a_rotor_on_index(self,idx):
        if self.is_rotor_index_valid(idx):
            self._rotors.insert(idx,_load_saved_rotor())
        elif idx>len(self._rotors):
            self._rotors.append(_load_saved_rotor())
        else:
            raiseBadInputException()
        
    def _get_rotors_names_positions(self):
        return [rotor.get_name() for rotor in self._rotors]
        
    def _are_positions_valid(self,string_positions):
        return all([char in self._characters_in_use for char in string_positions]) and len(string_positions)==len(self._rotors)
    
    def _change_rotors_positions(self,positions_string:str):
        #Here we get a string of positions to set to the rotors in the list of rotors (all of them)
        #First we check that all characters of the string are valid
        if self._are_positions_valid(positions_string):
            for i in range(len(positions_string)):
                self._rotors[i]._define_position(positions_string[i])
        else:
            raiseBadInputException()

    def _reorder_all_rotors(self,position_list:list):
        #For every rotor they are asigned a new position in the list with their index
        #First we check that the position list that we are given is a scrambled list of non-repeated valid indexes
        positions_copy=copy.copy(position_list)
        positions_copy.sort()
        if all([self.is_rotor_index_valid(idx) for idx in position_list]) and positions_copy==list(range(len(self._rotors))):
            new_rotor_list=[i for i in range(len(self._rotors))]
            for i in range(len(self._rotors)):
                new_rotor_list[position_list[i]]=self._rotors[i]
            self._rotors=new_rotor_list
        else:
            raiseBadInputException()

    # def _single_rotor_setup(self, rotor: Rotor):
    #     rotor.show_config()
    #     rotor.configure()
    #     print(">Rotor setup finished, going back to selection")
    def _random_conf_rotors(self, jump):
        if not is_valid_seed(jump):
            raiseBadInputException()
        temp_seed=self._seed
        for rotor_ptr in self._rotors:
            temp_seed+=jump
            rotor_ptr._randomize_dictionaries(temp_seed)
            rotor_ptr._random_name(temp_seed)
            rotor_ptr._randomize_position(temp_seed)
            rotor_ptr._randomize_notches(temp_seed)


    # Pickled functions

    def setup_random_machine(self, seed=None, noRotors=3):
        if not is_valid_seed(seed) or not self._is_valid_no_rotors(noRotors):
            raiseBadInputException()
        self._rotors = [copy.copy(self._ref_rotor) for _ in range(noRotors)]
        random.seed(self._seed)
        jump = random.randint(1, int(3e8))
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
        # self.show_config()
        # self.save_machine()

    # Finally, the crypt function <<<HERE IS WHERE I WAS LEFT, I NEED TO FINISH CRYPT LETTER, TEXT
    ## Add text function and check for characters

    def encrypt_decrypt(self,text):
        if not self._is_machine_set_up():
            raiseBadSetupException()
        CALL FOR CHECKS OF PROPER SETUP IN PLACE (AT LEAST ALL REFLECTOR CONNECTED, AT LEAST 1 ROTOR, AT LEAST ONE NOTCH PER ROTOR, SAVED MACHINE)
        THIS SHOULD ONLY ENCRYPT A PASSED TEXT, AND A LETTER BY LETTER (FOR GUI)
        # import copy as cp
        print(
            ">Every time you write a message, the machine will return to the configuration it is now. \n>WARNING: Do NOT use spaces, please.\n >>>If you want to stop, press Enter with no input."
        )
        
        # self.simple_show_config()
        input_var = 1
        while input_var:
            # message_length = 0
            input_var = input(
                ">>>Write Text (only allowed characters will be encrypted): "
            ).upper()
            output_message_list = []
            # print(self.rotor1._position)
            for char in input_var:
                if char not in self._characters_in_use:
                    continue
                self._current_distance_from_original_state += 1
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
            self.backspace(self._current_distance_from_original_state)

    def type_character(self, character):
        if len(character) > 1:
            raiseBadInputException()
        if character not in self._characters_in_use:
            return ""
        # First, position changes in rotors.
        self._current_distance_from_original_state += 1
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
            for i in range(len(self._rotors)): #We always move from first to last rotor
                if not self._rotors[i].backspace():
                    break
    def backspace_to_original_state(self):
        # For erasing all the input box in GUI, I can keep track of the inputs with an internal variable
        # And call this with internal variable
        for _ in range(self._current_distance_from_original_state):
            for i in range(len(self._rotors)): #We always move from first to last rotor
                if not self._rotors[i].backspace():
                    break

class MachineDash(Machine):
    def __init__(self, name="name", seed=None):
        self._ref_rotor = RotorDash()
        self._reflector = ReflectorDash()
        self._plugboard = PlugBoardDash()
        super().__init__(name, seed, CHARACTERS_dash, EQUIVALENCE_DICT_dash)
        # self._set_new_no_rotors(3)

import pandas as pd
import random
from ROTORS import *
def split_into_list(string):
    return [character for character in string]
def simplify_board_config(board_dict):
    seen_pairs=[]
    pairs=[]
    all_letters=split_into_list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    for letter_a, letter_b in board_dict.items():
        if letter_a in seen_pairs or letter_b in seen_pairs:
            continue
        elif letter_b==letter_a:
            continue
        else:
            pass
        pairs.append([letter_a, letter_b])
        seen_pairs.append(letter_a)
        seen_pairs.append(letter_b)
    unpaired=list(set(all_letters)-set(seen_pairs))
    board_config_simpl=pd.DataFrame(pairs, columns=["Letter A", "Letter B"])
    board_config_simpl["Unpaired"]=unpaired
    return board_config_simpl
class ENIGMAmachine:
    def __init__(self, name, seed=None):
        self.name=name
        #Write a default config
        if not seed:
            self.seed=random.randint(0, 999999)
        else:
            self.seed=seed
        #For now, default is nothingness
        self.board_config={letter:letter for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
    def name_seed(self):
        print(self.__repr__())
    def __repr__(self):
        print("Machine's name is:", self.name)
        print("Random seed of the machine is:", self.seed)
        return ("Machine name is %, and its random seed is %" % (self.name, self.seed))
    def randomize_board_config(self):
        pass
    def fast_config(self, rnd_seed=None):
        if rnd_seed:
            self.seed=rnd_seed
        self.fast_config()
    #Change the name of the machine
    def change_name(self, new_name):
        self.name=new_name
    #Machine configuration

    def manual_board_config(self):
        #Configuration of the cable board
        #PENDING: Make it stop after 26 letters have been assigned
            i=0
            seen_letters=[]
            board_dict={letter:letter for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
            all_letters=split_into_list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            while i==0:
                print("If you want to stop configurating the board, press Enter")
                configpair=input("Enter pair of letters for board configuration:").upper()
                if configpair.isalpha() or not configpair:
                    pass
                else:
                    print("Error: Input 2 letters please")
                    continue
                configpair=split_into_list(configpair)
                if len(list(set(all_letters)-set(seen_letters)))==0:
                    break
                if len(configpair)==2:
                    pass
                elif len(configpair)==0:
                    break
                else:
                    print("Error: Input 2 letters please")
                    continue
                if any(map(lambda v: v in configpair, seen_letters)):
                    print("Already plugged")
                    continue
                else:
                    seen_letters.append(configpair[0])
                    seen_letters.append(configpair[1])
                    board_dict[configpair[0]]=configpair[1]
                    board_dict[configpair[1]]=configpair[0]
                print("Current config:\n", simplify_board_config(board_dict))
                print("Not connected letters:\n", list(set(all_letters)-set(seen_letters)))
            print("Finished")
            self.board_config=board_dict
    def show_config(self):
        print("Board config:", simplify_board_config(self))
    def encrypt_decrypt(self):
        for char in input('Write Text: ').upper():
            print(char)
            number=(ord(char) - 64)
    def rotor_setup(self):
        list_rotor=self.import_rotor_list()
        self.manual_rotor_setup(default_rotors=list_rotor)
        print("Setup finished")
    def manual_rotor_setup(self, default_rotors=None):
        rotor1=ROTOR("I")
    def import_rotor_list(self):
        return list_of_rotors
    def position_rotors(self):
        pass
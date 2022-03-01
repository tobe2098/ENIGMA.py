import random
from ROTORS import *
class ENIGMAmachine:
    def __init__(self, name, seed=None):
        self.name=name
        #Include seed storages?
        #Write a default config
        if not seed:
            self.seed=random.randint(0, 99999999) #Number has to be big
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
    def random_setup(self, rnd_seed=None):
        #Every random generation of an object should have the seed shifted so that elements do not repeat themselves.
        #Inside element seeds should +1, between elements seeds should +10 or -10.
        if rnd_seed:
            self.seed=rnd_seed
        self.random_setup()
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
        return #list_of_rotors
    def position_rotors(self):
        pass
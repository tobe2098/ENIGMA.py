import random
import pickle
from ENutils import *
class REFLECTOR:
    def __init__(self):
        self.name="name"
    def manual_reflector_config(self):
        #Configuration of the cable reflector
        #PENDING: Make it stop after 26 letters have been assigned
        if self.refl_dict:
            print("Current reflector setup is:", simplify_board_config(self.refl_dict))
            accbool=input("Input N if you do NOT want to change the reflector setup:")
            if accbool=="N":
                return
        i=0
        seen_letters=[]
        reflector_dict={letter:letter for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
        all_letters=split_into_list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        while i==0:
            print("If you want to stop configurating the reflector, press Enter")
            configpair=input("Enter pair of letters for reflector configuration:").upper()
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
                reflector_dict[configpair[0]]=configpair[1]
                reflector_dict[configpair[1]]=configpair[0]
            print("Current config:\n", simplify_board_config(reflector_dict))
            print("Not connected letters:\n", list(set(all_letters)-set(seen_letters)))
        print("Finished")
        self.show_config()
        self.refl_dict=reflector_dict
    def show_config(self):
        print("Reflector config:", simplify_board_config(self.refl_dict))
    def random_config(self, seed):
        random.seed(seed)



import random
import pickle
import os
from ENIGMA_py.ENutils import *
class REFLECTOR:
    def __init__(self):
        self.name="name"
    def change_name(self, name):
        self.name=name
        print("Now name of the reflector is:", name)
    def manual_reflector_config(self):
        #Configuration of the cable reflector
        #PENDING: Make it stop after 26 letters have been assigned
        if self.refl_dict:
            print("Current reflector setup is:")
            print("Connections:", simplify_board_config(self.refl_dict))
            print("Name:", self.name)
            accbool=input("Input N if you do NOT want to change the reflector setup:")
            if accbool=="N":
                return
        if self.name=="name":
            print("Changing the name is necessary for exporting it")
        new_name=input(">>>Input new name for the reflector (Press Enter to skip):")
        if new_name:
            self.change_name(new_name)
        i=0
        seen_letters=[]
        reflector_dict={letter:letter for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
        all_letters=split_into_list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        while i==0:
            print("*If you want to stop configurating the reflector, press Enter")
            configpair=input(">>>Enter pair of letters for reflector configuration:").upper()
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
        self.show_config()
        self.refl_dict=reflector_dict
        self.refl_num_dict=transform_single_dict(self.refl_dict)
        self.export_reflector()
        print("Finished")
    def show_config(self):
        print("Reflector name:", self.name)
        print("Reflector config:", simplify_board_config(self.refl_dict))
    def export_reflector(self):
        if self.name=="name":
            print("Please assign a new name to the reflector with the function self.configure() or self.change_name()")
        current_path=path = os.getcwd()
        new_folder = "SAVED_REFLECTORS"
        path = os.path.join(current_path, new_folder)       
        if not os.path.exists(path):
            os.mkdir(path)
            print("Directory '% s' created" % new_folder) 
        save_file = open('{}/{}.reflector'.format(path,self.name), 'w') 
        pickle.dump(self, save_file)
        print("{} has been saved into {}.reflector".format(self.name, self.name))
        return #End
    def import_reflector_config(self):
        current_path=path = os.getcwd()
        new_folder = "SAVED_REFLECTORS"
        path = os.path.join(current_path, new_folder)       
        if not os.path.exists(path):
            print("There is no SAVED_REFLECTORS folder")
            return
        list_of_files=[element.rsplit(('.', 1)[0])[0] for element in os.listdir(path)]
        if len(list_of_files)==0:
            print("There are no reflectors saved")
            return
        print("Your available reflectors are: {}".format(list_of_files))
        reflector=input("Input reflector's position in the list:")
        filehandler = open("{}/{}.reflector".format(path, list_of_files[reflector-1]), 'r') 
        self = pickle.load(filehandler)
        return #End
    def random_reflector_setup(self, seed):
        random.seed(seed)
        #Set name
        name_list=[random.sample(range(1, 27), 1)[0] for i in range(0, 10)]
        name_list[0:5]=[chr(num+64) for num in name_list[0:5]]
        name_list[5:8]=[str(i%10) for i in name_list[5:8]]
        string1=""
        new_name=string1.join(name_list)
        self.change_name(new_name)
        #Now set the connections
        num_list=[i for i in range(1,27)]
        self.refl_num_dict=dict(zip(num_list, random.sample(range(1, 27), 26)))
        self.refl_dict=transform_single_dict(self.refl_num_dict)
        #Show final configuration
        self.show_config()
        #Export
        self.export_reflector()
        return self
def save_n_random_reflectors(n, seed):
    #Create and save into pickle objects 20 randomly generated rotors. Use seed to generate new seed, or simply add numbers
    for i in range(0,n):
        rotor=REFLECTOR()
        rotor.random_reflector_setup(seed+i)
    return "Done"
def tune_existing_reflector():
    pass
    ##Conda activation: conda info --envs, conda activate {}

import random
import pickle
import os
from ENIGMA_py.ENutils import *
class REFLECTOR:
    def __init__(self):
        self.name="name"
        self.refl_dict={letter:letter for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
        self.refl_num_dict=transform_single_dict(self.refl_dict)
    def change_name(self, name):
        self.name=name
        print(">Now name of the reflector is:", name)
    def manual_reflector_config(self):
        #Configuration of the cable reflector
        #PENDING: Make it stop after 26 letters have been assigned
        if self.refl_dict:
            print(">Current reflector setup is:")
            print(">Connections:\n", simplify_board_dict(self.refl_dict))
            print(">Name:", self.name)
            accbool=input(">>>Input N if you do NOT want to change the reflector setup:")
            if accbool=="N":
                return
        if self.name=="name":
            print(">Changing the name is necessary for exporting it")
        new_name=input(">>>Input new name for the reflector (Press Enter to skip):")
        if new_name:
            self.change_name(new_name)
        i=0
        seen_letters=[]
        reflector_dict={letter:letter for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
        all_letters=split_into_list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        while i==0:
            print(">If you want to stop configurating the reflector, press Enter")
            configpair=input(">>>Enter pair of letters for reflector configuration:").upper()
            if configpair.isalpha() or not configpair:
                pass
            else:
                print(">Error: Input 2 letters please")
                continue
            configpair=split_into_list(configpair)
            if len(list(set(all_letters)-set(seen_letters)))==0:
                break
            if len(configpair)==2:
                pass
            elif len(configpair)==0:
                break
            else:
                print(">Error: Input 2 letters please")
                continue
            if any(map(lambda v: v in configpair, seen_letters)):
                print(">Already plugged")
                continue
            else:
                seen_letters.append(configpair[0])
                seen_letters.append(configpair[1])
                reflector_dict[configpair[0]]=configpair[1]
                reflector_dict[configpair[1]]=configpair[0]
            print(">Current config:\n", simplify_board_dict(reflector_dict))
            print(">Not connected letters:\n", list(set(all_letters)-set(seen_letters)))
        self.show_config()
        self.refl_dict=reflector_dict
        self.refl_num_dict=transform_single_dict(self.refl_dict)
        self.export_reflector()
        print(">Finished")
    def show_config(self):
        print(">Reflector name:", self.name)
        print(">Reflector config:\n", simplify_board_dict(self.refl_dict))
    def export_reflector(self):
        if self.name=="name":
            print(">Please assign a new name to the reflector with the function self.configure() or self.change_name()")
        current_path=os.path.dirname(__file__)
        new_folder = "SAVED_REFLECTORS"
        path = os.path.join(current_path, new_folder)       
        if not os.path.exists(path):
            os.mkdir(path)
            print(">Directory '% s' created" % path) 
        save_file = open(r'{}/{}.reflector'.format(path,self.name), 'wb') 
        pickle.dump(self, save_file)
        print(">{} has been saved into {}.reflector in {}".format(self.name, self.name, path))
        return #End
    def import_reflector_config(self):
        current_path=os.path.dirname(__file__)
        new_folder = "SAVED_REFLECTORS"
        path = os.path.join(current_path, new_folder)       
        if not os.path.exists(path):
            print(">There is no {} folder".format(path))
            return
        list_of_files=[element.rsplit(('.', 1)[0])[0] for element in os.listdir(path)]
        if len(list_of_files)==0:
            print(">There are no reflectors saved")
            return
        print(">Your available reflectors are: {}".format(list_of_files))
        reflector=input(">>>Input reflector's position in the list:")
        filehandler = open(r"{}/{}.reflector".format(path, list_of_files[reflector-1]), 'rb') 
        self = pickle.load(filehandler)
        return #End
    def random_reflector_setup(self, seed=None, randomE=True):
        random.seed(seed)
        #Set name
        ### !!! Make sure letters do not connect to themselves!!!
        name_list=[random.sample(range(0, 26), 1)[0] for i in range(0, 10)]
        name_list[0:6]=[chr(num+65) for num in name_list[0:6]]
        name_list[6:10]=[str(i%10) for i in name_list[6:10]]
        string1=""
        new_name=string1.join(name_list)
        self.change_name(new_name)
        #Now set the connections
        num_list=[i for i in range(0,26)]
        for i in range(13):
            indexA=random.randint(0,len(num_list)-1)
            letterA=num_list.pop(indexA)
            if len(num_list)==1:
                indexB=0
            else:
                indexB=random.randint(0,len(num_list)-1)
            letterB=num_list.pop(indexB)
            self.refl_num_dict[letterA]=letterB
            self.refl_num_dict[letterB]=letterA
        self.refl_dict=transform_single_dict(self.refl_num_dict)
        #Show final configuration
        if randomE:
            self.show_config()
        #Export
        self.export_reflector()
        return
def save_n_random_reflectors(n, seed):
    #Create and save into pickle objects 20 randomly generated rotors. Use seed to generate new seed, or simply add numbers
    for i in range(0,n):
        rotor=REFLECTOR()
        rotor.random_reflector_setup(seed+i)
    return ">Done"
def tune_existing_reflector():
    reflector=REFLECTOR()
    reflector.import_reflector_config()
    reflector.manual_reflector_config()
    reflector.export_reflector()
    return ">Reflector was edited and saved"
    ##Conda activation: conda info --envs, conda activate {}

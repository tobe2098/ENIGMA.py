#from turtle import position #???????????? wtf
import random
from ENIGMA import split_into_list, simplify_board_config, gen_rnd_26list
import pickle
import os
class ROTOR:
    def __init__(self):
        self.name="name" #randomly generating a name is going to happen I guess
        self.notch=26 #self.notch can be a list
        self.position=1
        self.jump=1 #Jump between positions. Can be changed for extra randomness, but carefully, never zero or 26
        #Jump implementation will be done last. It can get complicated.

        #Attributes defined by functions:
        ##self.entry_dict
        ##self.exit_dict
        ##self.entry_num_dict
        ##self.exit_num_dict
        print("Please customize connections before use with self.customize connections.\n If you want to configure all of the rotors' parameters, use self.configure.")
    def change_name(self, name):
        self.name=name
    def define_rotor_jump(self, jump):
        self.jump=jump
    #Do dictionaries of str(numbers) to the new number (or the number of the new letter), and do 1 for each direction
    def define_position(self, position):
        self.position=(ord(position) - 64)
        print("Now notch is in position {}".format(chr((self.position +64))))
    def define_notches(self, position):
        position=split_into_list(position)
        notch_list=[ord(notch)-64 for notch in position]
        self.notch=notch_list
    def configure_numeric_dicts(self):
        #First, forward dict
        rev_dict=self.entry_dict
        new_values=[ord(i)-64 for i in rev_dict.values()]
        new_keys=[ord(i)-64 for i in rev_dict.keys()]
        num_dict=dict(zip(new_keys, new_values))
        self.entry_num_dict=num_dict
        #Second, reverse dict
        rev_dict=self.exit_dict
        new_values=[ord(i)-64 for i in rev_dict.values()]
        new_keys=[ord(i)-64 for i in rev_dict.keys()]
        num_dict=dict(zip(new_keys, new_values))
        self.exit_num_dict=num_dict
        return #End

    def customize_connections(self):
        #PENDING: Make it stop after 26 letters have been assigned. Update from board config.
        i=0
        entry_seen_letters=[]
        exit_seen_letters=[]
        entry_rotor_dict={letter:letter for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
        exit_rotor_dict={letter:letter for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
        entry_list=split_into_list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        exit_list=split_into_list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        while i==0:
            print("If you want to stop configurating the rotor, press Enter")
            configpair=input("Enter pair of letters for board configuration:").upper()
            if configpair.isalpha() or not configpair:
                pass
            else:
                print("Error: Input 2 letters please")
                continue
            if len(list(set(entry_list)-set(entry_seen_letters)))==0:
                break
            configpair=split_into_list(configpair)
            if len(configpair)==2:
                pass
            elif len(configpair)==0:
                break
            else:
                print("Error: Input 2 letters please")
                continue
            if any(map(lambda v: v in configpair, entry_seen_letters)):
                print("Already plugged")
                continue
            if any(map(lambda v: v in configpair, exit_seen_letters)):
                print("Already plugged")
                continue
            else:
                entry_seen_letters.append(configpair[0])
                exit_seen_letters.append(configpair[1])
                entry_rotor_dict[configpair[0]]=configpair[1]
                exit_rotor_dict[configpair[1]]=configpair[0]
            print("Current entry config:\n", simplify_board_config(entry_rotor_dict))
            print("Current exit config:\n", simplify_board_config(exit_rotor_dict))
            print("Not connected entry letters:\n", list(set(entry_list)-set(entry_seen_letters)))
            print("Not connected exit letters:\n", list(set(exit_list)-set(exit_seen_letters)))
        self.entry_dict=entry_rotor_dict
        self.exit_dict=exit_rotor_dict
        self.configure_numeric_dicts()
        print("Finished")

    def configure(self):
        letter_list=split_into_list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        print("Press Enter with no input to skip configuration of the parameter.")
        name=input("Write the rotor's name:").upper()
        position=input("Write the rotor's position (in letters, only 1):").upper()
        print("For your cryptosecurity, input between 1 and 5 notches, not more.")
        notch=split_into_list(input("Write the rotor's notch position/s (in letters):").upper())
        jump=int(input("Write the position jump per letter (in a single number) **Do not put a number, not implemented:"))
        while boolean not in list("y", "n"):
            boolean=input("Do you want to configure the connections of the rotor?[y/n]")
        if name:
            self.change_name(name)
        if jump<26:
            self.define_rotor_jump(jump)
        if position in letter_list:
            self.define_position(position)
        if set(notch).issubset(letter_list): #DO this every time you want to check if set a is a subset of set b
            self.define_notches(notch)
        if boolean=="y":
            self.customize_connections()
        print("You have finished configuring your rotor. If you want to save it in a file, use self.export_rotor() \n*Careful while defining notches")
        return #End
    def export_rotor(self):
        if self.name=="name":
            print("Please assign a new name to the rotor with the function self.configure() or self.change_name()")
        current_path=path = os.getcwd()
        new_folder = "SAVED_ROTORS"
        path = os.path.join(current_path, new_folder)       
        if not os.path.exists(path):
            os.mkdir(path)
            print("Directory '% s' created" % new_folder) 
        save_file = open('{}/{}.rotor'.format(path,self.name), 'w') 
        pickle.dump(self, save_file)
        print("{} has been saved into {}.rotor".format(self.name, self.name))
        return #End
    def import_rotor_config(self):
        current_path=path = os.getcwd()
        new_folder = "SAVED_ROTORS"
        path = os.path.join(current_path, new_folder)       
        if not os.path.exists(path):
            print("There is no SAVED_ROTORS folder")
            return
        list_of_files=[element.rsplit(('.', 1)[0])[0] for element in os.listdir(path)]
        if len(list_of_files)==0:
            print("There are no rotors saved")
            return
        print("Your available rotors are: {}".format(list_of_files))
        rotor=input("Input rotor's position in the list:")
        filehandler = open("{}/{}.rotor".format(path, list_of_files[rotor-1]), 'r') 
        self = pickle.load(filehandler)
        return #End

    def random_rotor_setup(self, seed=None): 
        #Seed has to be added from the machine calling the function, where the seed is stored/generated
        if not seed:
            print("Something went wrong. Make sure development has reached this stage!")
        #They generate the same number if seed is unchanged, but we need hte seed change to remain constant, so:
        random.seed(seed) 
        self.define_position(random.randint(1,25))
        seed+=1
        random.seed(seed) 
        number_notches=random.randint(1,5)
        
        seed+=1
        random.seed(seed)
        print(random.random()) 
        #And we use this to generate numbers and lists of numbers from which to derive configurations, notches, positions and names
        #in the case of the connection board, an extra number should be used to determine number of connections.
        #self.jump=random.randint(1,26) for implementation


class REFLECTOR:
    def __init__(self):
        self
    #Easiest of all
def create_real_rotor(rotor_name):
    if rotor_name=="I":
        rotor=ROTOR
        return rotor
def import_rotor(filename):
    filehandler = open(filename, 'r') 
    object = pickle.load(filehandler)

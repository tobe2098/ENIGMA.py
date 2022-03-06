import random
import pickle
from ENIGMA_py.ROTOR import *
from ENIGMA_py.ENutils import *
from ENIGMA_py.REFLECTOR import *
class ENIGMAmachine:
    def __init__(self, name="name", seed=None):
        self.name=name
        #Include seed storages?
        #Write a default config
        self.rotor1=ROTOR()
        self.rotor2=ROTOR()
        self.rotor3=ROTOR()
        self.reflector=REFLECTOR()
        if not seed:
            #Number has to be big, but how
            self.seed=random.randint(0, 9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999) 
            print("Seed has been randomly generated, and is now:", self.seed)
        else:
            self.seed=seed
        #For now, default is nothingness
        self.board_config={letter:letter for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
    #Basic functions
    def name_seed(self):
        print(self.__repr__())
    def __repr__(self):
        print("Machine's name is:", self.name)
        print("Random seed of the machine is:", self.seed)
        return ("Machine name is %, and its random seed is %" % (self.name, self.seed))
    def change_name(self, new_name):
        self.name=new_name
        print("The machine's name is now:", self.name )
    def add_fourth_rotor(self):
        self.rotor4=ROTOR()
        print("Fourth rotor added. Use self.manual_rotor_setup or tune_current_machine(machine) to modify.")
    #Showing configs
    def show_rotor_config(self):
        pass #Complete after manual config
    def show_refl_config(self):
        pass
    def show_config(self):
        print("Board config:", simplify_board_config(self.board_config))
        print("Rotor configs:")
        self.show_rotor_config()
        print("Reflector config:")
        self.show_refl_config()
    #Manual configs
    def _all_rotor_setup(self, rotor=None):
        self.show_rotor_config()
        if rotor:
            rotor.configure()
            print(">>>Rotor setup finished, going back to selection")
            return
        i=0
        while i==0:
            choose=input("Do you want to use only the same rotors?[y/n]:")
            if choose=="y":
                self.tune_loaded_rotors()
                self.rotor_order_change()
                self.change_rletter_position()
                self.change_rotor_notches()
                return
            elif choose=="n":
                choose2=input("Do you want to import pre-existing rotors that are not in the machine?[y/n]:")
                if choose2=="y":
                    print("Choosing a rotor for first position:")
                    self.rotor1.import_rotor_config()           
                    print("Choosing a rotor for second position:")
                    self.rotor2.import_rotor_config()
                    print("Choosing a rotor for third position:")
                    self.rotor3.import_rotor_config()
                    if self.rotor4:
                        print("Choosing a rotor for fourth position:")
                        self.rotor4.import_rotor_config()
                elif choose2=="n":
                    print("Rotors will be generated and saved randomly, you can edit them later.")
                    self.generate_random_rotors()
        print(">>>Setup of rotors finished, going back to selection")
        return #Ended
    def manual_rotor_setup(self):
        i=0
        while i==0:
            accbool=input(">>>Input rotor number to configure the rotor (0 to exit, 5 to configure all):")
            if accbool==0:
                break
            elif accbool==1:
                self._all_rotor_setup(self.rotor1)
            elif accbool==2:
                self._all_rotor_setup(self.rotor2)
            elif accbool==3:
                self._all_rotor_setup(self.rotor3)
            elif accbool==4 and self.rotor4:
                self._all_rotor_setup(self.rotor4)
            elif accbool==5:
                self._all_rotor_setup()
        print(">>>Setup of rotors completed.")
    def manual_refl_setup(self):
        self.reflector.manual_reflector_config()
        return #End
    def manual_board_config(self):
        #Configuration of the cable board
        #PENDING: Make it stop after 26 letters have been assigned
        if self.board_config:
            print("Current board setup is:", simplify_board_config(self.board_config))
            accbool=input("Input N if you do NOT want to change the board setup:")
            if accbool=="N":
                return
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
    def manual_complete_config(self):
        #Board
        print(">>>Configurating the connection board:")
        self.manual_board_config()
        #Rotors
        print(">>>Configurating rotors:")
        self.manual_rotor_setup()
        #Reflector
        print(">>>Configurating reflector:")
        self.manual_refl_setup()
        #Name. IMPORTANT: name is used to save as pickled object. 
        #Not changing the name will overwrite previous machine with same name
        print("Machine is ready to go. Changing name is advised.")
        name=input("Input machine name (previous save with the same name will be overwritten):")
        self.change_name(name)
        self.save_machine()
    #Pickled functions
    def save_machine(self):
        pass
    def load_machine(self):
        pass
    #Intern setup functions
    def change_rletter_position(self):
        pos1=input("Letter position for rotor 1:")
        pos2=input("Letter position for rotor 2:")
        pos3=input("Letter position for rotor 3:")
        if self.rotor4:
            pos4=input("Letter position for rotor 4:")
            self.rotor4.define_position(pos4)
        self.rotor1.define_position(pos1)
        self.rotor2.define_position(pos2)
        self.rotor3.define_position(pos3)
        return "Rottor letter positions set"
    def rotor_order_change(self):
        i=0
        while i==0:
            print("Rotor 1:", self.rotor1.name)
            print("Rotor 2:", self.rotor2.name)
            print("Rotor 3:", self.rotor3.name)
            if self.rotor4:
                print("Rotor 4:", self.rotor4.name)
            selec=input("Select rotor to put in a placeholder to get swapped (0 to exit):")
            selec2=input("Select rotor to put placeholder's order position and complete swap:")
            if selec==0:
                print("Finished with swaps")
                return
            elif selec==1:
                placeh=self.rotor1
                if selec2==1:
                    print("Nothing happened")
                elif selec2==2:
                    self.rotor1=self.rotor2
                    self.rotor2=placeh
                elif selec2==3:
                    self.rotor1=self.rotor3
                    self.rotor3=placeh
                elif selec2==4 and self.rotor4:
                    self.rotor1=self.rotor4
                    self.rotor4=placeh
            elif selec==2:
                placeh=self.rotor2
                if selec2==1:
                    self.rotor2=self.rotor1
                    self.rotor1=placeh
                elif selec2==2:
                    print("Nothing happened")
                elif selec2==3:
                    self.rotor2=self.rotor3
                    self.rotor3=placeh
                elif selec2==4 and self.rotor4:
                    self.rotor2=self.rotor4
                    self.rotor4=placeh
            elif selec==3:
                placeh=self.rotor3
                if selec2==1:
                    self.rotor3=self.rotor1
                    self.rotor1=placeh
                elif selec2==2:
                    self.rotor3=self.rotor2
                    self.rotor2=placeh
                elif selec2==3:
                    print("Nothing happened")
                elif selec2==4 and self.rotor4:
                    self.rotor3=self.rotor4
                    self.rotor4=placeh
            elif selec==4 and self.rotor4:
                placeh=self.rotor4
                if selec2==1:
                    self.rotor4=self.rotor1
                    self.rotor1=placeh
                elif selec2==2:
                    self.rotor4=self.rotor2
                    self.rotor2=placeh
                elif selec2==3:
                    self.rotor4=self.rotor3
                    self.rotor4=placeh
                elif selec2==4 and self.rotor4:
                    print("Nothing happened")

    def change_rotor_notches(self):
        #First rotor
        notchlist=[chr(i+64) for i in self.rotor1.notch]
        print("Rotor 1 notches:", notchlist)
        new_notches=input("Input new notches in a single string, e.g. ADF")
        self.rotor1.define_notches(new_notches)
        #Second rotor
        notchlist=[chr(i+64) for i in self.rotor2.notch]
        print("Rotor 2 notches:", notchlist)
        new_notches=input("Input new notches in a single string, e.g. ADF")
        self.rotor2.define_notches(new_notches)
        #Third rotor
        notchlist=[chr(i+64) for i in self.rotor3.notch]
        print("Rotor 3 notches:", notchlist)
        new_notches=input("Input new notches in a single string, e.g. ADF")
        self.rotor3.define_notches(new_notches)
        #Fourth rotor
        if self.rotor4:
            notchlist=[chr(i+64) for i in self.rotor4.notch]
            print("Rotor 4 notches:", notchlist)
            new_notches=input("Input new notches in a single string, e.g. ADF")
            self.rotor4.define_notches(new_notches)
    def tune_loaded_rotors(self):
        print("Configurating rotor 1 connections:")
        self.rotor1.customize_connections()
        print("Configurating rotor 2 connections:")
        self.rotor2.customize_connections()
        print("Configurating rotor 3 connections:")
        self.rotor3.customize_connections()
        if self.rotor4:
            print("Configurating rotor 4 connections:")
            self.rotor4.customize_connections()
        print("All connections configurated")
        return
    def tune_loaded_reflector(self):
        pass
    #RNG functions
    def generate_random_rotors(self):
        pass
    def randomize_board_config(self):
        pass
    def random_machine(self):
        #Use seed to generate the seed intervals between rotors, between 1 and 30?
        self.seed #This exists
        pass
    #Finally, the crypt function
    def encrypt_decrypt(self):
        print(">>>Every time you write a message, the machine will return to the configuration it is now. \n>>>WARNING: Do NOT use spaces, please.")
        for char in input('>>>Write Text: ').upper():
            print(char)
            number=(ord(char) - 64)
        #Not finished


def tune_existing_machine(machine):
    pass
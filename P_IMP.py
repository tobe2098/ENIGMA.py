from ROTOR import ROTOR
from REFLECTOR import REFLECTOR
import pickle
import random
#Look into installation of the module
def create_real_rotor(rotor_name):
    #Scripted creation of Wermacht rotors
    if rotor_name=="I":
        rotor=ROTOR
        return rotor
def import_rotor(filename): 
    # Import all available rotors into a list? Or just return a rotor from the saved ones?
    filehandler = open(filename, 'r') 
    object = pickle.load(filehandler)
def seed_list_show():
    pass #.txt with a list of seeds and attached non-related names?
    def import_rotor_list(self):
        return #list_of_rotors
        #Not finished, for ENIGMA_py.py
'''
#on positions: Also, change 26 by the notches
self.alpha.position+=self.alpha.jump
if self.alpha.position % 26==0:
    self.beta.position +=1
    self.alpha.position=0
    if self.beta.position % 26==0:
        self.beta.position=0
        self.gamma.position+=1
        '''
#Put better character prints so that it looks more aesthetic
#Put print("\a") somewhere? Does not work
#In case pickling does not work: "a" is for appending, "w" for writing, "b" for binary
# with open('mypickle.pickle', 'wb') as f:
#    pickle.dump(some_obj, f)

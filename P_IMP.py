from ROTORS import ROTOR
import pickle
def create_real_rotor(rotor_name):
    #Scripted creation of Wermacht rotors
    if rotor_name=="I":
        rotor=ROTOR
        return rotor
def import_rotor(filename): 
    # Import all available rotors into a list? Or just return a rotor from the saved ones?
    filehandler = open(filename, 'r') 
    object = pickle.load(filehandler)

def save_n_random_rotors(seed):
    #Create and save into pickle objects 20 randomly generated rotors. Use seed to generate new seed, or simply add numbers
    pass
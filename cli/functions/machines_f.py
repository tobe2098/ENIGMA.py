from platform import machine
from re import S
from cli.functions.plugboards_f import _reset_and_randomize_connections_pb, _show_config_pb
from cli.functions.reflectors_f import _reset_and_randomize_connections_rf, _show_config_rf
from cli.functions.rotors_f import _randomize_notches_rt, _randomize_position_rt, _reset_and_randomize_connections_rt, _show_config_rt
from utils.utils import is_valid_seed
from utils.utils_cli import askingInput, checkInputValidity, getSeedFromUser, printListOfOptions, printOutput, returningToMenu
from ...core import machines
import pandas as pd

import copy
# ALL MENUS MUST BE ABLE TO RETURN TO THE PREVIOUS MENU WITH THE SAME KEY
# ALL LOADING FUNCTIONS MUST BE HERE
# PUT A FUNCTION THAT SAVES EACH INDIVIDUAL COMPONENT (EXCEPT THE PLUGBOARDS (AND ROTOR POSITIONS) FOR SAFETY PURPOSES)
def _show_full_config_machine(machine_ref:machines.Machine):
    printOutput("Plugboard config:")
    _show_config_pb(machine_ref._plugboard)
    for i in range(len(machine_ref._rotors)):
        printOutput(f"Rotor {i+1} config:")
        _show_config_rt(machine_ref._rotors[i])
    printOutput("Reflector config:")
    _show_config_rf(machine_ref._reflector)


def _show_simple_config_machine(machine_ref: machines.Machine):
    config = pd.DataFrame()
    config["Rotor position"] = list(range(1, len(machine_ref._rotors))+1)
    config["Rotors"] = [rotor.get_name() for rotor in machine_ref._rotors]
    config["Letter position"] = [rotor._position for rotor in machine_ref._rotors]
    config["Notches"] = [rotor.get_notchlist_characters() for rotor in machine_ref._rotors]
    printOutput("Plugboard config:")
    _show_config_pb(machine_ref._plugboard)
    printOutput("Reflector:", machine_ref._reflector.get_name())
    printOutput("Rotor config:")
    print(config)
    printOutput("Machine name:", machine_ref.get_name())



def _random_setup_single_rotor_machine(machine_ref:machines.Machine):
    printListOfOptions([rotor.get_name() for rotor in machine_ref._rotors])
    rotor_index=askingInput("Input the rotor number (0 to n-1)")
    rotor_index=checkInputValidity(rotor_index,int,range(len(machine_ref._rotors)))
    if rotor_index:    
        _reset_and_randomize_connections_rt(machine_ref._rotors[rotor_index])
        _randomize_position_rt(machine_ref._rotors[rotor_index])
        _randomize_notches_rt(machine_ref._rotors[rotor_index])
    else:
        returningToMenu("Invalid index",output_type='e')
    
def _random_setup_reflector_machine(machine_ref:machines.Machine):
    printOutput("Careful with your seed choice, if you use the same one you get the same results")
    seed=getSeedFromUser()
    machine_ref._reflector._randomize_dictionaries(seed)

def _random_setup_reflector_global_seed_machine(machine_ref:machines.Machine):
    if machine_ref.get_seed()==0:
        returningToMenu("No global seed has been set",output_type='e')
    machine_ref._reflector._randomize_dictionaries(machine_ref.get_seed())


def _set_a_global_seed_machine(machine_ref:machines.Machine):
    printOutput("Be aware that your general machine setup is not randomized after you set this seed.")
    seed=getSeedFromUser()
    if not is_valid_seed(seed):
        returningToMenu("Not a valid seed", 'e')
    machine_ref._change_seed(seed=seed)

def _random_setup_all_rotors_machine(machine_ref:machines.Machine):
    if machine_ref.get_seed()==0:
        returningToMenu("No global seed has been set",output_type='e')
    jump=getSeedFromUser("seed jump")
    machine_ref._random_setup_all_rotors(jump=jump)


def _set_new_no_blank_rotors_machine(self, noRotors):
    askingInput("")
    
    self._rotors = [copy.copy(self._ref_rotor) for _ in range(noRotors)]


def _append_rotors(self, noRotors):
    for _ in range(noRotors):
        self._rotors.append(copy.copy(self._ref_rotor))


def _change_rotor_character_position(self):
    # MENU in machine!!! LETTERS HAVE TO BE FROM THE LIST!!!
    pos1 = input(">>>Letter position for rotor 1:")
    pos2 = input(">>>Letter position for rotor 2:")
    pos3 = input(">>>Letter position for rotor 3:")
    if self.rotor4:
        pos4 = input(">>>Letter position for rotor 4:")
        self.rotor4._define_position(pos4)
    self.rotor1._define_position(pos1)
    self.rotor2._define_position(pos2)
    self.rotor3._define_position(pos3)
    print(">Rottor character positions set")


def _rotor_order_change(self):
    while True:
        for i in range(len(self._rotors)):
            print(">Rotor {}:".format(i + 1), self._rotors[i].get_name())
        selec1 = input(
            ">>>Select rotor to put in a placeholder to get swapped (-1 to exit):"
        )
        selec2 = input(
            ">>>Select rotor to put placeholder's order position and complete swap:"
        )

        if selec1 == -1:
            print(">Finished with swaps")
            return
        else:
            selec1 -= 1
            selec2 -= 1
            self._rotors[selec1], self._rotors[selec2] = (
                self._rotors[selec2],
                self._rotors[selec1],
            )


def _edit_a_rotors_config(self):  ## This is just a menu call
    for i in range(len(self._rotors)):
        print(">Configurating rotor {} connections:".format(i))
        self._rotors[i].customize_connections()


def _edit_reflector_config(machine_ref: machines.Machine):
    pass


def _edit_plugboard_config(machine_ref: machines.Machine):
    pass


def encrypt_decrypt(self):
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


##import pickle
# class Foo(object):
#     pass
# foo = Foo()
# bar = Foo()
# bar.foo_ref = foo
# with open('tmp.pkl', 'wb') as f:
#     pickle.dump((foo, bar), f)
# with open('tmp.pkl', 'rb') as f:
#     foo2, bar2 = pickle.load(f)

# print id(foo) == id(bar.foo_ref) # True
# print id(foo2) == id(bar2.foo_ref) # True


def load_machine(
    self,
):  # THIS LOAD FUNCTION IS DEPRECATED, IT DOES NOT WORK, USE THE ONE THAT IS NOT CLASS DEFINED
    # THE FUNCTION MUST DEAL WITH THE STORED OBJECTS IN ORDER LOOK STACK OVERFLOW
    current_path = os.path.dirname(__file__)
    new_folder = utils.MACHINES_FILE_HANDLE
    path = os.path.join(current_path, new_folder)
    if not os.path.exists(path):
        print("There is no {} folder".format(path))
        return
    list_of_files = [element.rsplit((".", 1)[0])[0] for element in os.listdir(path)]
    if len(list_of_files) == 0:
        print("There are no machines saved")
        return
    print("Your available machines are:")
    for i in list_of_files:
        print(i)
    machine = int(input("Input machine's position in the list:"))
    file = os.path.join(path, "{}.machine".format(list_of_files[machine - 1]))
    filehandler = open(file, "rb")
    self = pickle.load(filehandler)
    filehandler.close()
    # return self  # End


def load_existing_machine():
    current_path = os.path.dirname(__file__)
    new_folder = utils.MACHINES_FILE_HANDLE
    path = os.path.join(current_path, new_folder)
    if not os.path.exists(path):
        print(">There is no {} folder".format(path))
        return
    list_of_files = [element.rsplit((".", 1)[0])[0] for element in os.listdir(path)]
    if len(list_of_files) == 0:
        print(">There are no machines saved")
        return
    print(">Your available machines are:")
    for i in list_of_files:
        print(i)
    machine = int(input(">>>Input machine's position in the list:"))
    file = os.path.join(path, "{}.machine".format(list_of_files[machine - 1]))
    filehandler = open(file, "rb")
    machine = pickle.load(filehandler)
    filehandler.close()
    return machine


def setup_random_machine(self):
    print(">Randomly generating your ENIGMA machine:")
    noRotors = "a"
    while not isinstance(noRotors, int):
        noRotors = input(">>>Input the number of rotors:")
        if noRotors > MAX_NO_ROTORS:
            noRotors = ""
            print(
                "Maximum number of rotors allowed is {} (for your own good)".format(
                    MAX_NO_ROTORS
                )
            )


def save_machine(self):
    # Research on how to pickle and unpickle member custom classes
    while self._name.strip() == "name" or self._name.strip() == "":
        self._name = input(">>>Please assign a new name to the machine:")
    current_path = os.path.dirname(__file__)
    new_folder = utils.MACHINES_FILE_HANDLE
    path = os.path.join(current_path, new_folder)
    if not os.path.exists(path):
        os.mkdir(path)
        print("Directory '% s' created" % path)
    save_file = open(r"{}/{}.machine".format(path, self._name), "wb")
    pickle.dump(self, save_file)
    print(
        "{} has been saved into {}.machine in {}".format(self._name, self._name, path)
    )
    save_file.close()
    # return  # End

    def manual_complete_config(self):
        # MENU HERE TOO
        raise Exception
        # Board
        print(">Configurating the connection board:")
        self._plugboard.manual_board_setup()
        # Rotors
        print(">Configurating rotors:")
        self._manual_rotor_setup()
        # Reflector
        print(">Configurating reflector:")
        self._reflector.configure()
        # Name. IMPORTANT: name is used to save as pickled object.
        # Not changing the name will overwrite previous machine with same name
        print(">Machine is ready to go. Changing name is advised")
        name = input(
            ">>>Input machine name (previous save with the same name will be overwritten):"
        )
        self.change_name(name)
        self.save_machine()

    def _all_rotor_setup(self):
        self.show_rotor_config()
        raise Exception
        # Maybe client no-gui? Remove editors from here then, bc not compatible with GUI
        # NEED A FULL MENU HERE, WITH ADD R/C/L, REMOVE, RESET AND RANDOMIZE, RESET AND CONFIGURE, LOAD ROTORS IN PLACE
        print(">The machine currently has {} rotors".format(len(self._rotors)))
        self._append_rotors(input(">>>Number of rotors to add? "))
        # while True:
        choose = input(">>>Do you want to use only the same rotors?[y/n]:")
        if choose == "y":
            self._tune_loaded_rotors()
            self._rotor_order_change()
            self._change_rotor_character_position()
            self._change_rotor_notches()
        elif choose == "n":
            choose2 = input(
                ">>>Do you want to import pre-existing rotors that are not in the machine?[y/n]:"
            )
            if choose2 == "y":
                for i in range(input(">>>Input desired number of rotors: ")):
                    print(">Choosing a rotor for position no. {}:".format(i))
                    self._rotors[i].import_rotor()
            elif choose2 == "n":
                print(
                    ">Rotors will be generated and saved randomly, you can edit them later."
                )
                self.generate_random_rotors()
        print(">Setup of rotors finished, going back to selection")

    def show_rotor_config(self):
        print(">ROTORS START")
        for i in range(len(self._rotors)):
            print(">Rotor no. {}:".format(i + 1))
            self._rotors[i].show_config()
        print(">ROTORS END")

    def import_rotor(self):
        current_path = os.path.dirname(__file__)
        new_folder = utils.ROTORS_FILE_HANDLE
        path = os.path.join(current_path, new_folder)
        if not os.path.exists(path):
            print("There is no {} folder".format(path))
            return
        list_of_files = [element.rsplit((".", 1)[0])[0] for element in os.listdir(path)]
        if len(list_of_files) == 0:
            print("There are no rotors saved")
            return
        print("Your available rotors are: {}".format(list_of_files))
        rotor = input("Input rotor's position in the list:")
        filehandler = open(r"{}\\{}.rotor".format(path, list_of_files[rotor - 1]), "rb")
        self = pickle.load(filehandler)
        filehandler.close()

    def import_reflector(self):
        current_path = os.path.dirname(__file__)
        new_folder = utils.REFLECTORS_FILE_HANDLE
        path = os.path.join(current_path, new_folder)
        if not os.path.exists(path):
            print(">There is no {} folder".format(path))
            return
        list_of_files = [element.rsplit((".", 1)[0])[0] for element in os.listdir(path)]
        if len(list_of_files) == 0:
            print(">There are no reflectors saved")
            return
        print(">Your available reflectors are: {}".format(list_of_files))
        reflector = input(">>>Input reflector's position in the list:")
        filehandler = open(
            r"{}\\{}.reflector".format(path, list_of_files[reflector - 1]), "rb"
        )
        self = pickle.load(filehandler)


def generate_n_random_reflectors(n, seed: int):
    # Create and save into pickle objects 20 randomly generated rotors. Use seed to generate new seed, or simply add numbers
    for index in range(0, n):
        reflector = reflector.Reflector()
        reflector.random_name(seed + index)
        reflector.random_setup(seed + index)
    utils_cli.printOutput(f"Created and saved {n} rotors.")

from hmac import new
from platform import machine
from cli.functions.plugboards_f import _show_config_pb
from cli.functions.reflectors_f import  _show_config_rf
from cli.functions.rotors_f import _randomize_notches_rt, _randomize_position_rt, _reset_and_randomize_connections_rt, _show_config_rt
from utils.utils import Constants, is_valid_seed
from utils.utils_cli import askingInput, checkInputValidity, getSeedFromUser, printListOfOptions, printOutput, printWarning, returningToMenu
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
    # printOutput("Careful with your seed choice, if you use the same one you get the same results")
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
        returningToMenu("Not a valid seed", output_type='e')
    machine_ref._change_seed(seed=seed)

def _random_setup_all_rotors_machine(machine_ref:machines.Machine):
    if machine_ref.get_seed()==0:
        returningToMenu("No global seed has been set",output_type='e')
    jump=getSeedFromUser("seed jump")
    machine_ref._random_setup_all_rotors(jump=jump)

def _randomize_entire_machine(machine_ref:machines.Machine):
    printWarning("The previous global seed will be replaced by the seed you input")
    seed=getSeedFromUser()
    no_rotors=askingInput("Input desired number of rotors (invalid for same number)")
    no_rotors=checkInputValidity(no_rotors, int, range(1,Constants.MAX_NO_ROTORS))
    machine_ref.setup_machine_randomly(seed, no_rotors or machine_ref.get_no_rotors())

def _re_randomize_with_global_seed_machine(machine_ref:machines.Machine):
    if machine_ref.get_seed()==0:
        returningToMenu("No global seed has been set",output_type='e')
    machine_ref.setup_machine_randomly(machine_ref.get_seed(),machine_ref.get_no_rotors())

def _set_new_no_blank_rotors_machine(machine_ref:machines.Machine):
    new_no_rotors=askingInput(f"Enter number of new rotors to set in the machine (0 to {Constants.MAX_NO_ROTORS})")
    new_no_rotors=checkInputValidity(new_no_rotors, int, range(1, Constants.MAX_NO_ROTORS+1))
    if new_no_rotors:
        machine_ref._set_new_no_rotors(new_no_rotors)
    else:
        returningToMenu("Invalid input or input is zero",output_type='e')
    
def _append_rotors(machine_ref:machines.Machine):
    if machine_ref.get_no_rotors()==Constants.MAX_NO_ROTORS:
        returningToMenu("You reached the maximum number of rotors. Why would you do such a thing?","e")
    no_rotors_append=askingInput(f"Enter number of new rotors to append to the machine (0 to {Constants.MAX_NO_ROTORS-machine_ref.get_no_rotors()})")
    no_rotors_append=checkInputValidity(no_rotors_append, int, range(1, Constants.MAX_NO_ROTORS-machine_ref.get_no_rotors()+1))
    if no_rotors_append:
        machine_ref._append_rotors(no_rotors_append)
    else:
        returningToMenu("Invalid input or input is zero",output_type='e')
    

def _load_rotors_at_index(machine_ref:machines.Machine):
    if machine_ref.get_no_rotors()==Constants.MAX_NO_ROTORS:
        returningToMenu("You reached the maximum number of rotors. Why would you do such a thing?","e")
    index=askingInput(f"Choose a valid index where to insert new rotors (0 to {machine_ref.get_no_rotors()-1})")
    index=checkInputValidity(index, int, range(0,machine_ref.get_no_rotors()-1))
    # no_rotors_insert=askingInput(f"Enter number of new rotors to append to the machine (1 to {Constants.MAX_NO_ROTORS-machine_ref.get_no_rotors()})")
    # no_rotors_insert=checkInputValidity(no_rotors_insert, int, range(1, Constants.MAX_NO_ROTORS-machine_ref.get_no_rotors()+1))
    if index:
        machine_ref._load_a_rotor_on_index(index)
    else:
        returningToMenu("Invalid index input",output_type='e')
    

def _change_all_rotors_character_position(machine_ref:machines.Machine):
    # MENU in machine!!! LETTERS HAVE TO BE FROM THE LIST!!!
    printOutput("You can skip the change of character of a rotor by giving any invalid input")
    new_positions=[]
    printListOfOptions(machine_ref.get_rotors_names_ordered())
    for i in range(machine_ref.get_no_rotors()):
        remaining = list(set(machine_ref) - set(new_positions))
        printOutput("Remaining positions are ",remaining)
        new_pos=askingInput(f"Input new position for rotor {i+1}")
        new_pos=checkInputValidity(new_pos, _range=machine_ref._characters_in_use)
        while new_pos not in remaining:
            printOutput("Remaining positions are ",remaining)
            new_pos=askingInput(f"Input new position for rotor {i+1}")
            new_pos=checkInputValidity(new_pos, _range=machine_ref._characters_in_use)
        new_positions.append(new_pos)
    positions_copy = copy.copy(new_positions)
    positions_copy.sort()
    if all(
            [machine.is_rotor_index_valid(idx) for idx in new_positions]
        ) and positions_copy == list(range(machine_ref.get_no_rotors())):
        machine_ref._reorder_all_rotors(position_list=new_positions)
    else:
        returningToMenu("The positions you provided were not valid",output_type='e')

def _change_a_rotor_character_position(machine_ref:machines.Machine):
    pass

def _swap_two_rotors():
def _reorder_all_rotors():



def _rotor_order_change(machine_ref):
    while True:
        for i in range(len(machine_ref._rotors)):
            print(">Rotor {}:".format(i + 1), machine_ref._rotors[i].get_name())
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
            machine_ref._rotors[selec1], machine_ref._rotors[selec2] = (
                machine_ref._rotors[selec2],
                machine_ref._rotors[selec1],
            )


def _edit_a_rotors_config(machine_ref):  ## This is just a menu call
    for i in range(len(machine_ref._rotors)):
        print(">Configurating rotor {} connections:".format(i))
        machine_ref._rotors[i].customize_connections()


def _edit_reflector_config(machine_ref: machines.Machine):
    pass


def _edit_plugboard_config(machine_ref: machines.Machine):
    pass


def encrypt_decrypt(machine_ref):
    CALL FOR CHECKS OF PROPER SETUP IN PLACE (AT LEAST ALL REFLECTOR CONNECTED, AT LEAST 1 ROTOR, AT LEAST ONE NOTCH PER ROTOR, SAVED MACHINE)
    THIS SHOULD ONLY ENCRYPT A PASSED TEXT, AND A LETTER BY LETTER (FOR GUI)
    # import copy as cp
    print(
        ">Every time you write a message, the machine will return to the configuration it is now. \n>WARNING: Do NOT use spaces, please.\n >>>If you want to stop, press Enter with no input."
    )

    # machine_ref.simple_show_config()
    input_var = 1
    while input_var:
        # message_length = 0
        input_var = input(
            ">>>Write Text (only allowed characters will be encrypted): "
        ).upper()
        output_message_list = []
        # print(machine_ref.rotor1._position)


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
    machine_ref,
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
    machine_ref = pickle.load(filehandler)
    filehandler.close()
    # return machine_ref  # End


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


def setup_random_machine(machine_ref):
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


def save_machine(machine_ref):
    # Research on how to pickle and unpickle member custom classes
    while machine_ref._name.strip() == "name" or machine_ref._name.strip() == "":
        machine_ref._name = input(">>>Please assign a new name to the machine:")
    current_path = os.path.dirname(__file__)
    new_folder = utils.MACHINES_FILE_HANDLE
    path = os.path.join(current_path, new_folder)
    if not os.path.exists(path):
        os.mkdir(path)
        print("Directory '% s' created" % path)
    save_file = open(r"{}/{}.machine".format(path, machine_ref._name), "wb")
    pickle.dump(machine_ref, save_file)
    print(
        "{} has been saved into {}.machine in {}".format(machine_ref._name, machine_ref._name, path)
    )
    save_file.close()
    # return  # End

    def manual_complete_config(machine_ref):
        # MENU HERE TOO
        raise Exception
        # Board
        print(">Configurating the connection board:")
        machine_ref._plugboard.manual_board_setup()
        # Rotors
        print(">Configurating rotors:")
        machine_ref._manual_rotor_setup()
        # Reflector
        print(">Configurating reflector:")
        machine_ref._reflector.configure()
        # Name. IMPORTANT: name is used to save as pickled object.
        # Not changing the name will overwrite previous machine with same name
        print(">Machine is ready to go. Changing name is advised")
        name = input(
            ">>>Input machine name (previous save with the same name will be overwritten):"
        )
        machine_ref.change_name(name)
        machine_ref.save_machine()

    def _all_rotor_setup(machine_ref):
        machine_ref.show_rotor_config()
        raise Exception
        # Maybe client no-gui? Remove editors from here then, bc not compatible with GUI
        # NEED A FULL MENU HERE, WITH ADD R/C/L, REMOVE, RESET AND RANDOMIZE, RESET AND CONFIGURE, LOAD ROTORS IN PLACE
        print(">The machine currently has {} rotors".format(len(machine_ref._rotors)))
        machine_ref._append_rotors(input(">>>Number of rotors to add? "))
        # while True:
        choose = input(">>>Do you want to use only the same rotors?[y/n]:")
        if choose == "y":
            machine_ref._tune_loaded_rotors()
            machine_ref._rotor_order_change()
            machine_ref._change_rotor_character_position()
            machine_ref._change_rotor_notches()
        elif choose == "n":
            choose2 = input(
                ">>>Do you want to import pre-existing rotors that are not in the machine?[y/n]:"
            )
            if choose2 == "y":
                for i in range(input(">>>Input desired number of rotors: ")):
                    print(">Choosing a rotor for position no. {}:".format(i))
                    machine_ref._rotors[i].import_rotor()
            elif choose2 == "n":
                print(
                    ">Rotors will be generated and saved randomly, you can edit them later."
                )
                machine_ref.generate_random_rotors()
        print(">Setup of rotors finished, going back to selection")

    def show_rotor_config(machine_ref):
        print(">ROTORS START")
        for i in range(len(machine_ref._rotors)):
            print(">Rotor no. {}:".format(i + 1))
            machine_ref._rotors[i].show_config()
        print(">ROTORS END")

    def import_rotor(machine_ref):
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
        machine_ref = pickle.load(filehandler)
        filehandler.close()

    def import_reflector(machine_ref):
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
        machine_ref = pickle.load(filehandler)


def generate_n_random_reflectors(n, seed: int):
    # Create and save into pickle objects 20 randomly generated rotors. Use seed to generate new seed, or simply add numbers
    for index in range(0, n):
        reflector = reflector.Reflector()
        reflector.random_name(seed + index)
        reflector.random_setup(seed + index)
    utils_cli.printOutput(f"Created and saved {n} rotors.")

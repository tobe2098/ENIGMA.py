from ...core import machines


# ALL MENUS MUST BE ABLE TO RETURN TO THE PREVIOUS MENU WITH THE SAME KEY
# ALL LOADING FUNCTIONS MUST BE HERE
# PUT A FUNCTION THAT SAVES EACH INDIVIDUAL COMPONENT (EXCEPT THE PLUGBOARDS (AND ROTOR POSITIONS) FOR SAFETY PURPOSES)
def _random_conf_rotors(self, jump):
    for i in range(len(self._rotors)):
        self._rotors[i].random_setup(self._seed + jump, showConfig=False)
        jump += 1
    return ">Rotors and reflector set up and saved."


def _set_new_no_rotors(self, noRotors):
    self._rotors = [copy.copy(self._ref_rotor) for _ in range(noRotors)]


def _append_rotors(self, noRotors):
    for _ in range(noRotors):
        self._rotors.append(copy.copy(self._ref_rotor))


def _tune_loaded_rotors(self):  ## This is just a menu call
    for i in range(len(self._rotors)):
        print(">Configurating rotor {} connections:".format(i))
        self._rotors[i].customize_connections()


def _change_rotor_letter_position(self):
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
    print(">Rottor letter positions set")


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
    pass


def save_machine():
    pass

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
            self._change_rotor_letter_position()
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

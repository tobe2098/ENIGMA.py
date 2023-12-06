from ...core import rotors


## New seeds for standalone generated rotors, reflectors and boards
### EACH OBJECT SET OF MENUS TAKES THE REFERENCE FROM THE MACHINE, AND THEN OPERATES ON IT, EFFECTIVELY NOT TOUCHING THE MACHINE ITSELF BUT ITS OBJECTS
### EXCEPT FOR LOADING!!!!!! LOADING OF ITEMS HAS TO BE DONE DIRECTLY IN THE MACHINE MENU
### ALSO EXCEPT ALL GENERALISTIC CONFIG CALLS
# Intern setup functions
def _change_rotor_letter_position(self):
    # MENU
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


def _change_rotor_notches(self):
    for i in range(len(self._rotors)):
        print(">Rotor {} notches:", self._rotors[i].get_notchlist())
        self._rotors[i]._define_notches(input(">>>Input new notches(empty to skip):"))


def _tune_loaded_rotors(self):
    for i in range(len(self._rotors)):
        print(">Configurating rotor {} connections:".format(i))
        self._rotors[i].customize_connections()


# RNG functions
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

    # def add_a_rotor(self):
    #     self.rotor4=Rotor()
    #     self.n_rotors=4
    #     print(">>>Fourth rotor added. Use self.rotor4.manual_rotor_setup() to modify or self.rotor4.random_rotor_setup()")
    # Showing configs
    def show_rotor_config(self):
        print(">ROTORS START")
        for i in range(len(self._rotors)):
            print(">Rotor no. {}:".format(i + 1))
            self._rotors[i].show_config()
        print(">ROTORS END")

    def show_single_rotor_config(self, rotor_no):
        print(">Rotor no. {}:".format(rotor_no))
        self._rotors[rotor_no - 1].show_config()

    def _manual_rotor_setup(self):
        while True:
            raise Exception
            # NEED A FULL MENU HERE, WITH ADD R/C/L, REMOVE, RESET AND RANDOMIZE, RESET AND CONFIGURE, LOAD ROTORS IN PLACE

            actionEnum = (
                input(
                    ">>>Input rotor number to configure the rotor (press 0 to configure all, any higher number to abort):"
                )
                - 1
            )
            if actionEnum == -1:
                self._all_rotor_setup()
            elif actionEnum < len(self._rotors):
                self._single_rotor_setup(self._rotors[actionEnum])
            else:
                break
        print(">Setup of rotors completed.")

    def customize_connections(self):
        entry_seen_letters = []
        exit_seen_letters = []
        if self._forward_dict and self._backward_dict:
            print(">Current setup is:")
            print(">Forward connections in the rotor:", self._forward_dict)
            print(">Backward connections in the rotor:", self._backward_dict)
            accbool = input(
                ">>>Input N if you do not want to change the configuration:"
            )
            if accbool == "N":
                return
        entry_rotor_dict = dict(zip(self._characters_in_use, self._characters_in_use))
        exit_rotor_dict = dict(zip(self._characters_in_use, self._characters_in_use))
        entry_list = copy.copy(self._characters_in_use)
        exit_list = copy.copy(self._characters_in_use)
        while True:
            print(">If you want to stop configurating the rotor, press Enter")
            configpair = input(
                ">>>Enter pair of letters for board configuration:"
            ).upper()
            if configpair.isalpha() or not configpair:
                pass
            else:
                print(">Error: Input 2 letters please")
                continue
            if len(list(set(entry_list) - set(entry_seen_letters))) == 0:
                break
            configpair = list(configpair)
            if len(configpair) == 2:
                pass
            elif len(configpair) == 0:
                break
            else:
                print(">Error: Input 2 letters please")
                continue
            if any(map(lambda v: v in configpair, entry_seen_letters)):
                print(">Already plugged")
                continue
            if any(map(lambda v: v in configpair, exit_seen_letters)):
                print(">Already plugged")
                continue
            else:
                entry_seen_letters.append(configpair[0])
                exit_seen_letters.append(configpair[1])
                entry_rotor_dict[configpair[0]] = configpair[1]
                exit_rotor_dict[configpair[1]] = configpair[0]
            print(">Current entry config:\n", simplify_board_dict(entry_rotor_dict))
            print(">Current exit config:\n", simplify_board_dict(exit_rotor_dict))
            print(
                ">Not connected entry letters:\n",
                list(set(entry_list) - set(entry_seen_letters)),
            )
            print(
                ">Not connected exit letters:\n",
                list(set(exit_list) - set(exit_seen_letters)),
            )
        self._forward_dict = entry_rotor_dict
        self._backward_dict = exit_rotor_dict
        self._update_dicts()
        print(">Finished")

    def configure(self):
        print("Press Enter with no input to skip configuration of the parameter.")
        name = input("Write the rotor's name:").upper()
        position = input("Write the rotor's position (in letters, only 1):").upper()
        print("For your cryptosecurity, input between 1 and 5 notches, not more.")
        notch = list(input("Write the rotor's notch position/s (in letters):").upper())
        # jump=int(input("Write the position jump per letter (in a single number) * [0<x<26]:"))
        while boolean not in list("y", "n"):
            boolean = input(
                "Do you want to configure the connections of the rotor?[y/n]"
            )
        if name:
            self._change_name(name)
        # if jump<26:
        #     self.define_rotor_jump(jump)
        if position in self._characters_in_use:
            self._define_position(position)
        if set(notch).issubset(
            self._characters_in_use
        ):  # DO this every time you want to check if set a is a subset of set b
            self._define_notches(notch)
        if boolean == "y":
            self.customize_connections()
        self.show_config()
        print(
            "You have finished configuring your rotor. If you want to save it in a file, use self.export_rotor() \n*Careful while defining notches"
        )


def save_n_random_rotors(n, seed):
    for i in range(0, n):
        rotor = Rotor()
        rotor.random_setup(seed + i)
    return ">Done"


def tune_existing_rotor():
    rotor = Rotor()
    rotor.import_rotor()
    rotor.configure()
    rotor.export_rotor()
    return ">Rotor was edited and saved"

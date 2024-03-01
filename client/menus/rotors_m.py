from ...core import machines
from ...core import rotors
from ...utils import utils_cli
from ..functions import rotors_f
import os


_menu_rotor_name_options = {
    "1": ("Change name", rotors_f._change_rotor_name_rt),
    "2": ("Randomize name", rotors_f._randomize_name_rt),
    "0": ("Exit menu", utils_cli.exitMenu),
}


_menu_rotor_connections_options = {
    "1": ("Delete a single connection", rotors_f._choose_connection_to_delete_rt),
    "2": ("Create a single connection", rotors_f._create_a_connection_single_choice_rt),
    "3": ("Form all connections left", rotors_f._form_all_connections_rt),
    "0": ("Exit menu", utils_cli.exitMenu),
}

_menu_rotor_reset_options = {
    "1": (
        "Reset and form max. connections",
        rotors_f._reset_and_streamline_connections_by_pairs_rt,
    ),
    "2": (
        "Reset and randomize connections",
        rotors_f._reset_and_randomize_connections_rt,
    ),
    "3": ("Reset connections", rotors_f._reset_connections_rt),
    "0": ("Exit menu", utils_cli.exitMenu),
}

_menu_rotor_saved_rotor = {
    "1": ("Save rotor", rotors_f._save_in_current_directory_rt),
    "2": ("Change rotor name", rotors_f._change_rotor_name_rt),
    "3": ("Delete a single connection", rotors_f._choose_connection_to_delete_rt),
    "4": ("Create a single connection", rotors_f._create_a_connection_single_choice_rt),
    "5": ("Form all connections left", rotors_f._form_all_connections_rt),
    "6": (
        "Reset and form max. connections",
        rotors_f._reset_and_streamline_connections_by_pairs_rt,
    ),
    "7": (
        "Reset and randomize connections",
        rotors_f._reset_and_randomize_connections_rt,
    ),
    "8": ("Reset connections", rotors_f._reset_connections_rt),
    "0": ("Exit menu", utils_cli.exitMenu),
}


def _name_rotor_menu(rotor_ref: rotors.Rotor):
    while True:

        rotors_f._print_name_rt(rotor_ref)
        try:
            for key in sorted(_menu_rotor_name_options.keys()):
                utils_cli.printMenuOption(key + ":" + _menu_rotor_name_options[key][0])

            answer = str(input(utils_cli.askForMenuOption()))
            _menu_rotor_name_options.get(answer, [None, utils_cli.invalidChoice])[1](
                rotor_ref
            )
        except utils_cli.ReturnToMenuException:
            print(utils_cli.ReturnToMenuException.message)
        except utils_cli.MenuExitException:
            utils_cli.clearScreenSafety()
            utils_cli.exitMenu()


def _connections_rotor_menu(rotor_ref: rotors.Rotor):
    while True:
        try:
            rotors_f._show_config_rt(rotor_ref)
            for key in sorted(_menu_rotor_connections_options.keys()):
                utils_cli.printMenuOption(
                    key + ":" + _menu_rotor_connections_options[key][0]
                )

            answer = str(input(utils_cli.askForMenuOption()))
            _menu_rotor_connections_options.get(
                answer, [None, utils_cli.invalidChoice]
            )[1](rotor_ref)
        except utils_cli.ReturnToMenuException:
            print(utils_cli.ReturnToMenuException.message)
        except utils_cli.MenuExitException:
            utils_cli.clearScreenSafety()
            utils_cli.exitMenu()


def _reset_rotor_menu(rotor_ref: rotors.Rotor):
    while True:
        try:
            rotors_f._show_config_rt(rotor_ref)
            for key in sorted(_menu_rotor_reset_options.keys()):
                utils_cli.printMenuOption(key + ":" + _menu_rotor_reset_options[key][0])

            answer = str(input(utils_cli.askForMenuOption()))
            _menu_rotor_reset_options.get(answer, [None, utils_cli.invalidChoice])[1](
                rotor_ref
            )
        except utils_cli.ReturnToMenuException:
            print(utils_cli.ReturnToMenuException.message)
        except utils_cli.MenuExitException:
            utils_cli.clearScreenSafety()
            utils_cli.exitMenu()


def _saved_rotor_menu(rotor_ref: rotors.Rotor):
    while True:
        try:
            rotors_f._show_config_rt(rotor_ref)
            for key in sorted(_menu_rotor_saved_rotor.keys()):
                utils_cli.printMenuOption(key + ":" + _menu_rotor_saved_rotor[key][0])

            answer = str(input(utils_cli.askForMenuOption()))
            _menu_rotor_saved_rotor.get(answer, [None, utils_cli.invalidChoice])[1](
                rotor_ref
            )
        except utils_cli.ReturnToMenuException:
            print(utils_cli.ReturnToMenuException.message)
        except utils_cli.MenuExitException:
            utils_cli.clearScreenSafety()
            utils_cli.exitMenu()


def _load_saved_rotor_for_editing(rotor: rotors.Rotor = None, recursive: bool = False):
    if not recursive:
        rotor = load_saved_rotor()
    _saved_rotor_menu(rotor)
    try:
        rotors_f._save_in_current_directory_rt(rotor)
        utils_cli.returningToMenuNoMessage()
    except utils_cli.MenuExitException:
        current_path = os.getcwd()
        new_folder = "SAVED_rotorS"
        path = os.path.join(current_path, new_folder)
        if not utils_cli.checkIfFileExists(path, rotor._name, "rotor"):
            utils_cli.printOutput("A file with the rotor's name was not detected")
            accbool = ""
            while not accbool == "n" or not accbool == "y":
                accbool = input(
                    utils_cli.askingInput("Do you want to exit anyway?[y/n]")
                ).lower()
            if accbool == "n":
                _load_saved_rotor_for_editing(rotor, True)
            utils_cli.returningToMenuMessage((f"rotor {rotor.name} was discarded"))
    # Conda activation: conda info --envs, conda activate {}


_menu_rotor = {
    "1": ("Show current rotor setup", rotors_f._show_config_rt),
    "2": ("Save rotor", rotors_f._save_in_current_directory_rt),
    "3": ("Naming menu", _name_rotor_menu),
    "4": ("Connections options menu", _connections_rotor_menu),
    "5": ("Resetting options menu", _reset_rotor_menu),
    "6": ("Edit a previously saved rotor", _load_saved_rotor_for_editing),
    "0": ("Exit menu", rotors_f._exitMenu_rt),
}


def main_rotor_menu(machine_ref: machines.Machine):
    while True:
        try:
            for key in sorted(_menu_rotor.keys()):
                printMenuOption(key + ":" + _menu_rotor[key][0])

            answer = str(input(askForMenuOption()))
            _menu_rotor.get(answer, [None, invalidChoice])[1](machine_ref)
        except ReturnToMenuException:
            print(ReturnToMenuException.message)
        except utils_cli.MenuExitException:
            clearScreenSafety()
            utils_cli.exitMenu()


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
    return ">Rotors and rotor set up and saved."

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

    def random_setup(self, seed=None, showConfig=True):
        # Randomly generate a rotor and store it in a folder
        # Seed has to be added from the machine calling the function, where the seed is stored/generated
        if not seed:
            print(
                ">>Something went wrong. Make sure development has reached this stage!"
            )
        # Once the seed is set, as long as the same operations are performed the same numbers are generated:
        random.seed(seed)
        # Name generation
        name_list = [
            random.sample(range(0, self._no_characters), 1)[0] for _ in range(0, 13)
        ]
        name_list[0:9] = [self._conversion_in_use[num] for num in name_list[0:9]]
        name_list[9:13] = [str(i % 10) for i in name_list[9:13]]
        string1 = ""
        name = string1.join(name_list)
        self._change_name(name)
        # Position
        self._define_position(
            self._conversion_in_use[random.randint(0, self._no_characters)]
        )  # Check in the future whether this setups are correct
        # Notches
        notch_list = [
            self._conversion_in_use[i]
            for i in set(
                random.sample(range(0, self._no_characters), random.randint(1, 5))
            )
        ]
        self._define_notches(notch_list)
        # self.define_rotor_jump(random.randint(1,25))
        # Forward dictionary
        num_list = list(range(0, self._no_characters))
        self._forward_num_dict = dict(
            zip(
                num_list,
                random.sample(range(0, self._no_characters), self._no_characters),
            )
        )
        sorted_dict = dict(sorted(self._forward_num_dict.items(), key=lambda x: x[1]))
        self._backward_num_dict = dict(zip(sorted_dict.values(), sorted_dict.keys()))
        print(">Rotor connections established")
        self._update_dicts(False)
        if showConfig:
            self.show_config()
        self.export_rotor()
        return
        # And we use this to generate numbers and lists of numbers from which to derive configurations, notches, positions and names
        # in the case of the connection board, an extra number should be used to determine nu


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

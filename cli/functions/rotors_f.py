## New seeds for standalone generated rotors, reflectors and boards
### EACH OBJECT SET OF MENUS TAKES THE REFERENCE FROM THE MACHINE, AND THEN OPERATES ON IT, EFFECTIVELY NOT TOUCHING THE MACHINE ITSELF BUT ITS OBJECTS
### EXCEPT FOR LOADING!!!!!! LOADING OF ITEMS HAS TO BE DONE DIRECTLY IN THE MACHINE MENU
### ALSO EXCEPT ALL GENERALISTIC CONFIG CALLS
# Intern setup functions
from ...core import rotors
from ...utils import utils
from ...utils.utils_cli import *
import pickle


def _show_config_rf(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    printOutput(
        "Rotor letter position :"
        + str(rotor_ref._conversion_in_use[rotor_ref._position])
    )
    printOutput("Rotor letter jumps:" + str(rotor_ref.jump))
    notchlist = [rotor_ref._conversion_in_use[i] for i in rotor_ref._notches]
    printOutput("Rotor notches:" + str(notchlist))
    printOutput("Forward connections in the rotor:" + str(rotor_ref._forward_dict))
    printOutput("Backward connections in the rotor:" + str(rotor_ref._backward_dict))
    printOutput("Rotor name:" + str(rotor_ref._name))
    returningToMenuNoMessage()


def _choose_connection_to_delete_rf(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    paired_df, _ = utils.simplify_dictionary_paired_unpaired(rotor_ref._board_dict)

    if paired_df.shape[0] == 0:
        returningToMenuMessage("There are no available connections.")

    printOutput("Current connections are:")
    print(paired_df)
    row = askingInput("Choose a connection to delete (by index):")

    if isinstance(row, int) and row > 0 and row < paired_df.shape[0]:
        _delete_a_connection_rf(rotor_ref=rotor_ref, connIndex=row)
        returningToMenuMessage("Connection was deleted.")
    else:
        returningToMenuMessage("Index invalid.")


def _delete_a_connection_rf(rotor_ref: rotors.Rotor, connIndex):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
        connIndex (_type_): _description_
    """
    paired_df, _ = utils.simplify_dictionary_paired_unpaired(rotor_ref._board_dict)
    for entry in paired_df.iloc[connIndex]:
        # del rotor_ref._board_dict[entry] #Requires testing
        rotor_ref[entry] = entry

    rotor_ref._update_dicts()
    # del d['k2']


def _create_a_connection_single_choice_rf(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    _, unpaired_list = utils.simplify_dictionary_paired_unpaired(rotor_ref._board_dict)
    if len(unpaired_list) < 2:
        returningToMenuMessage(
            "There are no letters left to pair (one or fewer left unconnected)."
        )
    print(">Unpaired letters:", unpaired_list)
    letter1 = askingInput("Choose a letter to pair:").upper()
    if letter1 not in unpaired_list:
        returningToMenuMessage("Invalid input.")
    printOutput("Remaining letters:"), list(set(unpaired_list) - set(letter1))
    letter2 = askingInput("Choose the second letter:").upper()
    if letter2 not in list(set(unpaired_list) - set(letter1)):
        returningToMenuMessage("Invalid input.")
    rotor_ref._board_dict[letter1] = letter2
    rotor_ref._board_dict[letter2] = letter1
    rotor_ref._update_dicts()
    returningToMenuMessage("The connection was formed.")


# First get a letter, show unconnected again, then choose to connect. If wrong choice, go back to start


def _connect_two_letters_rf(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    _, unpaired_list = utils.simplify_dictionary_paired_unpaired(rotor_ref._board_dict)
    if len(unpaired_list) < 2:
        returningToMenuMessage(
            "There are no letters left to pair (one or fewer left unconnected)."
        )
    while True:
        printOutput("Unpaired letters:"), unpaired_list
        printOutput("If you want to stop configurating the board, press Enter.")
        letters = askingInput("Input two letters to pair:").strip().upper()
        if letters.isalpha() and len(letters) == 2:
            pass
        elif not letters:
            returningToMenuNoMessage("No input.")
        else:
            print("Error: Input 2 letters please.")
            continue
        letters = list(letters)
        if not all(map(lambda v: v in letters, unpaired_list)):
            printOutput("One of the letters is already connected.")
            continue
        break
    rotor_ref._board_dict[letters[0]] = letters[1]
    rotor_ref._board_dict[letters[1]] = letters[0]
    printOutput("Connection formed.")


def _form_all_connections_rf(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    _show_config_rf(rotor_ref)
    _, unpaired_list = utils.simplify_dictionary_paired_unpaired(rotor_ref._board_dict)
    _form_n_connections_rf(rotor_ref, int(len(unpaired_list) / 2))
    returningToMenuMessage(
        "There are no letters left to pair (one or fewer left unconnected)."
    )


# def reset_and_form_all_connections(rotor_ref: rotors.Rotor):
#     """_summary_

#     Args:
#         rotor_ref (rotors.Rotor): _description_
#     """
#     reset_connections(rotor_ref)
#     form_all_connections(rotor_ref)


def _form_n_connections_rf(rotor_ref: rotors.Rotor, connections: int):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
        connections (int): _description_
    """
    for i in range(connections):
        clearScreenConvenience()
        printOutput(f"Creating connection {i+1} of {connections}")
        _connect_two_letters_rf(rotor_ref)


def _reset_and_streamline_connections_by_pairs_rf(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    _reset_connections_rf(rotor_ref)
    while True:
        accbool = askingInput("Do you still want to make changes?[y/n]").lower()
        if accbool == "n":
            returningToMenuNoMessage()
        elif accbool == "y":
            break
    while True:
        _connect_two_letters_rf(rotor_ref)


## The board is fully connected (one or fewer letters left unconnected). If wrong choice, go back to start


def _reset_and_randomize_connections_rf(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    seed = input(
        askingInput(
            "Introduce a positive integer as a seed to randomize the plugboard connections: "
        )
    )
    if not isinstance(seed, int) and seed > 0:
        returningToMenuMessage("Number is not a positive integer.")
    rotor_ref._reset_dictionaries()
    rotor_ref.random_setup(seed)


def _reset_connections_rf(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    rotor_ref._reset_dictionaries()


def _print_name_rf(rotor_ref: rotors.Rotor):
    printOutput("REFLECTOR NAME: " + rotor_ref._name)


def _change_reflector_name_rf(rotor_ref: rotors.Rotor):
    new_name = str(askingInput("Input a new name for the reflector:"))
    while any(not c.isalnum() for c in new_name) or not new_name:
        printOutput("Input only alphanumerical.")
        new_name = str(askingInput("Input a new name for the reflector:"))
    rotor_ref._change_name(new_name)
    returningToMenuMessage("Reflector name changed to: " + rotor_ref._name)


def _randomize_name_rf(rotor_ref: rotors.Rotor):
    rotor_ref.random_name()
    returningToMenuMessage("NEW NAME: " + rotor_ref.name)


def _save_in_current_directory_rf(rotor_ref: rotors.Rotor):
    while (
        rotor_ref.name == "name"
        or rotor_ref.name == ""
        or any(not c.isalnum() for c in rotor_ref.name)
    ):
        rotor_ref._change_name(
            askingInput("Please assign a new name to the reflector:")
        ).strip()
    current_path = os.getcwd()
    new_folder = "SAVED_REFLECTORS"
    path = os.path.join(current_path, new_folder)
    if not os.path.exists(path):
        os.mkdir(path)
        printOutput("Directory '% s' created" % path)
    if checkIfFileExists(path, rotor_ref._name, "reflector"):
        printOutput("A reflector with this name already exists.")
        accbool = ""
        while not accbool == "n" or not accbool == "y":
            accbool = input(
                askingInput("Do you want to overwrite the saved reflector? [y/n]")
            ).lower()
        if accbool == "n":
            returningToMenuNoMessage()
    save_file = open(r"{}\\{}.reflector".format(path, rotor_ref._name), "wb")
    pickle.dump(rotor_ref, save_file)
    returningToMenuMessage(
        (
            "{} has been saved into {}.reflector in {}".format(
                rotor_ref.name, rotor_ref.name, path
            )
        )
    )


def load_saved_reflector():
    current_path = os.path.dirname(__file__)
    new_folder = "SAVED_REFLECTORS"
    path = os.path.join(current_path, new_folder)
    if not os.path.exists(path):
        returningToMenuMessage("There is no {} folder.".format(path))
    list_of_files = [element.rsplit((".", 1)[0])[0] for element in os.listdir(path)]
    if len(list_of_files) == 0:
        returningToMenuMessage("There are no reflectors saved.")
    printOutput("Your available reflectors are: {}".format(list_of_files))
    reflector = askingInput("Input reflector's position in the list: ")
    while (
        not isinstance(reflector, int)
        or reflector > len(list_of_files) - 1
        or reflector < 0
    ):
        printOutput("Please input a valid index.")
        reflector = askingInput("Input reflector's position in the list:")
    filehandler = open(
        r"{}\\{}.reflector".format(path, list_of_files[reflector - 1]), "rb"
    )
    return pickle.load(filehandler)


def _exitMenu_rf(rotor_ref: rotors.Rotor):
    _, unpaired_list = utils.simplify_dictionary_paired_unpaired(
        rotor_ref._reflector_dict
    )
    if len(unpaired_list) > 1:
        returningToMenuMessage(
            "To avoid self-sabotage, a partially connected reflector is discouraged."
        )
    exitMenu()


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
            random.sample(range(0, len(self._characters_in_use)), 1)[0]
            for _ in range(0, 13)
        ]
        name_list[0:9] = [self._conversion_in_use[num] for num in name_list[0:9]]
        name_list[9:13] = [str(i % 10) for i in name_list[9:13]]
        string1 = ""
        name = string1.join(name_list)
        self._change_name(name)
        # Position
        self._define_position(
            self._conversion_in_use[random.randint(0, len(self._characters_in_use))]
        )  # Check in the future whether this setups are correct
        # Notches
        notch_list = [
            self._conversion_in_use[i]
            for i in set(
                random.sample(
                    range(0, len(self._characters_in_use)), random.randint(1, 5)
                )
            )
        ]
        self._define_notches(notch_list)
        # self.define_rotor_jump(random.randint(1,25))
        # Forward dictionary
        num_list = list(range(0, len(self._characters_in_use)))
        self._forward_num_dict = dict(
            zip(
                num_list,
                random.sample(
                    range(0, len(self._characters_in_use)), len(self._characters_in_use)
                ),
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

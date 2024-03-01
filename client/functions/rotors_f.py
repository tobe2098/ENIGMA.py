## New seeds for standalone generated rotors, reflectors and boards
### EACH OBJECT SET OF MENUS TAKES THE REFERENCE FROM THE MACHINE, AND THEN OPERATES ON IT, EFFECTIVELY NOT TOUCHING THE MACHINE ITSELF BUT ITS OBJECTS
### EXCEPT FOR LOADING!!!!!! LOADING OF ITEMS HAS TO BE DONE DIRECTLY IN THE MACHINE MENU
### ALSO EXCEPT ALL GENERALISTIC CONFIG CALLS
### PUT WARNING IN ALL MENUING RELATED TO JUMP (IN RANDOM JUMP IS ALWAYS 1?)never zero or no_chars%jump==0!!, write explanation of interplay between notches and jump
# Intern setup functions
from ...core import rotors
from ...utils import utils
from ...utils import utils_cli
import random
import os
import pickle
from copy import copy


def _show_config_rt(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    utils_cli.printOutput(
        "Rotor letter position :",
        str(rotor_ref._conversion_in_use[rotor_ref._position]),
    )
    utils_cli.printOutput("Rotor letter jumps:", str(rotor_ref._jump))
    notchlist = [rotor_ref._conversion_in_use[i] for i in rotor_ref._notches]
    utils_cli.printOutput("Rotor notches:", str(notchlist))
    utils_cli.printOutput(
        "Forward connections in the rotor:", (rotor_ref._forward_dict)
    )
    utils_cli.printOutput(
        "Backward connections in the rotor:", str(rotor_ref._backward_dict)
    )
    utils_cli.printOutput("Rotor name:", str(rotor_ref._name))
    (
        _,
        unpaired,
        _,
        _,
    ) = utils.simplify_rotor_dictionary_paired_unpaired(
        rotor_ref._forward_dict, rotor_ref._backward_dict
    )
    if len(unpaired) > 0:
        utils_cli.printOutput(
            "One or more connections are self-connections. This may go against proper practice"
        )
    utils_cli.returningToMenuNoMessage()


# For now, in text, there will be no connection deletion? Or will there?
def _choose_connection_to_delete_rt(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    paired_df, _, _, _ = utils.simplify_rotor_dictionary_paired_unpaired(
        rotor_ref._forward_dict, rotor_ref._backward_dict
    )

    if paired_df.shape[0] == 0:
        utils_cli.returningToMenuMessage("There are no available connections")

    utils_cli.printOutput("Current connections are:")
    print(paired_df)
    row = utils_cli.askingInput("Choose a connection to delete (by index):")

    if isinstance(row, int) and row > 0 and row < paired_df.shape[0]:
        _delete_a_connection_rt(rotor_ref=rotor_ref, connIndex=row)
        utils_cli.returningToMenuMessage("Connection was deleted")
    else:
        utils_cli.returningToMenuMessage("Index invalid")


def _delete_a_connection_rt(rotor_ref: rotors.Rotor, connIndex):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
        connIndex (_type_): _description_
    """
    paired_df, _, _, _ = utils.simplify_rotor_dictionary_paired_unpaired(
        rotor_ref._forward_dict, rotor_ref._backward_dict
    )
    entry1, entry2 = paired_df.iloc[connIndex]
    # del rotor_ref._board_dict[entry] #Requires testing
    rotor_ref._forward_dict[entry1] = ""
    rotor_ref._backward_dict[entry2] = ""
    rotor_ref.lacks_conn = True
    rotor_ref._update_dicts()
    # del d['k2']


def _create_a_connection_single_choice_rt(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    (
        _,
        _,
        front_unformed,
        back_unformed,
    ) = utils.simplify_rotor_dictionary_paired_unpaired(
        rotor_ref._forward_dict, rotor_ref._backward_dict
    )
    if len(front_unformed) == 0 and len(back_unformed) == 0:
        rotor_ref.lacks_conn = False
        utils_cli.returningToMenuMessage(
            "There are no letters left to pair (one or fewer left unconnected)"
        )
    utils_cli.printOutput("Unpaired letters in front side:", (front_unformed))

    letter1 = utils_cli.askingInput("Choose a letter to pair from front side:").upper()
    if letter1 not in front_unformed:
        utils_cli.returningToMenuMessage("Invalid input")
    utils_cli.printOutput("Unpaired letters in back side:", (back_unformed))
    letter2 = utils_cli.askingInput(
        "Choose the second letter from the back side:"
    ).upper()
    if letter2 not in back_unformed:
        utils_cli.returningToMenuMessage("Invalid input")
    rotor_ref._forward_dict[letter1] = letter2
    rotor_ref._backward_dict[letter2] = letter1
    rotor_ref._update_dicts()
    utils_cli.returningToMenuMessage("The connection was formed")
    if len(front_unformed) - 1 == 0 and len(back_unformed) - 1 == 0:
        rotor_ref.lacks_conn = False


# First get a letter, show unconnected again, then choose to connect. If wrong choice, go back to start


def _connect_all_letters_rt(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    # (
    #     _,
    #     _,
    #     front_unformed,
    #     back_unformed,
    # ) = utils.simplify_rotor_dictionary_paired_unpaired(
    #     rotor_ref._forward_dict, rotor_ref._backward_dict
    # )
    # if len(front_unformed) == 0 and len(back_unformed) == 0:
    #     rotor_ref.lacks_conn = True
    #     utils_cli.returningToMenuMessage(
    #         "There are no letters left to pair (one or fewer left unconnected)"
    #     )
    while True:
        (
            _,
            _,
            front_unformed,
            back_unformed,
        ) = utils.simplify_rotor_dictionary_paired_unpaired(
            rotor_ref._forward_dict, rotor_ref._backward_dict
        )
        if len(front_unformed) == 0 and len(back_unformed) == 0:
            rotor_ref.lacks_conn = False
            utils_cli.returningToMenuMessage(
                "There are no letters left to pair (one or fewer left unconnected)"
            )
        utils_cli.printOutput("Unpaired letters in front side:", (front_unformed))
        utils_cli.printOutput("Unpaired letters in back side:", (back_unformed))
        utils_cli.printOutput(
            "If you want to stop configurating the board, press Enter"
        )
        letters = (
            utils_cli.askingInput(
                "Input one letter from front side, one from back side (in order):"
            )
            .strip()
            .upper()
        )
        if letters.isalpha() and len(letters) == 2:
            pass
        elif not letters:
            return
        else:
            print("Error: Only 2 letters please")
            continue
        letters = list(letters)
        if letters[0] not in front_unformed or letters[1] not in back_unformed:
            utils_cli.printOutput("One or more letters are already connected")
            continue
        # break
        rotor_ref._forward_dict[letters[0]] = letters[1]
        rotor_ref._backward_dict[letters[1]] = letters[0]
        utils_cli.printOutput("Connection formed")


def _form_all_connections_rt(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    _show_config_rt(rotor_ref)
    # _, unpaired_list = utils.simplify_simple_dictionary_paired_unpaired(
    #     rotor_ref._board_dict
    # )
    _connect_all_letters_rt(rotor_ref)
    rotor_ref.lacks_conn = True
    utils_cli.returningToMenuMessage("You exited without forming all connections!")

    # utils_cli.returningToMenuMessage(
    #     "There are no letters left to pair (one or fewer left unconnected)"
    # )


# def reset_and_form_all_connections(rotor_ref: rotors.Rotor):
#     """_summary_

#     Args:
#         rotor_ref (rotors.Rotor): _description_
#     """
#     reset_connections(rotor_ref)
#     form_all_connections(rotor_ref)


def _swap_two_connections_rt(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
        connections (int): _description_
    """
    _show_config_rt(rotor_ref)
    letter1 = utils_cli.askingInput(
        "Choose a frontside connection by the frontside letter to swap:"
    ).upper()
    if letter1 not in rotor_ref._characters_in_use:
        utils_cli.printOutput("Invalid input")
        return
    letter2 = utils_cli.askingInput(
        "Choose a second frontside connection by the frontside letter to swap:"
    ).upper()
    if letter2 not in rotor_ref._characters_in_use:
        utils_cli.printOutput("Invalid input")
        return
    (
        rotor_ref._backward_dict[rotor_ref._forward_dict[letter1]],
        rotor_ref._backward_dict[rotor_ref._forward_dict[letter2]],
    ) = (
        rotor_ref._backward_dict[rotor_ref._forward_dict[letter2]],
        rotor_ref._backward_dict[rotor_ref._forward_dict[letter1]],
    )
    rotor_ref._forward_dict[letter1], rotor_ref._forward_dict[letter2] = (
        rotor_ref._forward_dict[letter2],
        rotor_ref._forward_dict[letter1],
    )
    rotor_ref._update_dicts()
    utils_cli.printOutput("The connection was swapped")


def _swap_connections_rt(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    while True:
        boolean = utils_cli.askingInput(
            "If you do not want to continue swapping, enter N:"
        ).upper()
        if boolean == "N":
            utils_cli.returningToMenuMessage("Returning to menu...")
        _swap_two_connections_rt(rotor_ref=rotor_ref)

    # utils_cli.returningToMenuMessage(
    #     "There are no letters left to pair (one or fewer left unconnected)."
    # )


def _reset_and_streamline_connections_by_pairs_rt(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    _reset_connections_rt(rotor_ref)
    # while True:
    #     accbool = utils_cli.utils_cli.askingInput("Do you still want to make changes?[y/n]").lower()
    #     if accbool == "n":
    #         utils_cli.returningToMenuNoMessage()
    #     elif accbool == "y":
    #         break
    _connect_all_letters_rt(rotor_ref)
    rotor_ref.lacks_conn = True
    utils_cli.returningToMenuMessage("You exited without forming all connections!")


def _reset_and_randomize_connections_rt(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    seed = input(
        utils_cli.askingInput(
            "Introduce a positive integer as a seed to randomize the rotor connections: "
        )
    )
    if not isinstance(seed, int) and seed > 0:
        utils_cli.returningToMenuMessage("Number is not a positive integer")
    if not seed:
        utils_cli.returningToMenuMessage(
            "Seed is necessary for randomization of connections"
        )
    rotor_ref._reset_dictionaries()
    rotor_ref._randomize_dictionaries(seed)
    utils_cli.returningToMenuMessage("Rotor connections established")


def _reset_connections_rt(rotor_ref: rotors.Rotor):
    """_summary_

    Args:
        rotor_ref (rotors.Rotor): _description_
    """
    rotor_ref._reset_dictionaries()


def _print_name_rt(rotor_ref: rotors.Rotor):
    utils_cli.printOutput("ROTOR NAME:", rotor_ref._name)


def _change_rotor_name_rt(rotor_ref: rotors.Rotor):
    new_name = str(utils_cli.askingInput("Input a new name for the rotor:"))
    while any(not c.isalnum() for c in new_name) or not new_name:
        utils_cli.printOutput("Input only alphanumerical")
        new_name = str(utils_cli.askingInput("Input a new name for the rotor:"))
    rotor_ref._change_name(new_name)
    utils_cli.returningToMenuMessage("Rotor name changed to:", rotor_ref._name)


def _randomize_name_rt(rotor_ref: rotors.Rotor):
    rotor_ref._random_name()
    utils_cli.returningToMenuMessage("Rotor name changed to:", rotor_ref._name)


def _save_in_current_directory_rt(rotor_ref: rotors.Rotor):
    while (
        rotor_ref._name == "name"
        or rotor_ref._name == ""
        or any(not c.isalnum() for c in rotor_ref._name)
    ):
        rotor_ref._change_name(
            utils_cli.askingInput("Please assign a new name to the rotor:")
        ).strip()
    current_path = os.getcwd()
    new_folder = "SAVED_ROTORS"
    path = os.path.join(current_path, new_folder)
    if not os.path.exists(path):
        os.mkdir(path)
        utils_cli.printOutput("Directory '% s' created" % path)
    if utils_cli.checkIfFileExists(path, rotor_ref._name, "rotor"):
        utils_cli.printOutput("A rotor with this name already exists")
        accbool = ""
        while not accbool == "n" or not accbool == "y":
            accbool = input(
                utils_cli.askingInput("Do you want to overwrite the saved rotor? [y/n]")
            ).lower()
        if accbool == "n":
            utils_cli.returningToMenuNoMessage()
    save_file = open(r"{}\\{}.rotor".format(path, rotor_ref._name), "wb")
    pickle.dump(rotor_ref, save_file)
    utils_cli.returningToMenuMessage(
        (
            "{} has been saved into {}.rotor in {}".format(
                rotor_ref._name, rotor_ref._name, path
            )
        )
    )


def _exitMenu_rt(rotor_ref: rotors.Rotor):
    (
        _,
        _,
        front_unformed,
        _,
    ) = utils.simplify_rotor_dictionary_paired_unpaired(
        rotor_ref._forward_dict, rotor_ref._backward_dict
    )
    if len(front_unformed) > 0:
        utils_cli.returningToMenuMessage(
            "Due to implementation reasons, a partially connected rotor is not allowed"
        )
    utils_cli.exitMenu()


def _change_notches_rt(rotor_ref: rotors.Rotor):
    utils_cli.printOutput("Rotor notches: ", rotor_ref.get_notchlist_letters())
    positions = [
        i
        for i in rotor_ref._define_notches(
            utils_cli.askingInput("Input new notches(empty to skip):").split()
        )
    ]
    if not positions:
        return

    rotor_ref._define_notches(positions)

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
        rotor = rotors.Rotor()
        rotor._random_setup(seed + i)
    return ">Done"


def tune_existing_rotor():
    rotor = rotors.Rotor()
    rotor.import_rotor()
    rotor.configure()
    rotor.export_rotor()
    return ">Rotor was edited and saved"

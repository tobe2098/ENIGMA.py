from ...core import machines
from ...core import reflectors
from ...core import utils
from .utils_m import *
import pickle

def _show_config_rf(reflector_ref: reflectors.Reflector):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
    """

    reflector_ref._show_config()
    returningToMenuNoMessage()


def _choose_connection_to_delete_rf(reflector_ref: reflectors.Reflector):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
    """
    paired_df, _ = utils.simplify_dictionary_paired_unpaired(reflector_ref._board_dict)

    if paired_df.shape[0] == 0:
        returningToMenuMessage("There are no available connections.")

    print(stringOutput("Current connections are:"), paired_df)
    row = input(askingInput("Choose a connection to delete (by index): "))

    if isinstance(row, int) and row > 0 and row < paired_df.shape[0]:
        _delete_a_connection_rf(reflector_ref=reflector_ref, connIndex=row)
        returningToMenuMessage("Connection was deleted.")
    else:
        returningToMenuMessage("Index invalid.")


def _delete_a_connection_rf(reflector_ref: reflectors.Reflector, connIndex):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
        connIndex (_type_): _description_
    """
    paired_df, _ = utils.simplify_dictionary_paired_unpaired(reflector_ref._board_dict)
    for entry in paired_df.iloc[connIndex]:
        # del reflector_ref._board_dict[entry] #Requires testing
        reflector_ref[entry] = entry

    reflector_ref._update_dicts()
    # del d['k2']


def _create_a_connection_single_choice_rf(reflector_ref: reflectors.Reflector):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
    """
    _, unpaired_list = utils.simplify_dictionary_paired_unpaired(reflector_ref._board_dict)
    if len(unpaired_list) < 2:
        returningToMenuMessage(
            "There are no letters left to pair (one or fewer left unconnected)."
        )
    print(">Unpaired letters:", unpaired_list)
    letter1 = input(askingInput("Choose a letter to pair:")).upper()
    if letter1 not in unpaired_list:
        returningToMenuMessage("Invalid input.")
    print(stringOutput("Remaining letters:"), list(set(unpaired_list) - set(letter1)))
    letter2 = input(askingInput("Choose the second letter:")).upper()
    if letter2 not in list(set(unpaired_list) - set(letter1)):
        returningToMenuMessage("Invalid input.")
    reflector_ref._board_dict[letter1] = letter2
    reflector_ref._board_dict[letter2] = letter1
    reflector_ref._update_dicts()
    returningToMenuMessage("The connection was formed.")


# First get a letter, show unconnected again, then choose to connect. If wrong choice, go back to start


def _connect_two_letters_rf(reflector_ref: reflectors.Reflector):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
    """
    _, unpaired_list = utils.simplify_dictionary_paired_unpaired(reflector_ref._board_dict)
    if len(unpaired_list) < 2:
        returningToMenuMessage(
            "There are no letters left to pair (one or fewer left unconnected)."
        )
    while True:
        print(stringOutput("Unpaired letters:"), unpaired_list)
        print(stringOutput("If you want to stop configurating the board, press Enter."))
        letters = input(askingInput("Input two letters to pair:")).strip().upper()
        if letters.isalpha() and len(letters) == 2:
            pass
        elif not letters:
            returningToMenuNoMessage("No input.")
        else:
            print("Error: Input 2 letters please")
            continue
        letters = list(letters)
        if not all(map(lambda v: v in letters, unpaired_list)):
            print(stringOutput("One of the letters is already connected."))
            continue
        break
    reflector_ref._board_dict[letters[0]] = letters[1]
    reflector_ref._board_dict[letters[1]] = letters[0]
    print(stringOutput("Connection formed."))


def _form_all_connections_rf(reflector_ref: reflectors.Reflector):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
    """
    _show_config_rf(reflector_ref)
    _, unpaired_list = utils.simplify_dictionary_paired_unpaired(reflector_ref._board_dict)
    _form_n_connections_rf(reflector_ref, int(len(unpaired_list) / 2))
    returningToMenuMessage(
        "There are no letters left to pair (one or fewer left unconnected)."
    )


# def reset_and_form_all_connections(reflector_ref: reflectors.Reflector):
#     """_summary_

#     Args:
#         reflector_ref (reflectors.Reflector): _description_
#     """
#     reset_connections(reflector_ref)
#     form_all_connections(reflector_ref)


def _form_n_connections_rf(reflector_ref: reflectors.Reflector, connections: int):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
        connections (int): _description_
    """
    for i in range(connections):
        clearScreenConvenience()
        print(stringOutput(f"Creating connection {i+1} of {connections}"))
        _connect_two_letters_rf(reflector_ref)


def _reset_and_streamline_connections_by_pairs_rf(reflector_ref: reflectors.Reflector):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
    """
    _reset_connections_rf(reflector_ref)
    while True:
        accbool = input(askingInput("Do you still want to make changes?[y/n]")).lower()
        if accbool == "n":
            returningToMenuNoMessage()
        elif accbool == "y":
            break
    while True:
        _connect_two_letters_rf(reflector_ref)


## The board is fully connected (one or fewer letters left unconnected). If wrong choice, go back to start


def _reset_and_randomize_connections_rf(reflector_ref: reflectors.Reflector):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
    """
    seed = input(
        askingInput(
            "Introduce a positive integer as a seed to randomize the plugboard connections: "
        )
    )
    if not isinstance(seed, int) and seed > 0:
        returningToMenuMessage("Number is not a positive integer.")
    reflector_ref._reset_dictionaries()
    reflector_ref.random_setup(seed)


def _reset_connections_rf(reflector_ref: reflectors.Reflector):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
    """
    reflector_ref._reset_dictionaries()


def _change_reflector_name_rf(reflector_ref: reflectors.Reflector):
    new_name=str(input(askingInput("Input a new name for the reflector: ")))
    while any(not c.isalnum() for c in new_name) or not new_name:
      print(stringOutput("Input only alphanumerical"))
      new_name=str(input(askingInput("Input a new name for the reflector: ")))
    reflector_ref._change_name(new_name)
    returningToMenuMessage("Reflector name changed to: " + reflector_ref._name)


def _save_in_current_directory_rf(reflector_ref: reflectors.Reflector):
    while reflector_ref.name == "name" or reflector_ref.name=="" or any(not c.isalnum() for c in reflector_ref.name):
        reflector_ref._change_name(input(askingInput("Please assign a new name to the reflector: ")).strip())
    current_path = os.getcwd()
    new_folder = "SAVED_REFLECTORS"
    path = os.path.join(current_path, new_folder)
    if not os.path.exists(path):
        os.mkdir(path)
        print(stringOutput("Directory '% s' created" % path))
    if os.path.isfile(r"{}\\{}.reflector".format(path, reflector_ref._name)):
        print(stringOutput("A rotor with this name already exists."))
        accbool=""
        while not accbool=='n' or  not accbool=='y':
          accbool=input(askingInput("Do you want to overwrite the saved rotor? [y/n]")).lower()
        if accbool=='n':
            returningToMenuNoMessage()
    save_file = open(r"{}\\{}.reflector".format(path, reflector_ref._name), "wb")
    pickle.dump(reflector_ref, save_file)
    returningToMenuMessage(
        ("{} has been saved into {}.reflector in {}".format(
            reflector_ref.name, reflector_ref.name, path
        ))
    )

def load_saved_reflector():
    current_path = os.path.dirname(__file__)
    new_folder = "SAVED_REFLECTORS"
    path = os.path.join(current_path, new_folder)
    if not os.path.exists(path):
        returningToMenuMessage("There is no {} folder.".format(path))
    list_of_files = [element.rsplit(('.', 1)[0])[0]
                      for element in os.listdir(path)]
    list_of_files = [element.rsplit((".", 1)[0])[0] for element in os.listdir(path)]
    if len(list_of_files) == 0:
        returningToMenuMessage("There are no reflectors saved.")
    print(stringOutput("Your available reflectors are: {}".format(list_of_files)))
    reflector = input(askingInput("Input reflector's position in the list: "))
    while not isinstance(reflector, int) or reflector>len(list_of_files)-1 or reflector<0:
        print(stringOutput("Please input a valid index."))
        reflector = input(askingInput("Input reflector's position in the list: "))
    filehandler = open(r"{}\\{}.reflector".format(
        path, list_of_files[reflector-1]), 'rb')
    filehandler = open(
        r"{}\\{}.reflector".format(path, list_of_files[reflector - 1]), "rb"
    )
    return pickle.load(filehandler)


def _exitMenu_rf(reflector_ref:reflectors.Reflector):
    _,unpaired_list=utils.simplify_dictionary_paired_unpaired(reflector_ref._reflector_dict)
    if len(unpaired_list)>1:
        returningToMenuMessage("To avoid self-sabotage, a partially connected reflector is discouraged.")
    exitMenu()

_menu_reflector = {
    "1": ("Show current reflector setup", _show_config_rf),
    "1": ("Save rotor", _save_in_current_directory_rf),
    "1": ("Change rotor name", _change_reflector_name_rf),
    "2": ("Delete a single connection", _choose_connection_to_delete_rf),
    "3": ("Create a single connection", _create_a_connection_single_choice_rf),
    "4": ("Form all connections left", _form_all_connections_rf),
    "6": ("Reset and form max. connections", _reset_and_streamline_connections_by_pairs_rf),
    "7": ("Reset and randomize connections", _reset_and_randomize_connections_rf),
    "8": ("Reset connections", _reset_connections_rf),
    "0": ("Exit menu", _exitMenu_rf),
}

_menu_reflector_name_options = {
    "1": ("Show current reflector setup", _show_config_rf),
    "1": ("Save rotor", _save_in_current_directory_rf),
    "1": ("Change rotor name", _change_reflector_name_rf),
    "2": ("Delete a single connection", _choose_connection_to_delete_rf),
    "3": ("Create a single connection", _create_a_connection_single_choice_rf),
    "4": ("Form all connections left", _form_all_connections_rf),
    "6": ("Reset and form max. connections", _reset_and_streamline_connections_by_pairs_rf),
    "7": ("Reset and randomize connections", _reset_and_randomize_connections_rf),
    "8": ("Reset connections", _reset_connections_rf),
    "0": ("Exit menu", _exitMenu_rf),
}

_menu_reflector_connections_options = {
    "1": ("Show current reflector setup", _show_config_rf),
    "1": ("Save rotor", _save_in_current_directory_rf),
    "1": ("Change rotor name", _change_reflector_name_rf),
    "2": ("Delete a single connection", _choose_connection_to_delete_rf),
    "3": ("Create a single connection", _create_a_connection_single_choice_rf),
    "4": ("Form all connections left", _form_all_connections_rf),
    "6": ("Reset and form max. connections", _reset_and_streamline_connections_by_pairs_rf),
    "7": ("Reset and randomize connections", _reset_and_randomize_connections_rf),
    "8": ("Reset connections", _reset_connections_rf),
    "0": ("Exit menu", _exitMenu_rf),
}

_menu_reflector_reset_options = {
    "1": ("Show current reflector setup", _show_config_rf),
    "1": ("Save rotor", _save_in_current_directory_rf),
    "1": ("Change rotor name", _change_reflector_name_rf),
    "2": ("Delete a single connection", _choose_connection_to_delete_rf),
    "3": ("Create a single connection", _create_a_connection_single_choice_rf),
    "4": ("Form all connections left", _form_all_connections_rf),
    "6": ("Reset and form max. connections", _reset_and_streamline_connections_by_pairs_rf),
    "7": ("Reset and randomize connections", _reset_and_randomize_connections_rf),
    "8": ("Reset connections", _reset_connections_rf),
    "0": ("Exit menu", _exitMenu_rf),
}


def main_reflector_menu(machine_ref: machines.Machine):
    while True:
        clearScreenSafety()
        try:
            for key in sorted(_menu_reflector.keys()):
                print(menuOption(key + ":" + _menu_reflector[key][0]))

            answer = str(input(askForMenuOption()))
            _menu_reflector.get(answer, [None, invalidChoice])[1](
                machine_ref
            )
        except ReturnToMenuException:
            print(ReturnToMenuException.message)
        except MenuExitException:
            exitMenu()

def name_reflector_menu(machine_ref: machines.Machine):
    while True:
        clearScreenSafety()
        try:
            for key in sorted(_menu_reflector.keys()):
                print(menuOption(key + ":" + _menu_reflector[key][0]))

            answer = str(input(askForMenuOption()))
            _menu_reflector.get(answer, [None, invalidChoice])[1](
                machine_ref._reflector
            )
        except ReturnToMenuException:
            print(ReturnToMenuException.message)
        except MenuExitException:
            exitMenu()
def connections_reflector_menu(machine_ref: machines.Machine):
    while True:
        clearScreenSafety()
        try:
            for key in sorted(_menu_reflector.keys()):
                print(menuOption(key + ":" + _menu_reflector[key][0]))

            answer = str(input(askForMenuOption()))
            _menu_reflector.get(answer, [None, invalidChoice])[1](
                machine_ref._reflector
            )
        except ReturnToMenuException:
            print(ReturnToMenuException.message)
        except MenuExitException:
            exitMenu()
def reset_reflector_menu(machine_ref: machines.Machine):
    while True:
        clearScreenSafety()
        try:
            for key in sorted(_menu_reflector.keys()):
                print(menuOption(key + ":" + _menu_reflector[key][0]))

            answer = str(input(askForMenuOption()))
            _menu_reflector.get(answer, [None, invalidChoice])[1](
                machine_ref._reflector
            )
        except ReturnToMenuException:
            print(ReturnToMenuException.message)
        except MenuExitException:
            exitMenu()
    def configure(self):
        # Configuration of the cable reflector
        # PENDING: Make it stop after 26 letters have been assigned
        if self.reflector_dict:
            print(">Current reflector setup is:")
            print(">Connections:\n", simplify_board_dict(self.reflector_dict))
            print(">Name:", self.name)
            accbool = input(
                ">>>Input N if you do NOT want to change the reflector setup:"
            )
            if accbool == "N":
                return
        if self.name == "name":
            print(">Changing the name is necessary for exporting it")
        new_name = input(">>>Input new name for the reflector (Press Enter to skip):")
        if new_name:
            self.change_name(new_name)
        seen_letters = []
        reflector_dict = {letter: letter for letter in self.characters_in_use}
        all_letters = self.characters_in_use
        while True:
            if len(list(set(all_letters) - set(seen_letters))) == 0:
                break
            print(">If you want to stop configurating the reflector, press Enter")
            configpair = input(
                ">>>Enter pair of letters for reflector configuration:"
            ).upper()
            if configpair and not configpair.isalpha():
                print(">Error: Input 2 letters please")
                continue
            configpair = [i for i in configpair]
            if len(configpair) == 2:
                pass
            elif len(configpair) == 0:
                break
            else:
                print(">Error: Input 2 letters please")
                continue
            if any(map(lambda v: v in configpair, seen_letters)):
                print(">One of the letters was already plugged")
                continue
            else:
                seen_letters.append(configpair[0])
                seen_letters.append(configpair[1])
                reflector_dict[configpair[0]] = configpair[1]
                reflector_dict[configpair[1]] = configpair[0]
            print(">Current config:\n", simplify_board_dict(reflector_dict))
            remaining_letters = list(set(all_letters) - set(seen_letters))
            print(">Not connected letters:\n", remaining_letters)
        if len(remaining_letters) == 1:
            reflector_dict[remaining_letters[0]] = remaining_letters[0]
        self.show_config()
        self.reflector_dict = copy.copy(reflector_dict)
        self._update_dicts()
        self.export_reflector()
        print(">Finished")


def generate_n_random_reflectors(n, seed):
    # Create and save into pickle objects 20 randomly generated rotors. Use seed to generate new seed, or simply add numbers
    for j in range(0, n):
        reflector = reflector.Reflector()
        reflector.random_name(seed+ j )
        reflector.random_setup(seed + j)
    print(stringOutput(f"Created and saved {n} rotors."))


def load_saved_reflector_for_editing():
    reflector = import_reflector()
    reflector.configure() CALL NEW MENU HERE
    reflector.export_reflector()
    print(stringOutput(f"Reflector {reflector.name} has been saved."))
    # Conda activation: conda info --envs, conda activate {}

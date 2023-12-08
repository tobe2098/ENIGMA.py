from ...core import machines
from ...core import reflectors
from ...core import utils
from .utils_m import *


def show_board_config(reflector_ref: reflectors.Reflector):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
    """

    reflector_ref._show_config()
    returningToMenuNoMessage()


def choose_connection_to_delete(reflector_ref: reflectors.Reflector):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
    """
    paired_df, _ = utils.simplify_board_dict(reflector_ref._board_dict)

    if paired_df.shape[0] == 0:
        returningToMenuMessage("There are no available connections.")

    print(stringOutput("Current connections are:"), paired_df)
    row = input(askingInput("Choose a connection to delete (by index): "))

    if isinstance(row, int) and row > 0 and row < paired_df.shape[0]:
        delete_a_connection(reflector_ref=reflector_ref, connIndex=row)
        returningToMenuMessage("Connection was deleted.")
    else:
        returningToMenuMessage("Index invalid.")


def delete_a_connection(reflector_ref: reflectors.Reflector, connIndex):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
        connIndex (_type_): _description_
    """
    paired_df, _ = utils.simplify_board_dict(reflector_ref._board_dict)
    for entry in paired_df.iloc[connIndex]:
        # del reflector_ref._board_dict[entry] #Requires testing
        reflector_ref[entry] = entry

    reflector_ref._update_dicts()
    # del d['k2']


def create_a_connection_single_choice(reflector_ref: reflectors.Reflector):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
    """
    _, unpaired_list = utils.simplify_board_dict(reflector_ref._board_dict)
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


def connect_two_letters(reflector_ref: reflectors.Reflector):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
    """
    _, unpaired_list = utils.simplify_board_dict(reflector_ref._board_dict)
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


def form_all_connections(reflector_ref: reflectors.Reflector):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
    """
    show_board_config(reflector_ref)
    _, unpaired_list = utils.simplify_board_dict(reflector_ref._board_dict)
    form_n_connections(reflector_ref, int(len(unpaired_list) / 2))
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


def form_n_connections(reflector_ref: reflectors.Reflector, connections: int):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
        connections (int): _description_
    """
    for i in range(connections):
        clearScreenConvenience()
        print(stringOutput(f"Creating connection {i+1} of {connections}"))
        connect_two_letters(reflector_ref)


def reset_and_streamline_connections_by_pairs(reflector_ref: reflectors.Reflector):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
    """
    reset_connections(reflector_ref)
    while True:
        accbool = input(askingInput("Do you still want to make changes?[y/n]")).lower()
        if accbool == "n":
            returningToMenuNoMessage()
        elif accbool == "y":
            break
    while True:
        connect_two_letters(reflector_ref)


## The board is fully connected (one or fewer letters left unconnected). If wrong choice, go back to start


def reset_and_randomize_connections(reflector_ref: reflectors.Reflector):
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
    reflector_ref._reset_and_randomize_board_dict(seed)


def reset_connections(reflector_ref: reflectors.Reflector):
    """_summary_

    Args:
        reflector_ref (reflectors.Reflector): _description_
    """
    reflector_ref._reset_dictionaries()


def change_reflector_name():
    pass


def save_reflector_in_current_directory():
    pass


_menu_reflector = {
    "1": ("Show current reflector setup", show_board_config),
    "2": ("Delete a single connection", choose_connection_to_delete),
    "3": ("Create a single connection", create_a_connection_single_choice),
    "4": ("Form all connections left", form_all_connections),
    "6": ("Reset and form max. connections", reset_and_streamline_connections_by_pairs),
    "7": ("Reset and randomize connections", reset_and_randomize_connections),
    "8": ("Reset connections", reset_connections),
    "0": ("Exit menu", exitMenu),
}


def main_reflector_menu(machine_ref: machines.Machine):
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
            raise MenuExitException()

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


def save_n_random_reflectors(n, seed):
    # Create and save into pickle objects 20 randomly generated rotors. Use seed to generate new seed, or simply add numbers
    for i in range(0, n):
        reflector = Reflector()
        reflector.random_setup(seed + i)
    return ">Done"


def tune_existing_reflector():
    reflector = Reflector()
    reflector.import_reflector()
    reflector.configure()
    reflector.export_reflector()
    return ">Reflector was edited and saved"
    # Conda activation: conda info --envs, conda activate {}

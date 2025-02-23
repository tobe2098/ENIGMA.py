import string
from denigma.utils.exceptions import FileIOErrorException, ReturnToMenuException
from denigma.utils.types_utils import getLowerCaseName
from denigma.cli.functions.plugboards_f import _show_config_pb
from denigma.cli.functions.rotors_f import _show_config_rt, _load_saved_rotor
from denigma.cli.functions.reflectors_f import _show_config_rf, _load_saved_reflector

from denigma.cli.menus.rotors_m import _menu_rotor
from denigma.cli.menus.reflectors_m import _menu_reflector
from denigma.cli.menus.plugboards_m import _menu_plugboard

from denigma.utils.utils import (
    Constants,
    is_valid_filename,
    is_valid_seed,
)
from denigma.utils.utils_cli import (
    askingInput,
    checkIfFileExists,
    checkInputValidity,
    exitMenu,
    getSeedFromUser,
    printError,
    printListOfOptions,
    printOutput,
    printWarning,
    returningToMenu,
    runNodeMenu,
    _get_a_charlist_from_storage,
)
from denigma.utils.formatting import printListing
from denigma.core import machines

import pandas as pd
import os
import copy
import pickle


# ALL MENUS MUST BE ABLE TO RETURN TO THE PREVIOUS MENU WITH THE SAME KEY
# ALL LOADING FUNCTIONS MUST BE HERE
# PUT A FUNCTION THAT SAVES EACH INDIVIDUAL COMPONENT (EXCEPT THE PLUGBOARDS (AND ROTOR POSITIONS) FOR SAFETY PURPOSES)
def _show_full_config_machine(machine_ref: machines.Machine):
    printOutput("Plugboard config:")
    _show_config_pb(machine_ref._plugboard)
    for i in range(len(machine_ref._rotors)):
        printOutput(f"Rotor {i+1} config:")
        _show_config_rt(machine_ref._rotors[i])
    printOutput("Reflector config:")
    _show_config_rf(machine_ref._reflector)
    printOutput("Characters in use: ", machine_ref.get_charlist())
    printOutput(
        f"The machine is {machine_ref.get_char_distance()} backspaces from its original state"
    )
    # returningToMenu()


def _show_simple_config_machine(machine_ref: machines.Machine):
    config = pd.DataFrame()
    config["Rotor position"] = list(range(1, len(machine_ref._rotors)) + 1)
    config["Rotors"] = [rotor.get_name() for rotor in machine_ref._rotors]
    config["Letter position"] = [rotor._position for rotor in machine_ref._rotors]
    config["Notches"] = [
        rotor.get_notchlist_characters() for rotor in machine_ref._rotors
    ]
    printOutput("Plugboard config:")
    _show_config_pb(machine_ref._plugboard)
    printOutput("Reflector:", machine_ref._reflector.get_name())
    printOutput("Rotor config:")
    print(config)
    printOutput("Machine name:", machine_ref.get_name())
    # returningToMenu()


def _random_setup_single_rotor_machine(machine_ref: machines.Machine):
    printListOfOptions([rotor.get_name() for rotor in machine_ref._rotors])
    rotor_index = askingInput("Input the rotor number (0 to n-1)")
    rotor_index = checkInputValidity(
        rotor_index, int, rangein=(0, machine_ref.get_no_rotors())
    )
    if rotor_index==None:
        returningToMenu("Invalid index", output_type="e")
    seed1 = getSeedFromUser("connections seed")
    seed2 = getSeedFromUser("character position seed")
    seed3 = getSeedFromUser("notches seed")
    machine_ref._rotors[rotor_index]._randomize_dictionaries(seed1)
    machine_ref._rotors[rotor_index]._randomize_notches(seed2)
    machine_ref._rotors[rotor_index]._randomize_position(seed3)
    returningToMenu("The rotor has been randomized with the provided seeds")


def _random_setup_reflector_machine(machine_ref: machines.Machine):
    # printOutput("Careful with your seed choice, if you use the same one you get the same results")
    seed = getSeedFromUser()
    machine_ref._reflector._randomize_dictionaries(seed)
    returningToMenu("Reflector has been randomized with the provided seed")


def _random_setup_reflector_global_seed_machine(machine_ref: machines.Machine):
    if not machine_ref.seed_is_set():
        returningToMenu("No global seed has been set", output_type="e")
    machine_ref._reflector._randomize_dictionaries(machine_ref.get_seed())
    returningToMenu("Reflector has been randomized with the machine's global seed")


def _set_a_global_seed_machine(machine_ref: machines.Machine):
    printOutput(
        "Be aware that your general machine setup is not randomized after you set this seed."
    )
    seed = getSeedFromUser()
    if not is_valid_seed(seed):
        returningToMenu("Not a valid seed", output_type="e")
    machine_ref._change_seed(seed=seed)
    returningToMenu("Global seed has been set")


def _random_setup_all_rotors_machine(machine_ref: machines.Machine):
    if machine_ref.get_seed() <= 0:
        returningToMenu("No global seed has been set", output_type="e")
    jump = getSeedFromUser("seed jump")
    machine_ref._random_setup_all_rotors(jump=jump)
    returningToMenu("All rotors have been randomized")


def _set_new_no_ref_rotors_machine(machine_ref: machines.Machine):
    new_no_rotors = askingInput(
        f"Enter number of new rotors to set in the machine (0 to {Constants.MAX_NO_ROTORS})"
    )
    if new_no_rotors=="":
        returningToMenu()
    new_no_rotors = checkInputValidity(
    new_no_rotors, int, rangein=(1, Constants.MAX_NO_ROTORS + 1)
    )
    if new_no_rotors==None:
        returningToMenu("Invalid input or input is zero", output_type="e")
    machine_ref._set_new_no_rotors(new_no_rotors)
    returningToMenu(
        f"{new_no_rotors} blank rotors have been set as the machine's rotors"
    )


def _append_rotors(machine_ref: machines.Machine):
    # if machine_ref.get_no_rotors() == Constants.MAX_NO_ROTORS:
    #     returningToMenu(
    #         "You reached the maximum number of rotors. Why would you do such a thing?",
    #         "e",
    #     )
    no_rotors_append = askingInput(
        f"Enter number of new rotors to append to the machine (0 to {Constants.MAX_NO_ROTORS-machine_ref.get_no_rotors()})"
    )
    if no_rotors_append=="":
        returningToMenu()
    no_rotors_append = checkInputValidity(
        no_rotors_append,
        int,
        rangein=(1, Constants.MAX_NO_ROTORS - machine_ref.get_no_rotors() + 1),
    )
    if no_rotors_append==None:
        returningToMenu("Invalid input or input is zero", output_type="e")
    machine_ref._append_rotors(no_rotors_append)
    returningToMenu("Rotors appended")


def _load_a_rotor_on_index(machine_ref: machines.Machine, idx):
    # Review, I dont remember if I had to do something extra here
    if machine_ref.is_rotor_index_valid(idx):
        machine_ref._rotors.insert(idx, _load_saved_rotor())
    elif idx > len(machine_ref._rotors):
        machine_ref._rotors.append(_load_saved_rotor())
    else:
        returningToMenu("Invalid input", "e")


def _load_rotors_at_index(machine_ref: machines.Machine):
    # if machine_ref.get_no_rotors() == Constants.MAX_NO_ROTORS:
    #     returningToMenu(
    #         "You reached the maximum number of rotors. Why would you do such a thing?",
    #         "e",
    #     )
    index = 1
    while index:
        index = askingInput(
            f"Choose a valid index where to insert new rotors (0 to {machine_ref.get_no_rotors()-1}) or empty input to return to menu"
        )
        if index=="":
            returningToMenu()
        index = checkInputValidity(index, int, rangein=(0, machine_ref.get_no_rotors()))
        # no_rotors_insert=askingInput(f"Enter number of new rotors to append to the machine (1 to {Constants.MAX_NO_ROTORS-machine_ref.get_no_rotors()})")
        # no_rotors_insert=checkInputValidity(no_rotors_insert, int, range(1, Constants.MAX_NO_ROTORS-machine_ref.get_no_rotors()+1))
        if index==None:
            returningToMenu("Invalid index input", output_type="e")
        if machine_ref.get_no_rotors() == Constants.MAX_NO_ROTORS:
            returningToMenu("Max number of rotors has been reached", output_type="e")
        machine_ref._load_a_rotor_on_index(index)
        printOutput(f"Rotor loaded at index {index}")
    # returningToMenu(f"Rotor loaded at index {index}")


def _load_rotor_for_reference(machine_ref: machines.Machine):
    machine_ref._ref_rotor = _load_saved_rotor()
    returningToMenu("Rotor has been loaded as the reference rotor")


def _change_all_rotors_character_position(machine_ref: machines.Machine):
    # MENU in machine!!! LETTERS HAVE TO BE FROM THE LIST!!!
    printOutput(
        "You can skip the change of character of a rotor by giving any invalid input"
    )
    new_positions = []
    printListOfOptions(machine_ref.get_rotors_and_charpos())
    for i in range(machine_ref.get_no_rotors()):
        # remaining = list(set(range(machine_ref.get_no_rotors())) - set(new_positions))
        # printOutput("Remaining positions are ", remaining)
        new_pos = askingInput(f"Input new character position for rotor {i+1}")
        new_pos = checkInputValidity(new_pos, rangein=machine_ref.get_charlist())
        # while new_pos not in remaining:
        #     printOutput("Remaining positions are ", remaining)
        #     new_pos = askingInput(f"Input new position for rotor {i+1}")
        #     new_pos = checkInputValidity(new_pos, rangein=machine_ref.get_charlist())
        new_positions.append(new_pos)
    # positions_copy = copy.copy(new_positions)
    # positions_copy.sort()
    # if not all(
    #     [machine_ref.is_rotor_index_valid(idx) for idx in new_positions]
    # ) and positions_copy == list(range(machine_ref.get_no_rotors())):
    #     returningToMenu("The positions you provided were not valid", output_type="e")
    # machine_ref._reorder_all_rotors(index_list=new_positions)
    for i in range(new_positions):
        if new_positions[i] in machine_ref.get_charlist():
            machine_ref.change_rotor_char_position(index=i, position=new_positions[i])
    returningToMenu("Rotors positions changed")


def _change_a_rotor_character_position(machine_ref: machines.Machine):
    printOutput("Rotors:")
    printListOfOptions(machine_ref.get_rotors_and_charpos())
    rotor_index = askingInput("Input rotor index to change character position")
    if rotor_index=="":
        returningToMenu()
    rotor_index = checkInputValidity(
        rotor_index, int, rangein=(0, machine_ref.get_no_rotors())
    )
    if rotor_index==None:
        returningToMenu("Invalid input", output_type="e")
    printOutput(
        "Current rotor character position is: ",
        machine_ref.get_rotor_char_pos(rotor_index),
    )
    printOutput("Valid character positions are: ", machine_ref.get_charlist())
    new_char_pos = askingInput("Input new character position")
    if new_char_pos=="":
        returningToMenu()
    new_char_pos = checkInputValidity(new_char_pos, rangein=machine_ref.get_charlist())
    if new_char_pos==None:
        returningToMenu("Invalid input", output_type="e")
    machine_ref.change_rotor_char_position(rotor_index, new_char_pos)
    returningToMenu("Position set")


def _swap_two_rotors(machine_ref: machines.Machine):
    printOutput("Rotors:")
    printListOfOptions(machine_ref.get_rotors_names_ordered())
    rotor1 = askingInput("Input first rotor index to swap")
    rotor2 = askingInput("Input second rotor index to swap")
    if rotor1=="" or rotor2=="":
        returningToMenu()
    rotor1 = checkInputValidity(rotor1, int, (0, machine_ref.get_no_rotors()))
    rotor2 = checkInputValidity(rotor2, int, (0, machine_ref.get_no_rotors()))
    if rotor1==None or rotor2==None:
        returningToMenu("Wrong input", output_type="e")
    machine_ref._swap_two_rotors_by_index(rotor1, rotor2)
    returningToMenu("The two rotors were swapped")


def _reorder_all_rotors(machine_ref: machines.Machine):
    printOutput("Rotors:")
    printListOfOptions(machine_ref.get_rotors_names_ordered())
    printOutput(
        "Remember: smaller indexes are closer to the plugboard, bigger ones closer to the reflector. Last rotor's notches are irrelevant"
    )
    index_list = askingInput(
        "Input the rotor indexes in the desired order, separated by commas"
    )
    index_list = index_list.split(",")
    index_list_copy = []
    for i in index_list:
        if i.isnumeric() and machine_ref.is_rotor_index_valid(int(i)):
            index_list_copy.append(int(i))
        else:
            returningToMenu("Invalid index", output_type="e")
    index_list = copy.copy(index_list_copy)
    index_list_copy.sort()
    if not index_list_copy == list(range(machine_ref.get_no_rotors())):
        returningToMenu("Incomplete index list", output_type="e")
    machine_ref._reorder_all_rotors(index_list=index_list)


def _edit_a_rotors_config(machine_ref: machines.Machine):  ## This is just a menu call
    printOutput("Rotors:")
    printListOfOptions(machine_ref.get_rotors_names_ordered())
    index = askingInput("Choose a rotor to edit its configuration")
    if index=="":
        returningToMenu()
    index = checkInputValidity(index, int, (0, machine_ref.get_no_rotors()))
    if index==None:
        returningToMenu("Invalid input", output_type="e")
    runNodeMenu(machine_ref._rotors[index], _menu_rotor)
    returningToMenu()


def _edit_ref_rotor_config(machine_ref: machines.Machine):  ## This is just a menu call
    runNodeMenu(machine_ref._ref_rotor, _menu_rotor)
    returningToMenu()


def _edit_reflector_config(machine_ref: machines.Machine):
    runNodeMenu(machine_ref._reflector, _menu_reflector)
    returningToMenu()


def _load_reflector(machine_ref: machines.Machine):
    loaded_reflector = _load_saved_reflector()
    # if not loaded_reflector:
    #     returningToMenu("There was an unexpected error") Not possible, either exception or actual reflector
    machine_ref._reflector = loaded_reflector
    returningToMenu("Reflector is loaded")


def _edit_plugboard_config(machine_ref: machines.Machine):
    runNodeMenu(machine_ref._plugboard, _menu_plugboard)
    returningToMenu()


def _set_new_original_state(machine_ref: machines.Machine):
    machine_ref.set_new_original_state()


def _machine_get_message(machine_ref: machines.Machine):
    if not machine_ref._is_machine_set_up():
        returningToMenu(
            "One or more of the machine's components is not properly set up",
            output_type="e",
        )

    ans = ""
    while ans != "y" and ans != "n":
        ans = askingInput(
            "Would you like to read the message from a .txt file?[y/n]"
        ).lower()
    if ans == "y":
        file = askingInput(
            f"Introduce the file's name to be read (without .txt, from {os.getcwd()} only)"
        )
        while not is_valid_filename(file) or not checkIfFileExists(
            os.getcwd(), file, ".txt"
        ):
            printError(f"The file {file}.txt does not exist")
            file = askingInput(
                f"Introduce the file's name to be read (without .txt, from {os.getcwd()} only)"
            )
        text = get_message_from_textfile(file)
    else:
        printOutput(
            "Allowed characters (others WILL be ignored):",
            machine_ref.get_charlist(),
        )
        text = askingInput("Write the desired message")
    return text


def get_message_from_textfile(filename: str):
    text = ""
    try:
        with open(file, "r") as file:
            while True:
                chunk = file.read(1024)  # Read in chunks of 1024 bytes
                if not chunk:
                    break
                # Process the chunk
                text += chunk
    except FileNotFoundError:
        raise FileIOErrorException(f"The file {filename} was not found")
    except IOError as e:
        raise FileIOErrorException(
            f"An error occurred while reading the file {filename}:{e}"
        )
    return text


def _encrypt_decrypt_text_nobackspace(machine_ref: machines.Machine):
    text = _machine_get_message(machine_ref=machine_ref)
    output = ""
    for char in text:
        char = machine_ref.type_character(char)
        output += char
    return output


def _encrypt_decrypt_text_backspace(machine_ref: machines.Machine):
    text = _machine_get_message(machine_ref=machine_ref)
    output = machine_ref.encrypt_decrypt_text(text)
    return output


def _encrypt_decrypt_cliout(machine_ref: machines.Machine):
    ans = ""
    while ans != "y" and ans != "n":
        ans = askingInput(
            "Would you like to return to the current state once the message is passed?[y/n]"
        ).lower()
    if ans == "y":
        message = _encrypt_decrypt_text_backspace(machine_ref=machine_ref)
        returningToMenu("The machine's output is: ", message)
    else:
        message = _encrypt_decrypt_text_nobackspace(machine_ref=machine_ref)
        returningToMenu("The machine's output is: ", message)


def _encrypt_decrypt_fileout(machine_ref: machines.Machine, filepath=None):
    if not filepath:
        filepath = askingInput(
            "Give a new filename to store your message as a text file in the current directory"
        )
        if not is_valid_filename(filepath):
            returningToMenu("Invalid filename", output_type="e")
        filepath += ".txt"
        filepath = os.path.join(os.getcwd(), filepath)
    ans = ""
    while ans != "y" and ans != "n":
        ans = askingInput(
            "Would you like to return to the current state once the message is passed?[y/n]"
        ).lower()
    message = ""
    prev_state = machine_ref.get_char_distance()
    if ans == "y":
        message = _encrypt_decrypt_text_backspace(machine_ref=machine_ref)
    else:
        message = _encrypt_decrypt_text_nobackspace(machine_ref=machine_ref)
    try:
        with open(filepath, "w") as file:
            file.write(message)
    except Exception as e:
        if ans == "n":
            machine_ref.backspace_to_original_state_or_destination(prev_state)
        printError(f"Failed to write to file: {e}")
        returningToMenu(f"Message output is: {message}")
    returningToMenu(f"Message stored in {filepath}")


# def _backspace_machine(machine_ref: machines.Machine):
#     printOutput(
#         f"The machine is currently {machine_ref.get_char_distance()} backspaces away from the original state"
#     )
#     backspaces = askingInput("Give the number of intended backspaces (whole number)")
#     backspaces = checkInputValidity(backspaces, int, (0, Constants.MAX_NO_BACKSPACES))


def _backspace_machine_to_origin(machine_ref: machines.Machine):
    machine_ref.backspace_to_original_state_or_destination()
    returningToMenu("Returned to original state")


def _change_machine_state_respect_to_origin(machine_ref: machines.Machine):
    printOutput(
        f"The machine is currently {machine_ref.get_char_distance()} backspaces away from the original state"
    )
    steps = askingInput(
        "Choose the target number of backspaces away from the original state"
    )
    if steps=="":
        returningToMenu()
    steps = checkInputValidity(steps, int)
    if steps==None:
        returningToMenu("Invalid input", output_type="e")
    machine_ref.backspace_to_original_state_or_destination(
        steps - machine_ref.get_char_distance()
    )
    returningToMenu(
        f"The machine is currently {machine_ref.get_char_distance()} backspaces away from the original state"
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


def _save_machine_in_its_folder(machine_ref: machines.Machine,menu_call=True):
    accbool = ""
    if menu_call:
        accbool="y"
    while not accbool == "n" and not accbool == "y":
        accbool = askingInput(
            f"Would you like to save the machine in use? If not, unsaved changes will be discarded. [y/n]"
        ).lower()
    if accbool == "n":
        returningToMenu()
    if not machine_ref._do_objects_have_identical_charlists():
        returningToMenu(
            "Not all parts of the machine share the same character list", output_type="e"
        )
    new_name = machine_ref.get_name()
    while not machine_ref._is_name_valid(new_name):
        new_name = askingInput(
            f"Please assign a new name to the {getLowerCaseName(machine_ref)}"
        ).strip(string.whitespace)
    machine_ref._change_name(new_name)

    path = Constants.MACHINE_FILE_PATH
    if not os.path.exists(path):
        os.mkdir(path)
        printOutput("Directory '% s' created" % path)
    if checkIfFileExists(path, machine_ref._name, getLowerCaseName(machine_ref)):
        printOutput(f"A {getLowerCaseName(machine_ref)} with this name already exists")
        accbool = ""
        while not accbool == "n" and not accbool == "y":
            accbool = askingInput(
                f"Do you want to overwrite the saved {getLowerCaseName(machine_ref)}? [y/n]"
            ).lower()
        if accbool == "n":
            returningToMenu()
    file_path = os.path.join(
        path, f"{machine_ref._name}.{getLowerCaseName(machine_ref)}"
    )
    try:
        save_file = open(file_path, "wb")
        pickle.dump(machine_ref, save_file)
        save_file.close()
    except Exception as e:
        returningToMenu(f"Failed to write on {file_path}:{e}")
    returningToMenu(
        f"{machine_ref.get_name()} has been saved into {machine_ref.get_name()}.{getLowerCaseName(machine_ref)} in {path}"
    )


def _randomize_entire_machine(machine_ref: machines.Machine):
    if machine_ref and machine_ref._do_objects_have_identical_charlists():
        try:
            _save_machine_in_its_folder(machine_ref=machine_ref, menu_call=False)
        except ReturnToMenuException as e:
            pass
    printWarning("The previous global seed will be replaced by the seed you input")
    seed = getSeedFromUser()
    no_rotors = askingInput("Input desired number of rotors (empty for same number)")
    no_rotors = checkInputValidity(no_rotors, int, (1, Constants.MAX_NO_ROTORS + 1))
    machine_ref.setup_machine_randomly(seed, no_rotors or machine_ref.get_no_rotors())
    returningToMenu(
        f"The machine's seed has been replaced and its settings have been set according to that seed, with {no_rotors or machine_ref.get_no_rotors()} rotors"
    )


def _re_randomize_with_global_seed_machine(machine_ref: machines.Machine):
    if machine_ref and machine_ref._do_objects_have_identical_charlists():
        try:
            _save_machine_in_its_folder(machine_ref=machine_ref,menu_call=False)
        except ReturnToMenuException as e:
            pass
    if not machine_ref.seed_is_set():
        returningToMenu("No global seed has been set", output_type="e")
    machine_ref.setup_machine_randomly(
        machine_ref.get_seed(), machine_ref.get_no_rotors()
    )
    returningToMenu("The machine's settings have been set according to the global seed")


def _load_saved_machine(machine_ref: machines.Machine | None = None):
    if machine_ref and machine_ref._do_objects_have_identical_charlists():
        try:
            _save_machine_in_its_folder(machine_ref=machine_ref,menu_call=False)
        except ReturnToMenuException as e:
            pass
    module_path = Constants.MODULE_PATH
    new_folder = Constants.MACHINES_FILE_HANDLE
    path = os.path.join(module_path, new_folder)
    if not os.path.exists(path):
        returningToMenu(f"There is no {path} folder", output_type="e")
    list_of_files = [
        element.rsplit(".", 1)[0] for element in os.listdir(path)
    ]  # if element.rsplit(".", 1)[1] == "machine"]
    if not list_of_files:
        returningToMenu("There are no machines saved", output_type="e")
    printListing("Your available machines are")
    printListOfOptions(list_of_files)
    machine = askingInput("Input machine's position in the list")
    if machine=="":
        returningToMenu()
    machine = checkInputValidity(machine, int, rangein=(0, len(list_of_files)))
    while machine==None:
        # while not isinstance(rotor, int) or rotor > len(list_of_files) - 1 or rotor < 0:
        printError("Please input a valid index")
        printListOfOptions(list_of_files)
        machine = askingInput("Input rotor's position in the list:")
        if machine=="":
            returningToMenu()
        machine = checkInputValidity(machine, int, rangein=(0, len(list_of_files)))
    file = os.path.join(path, f"{list_of_files[machine]}.machine")
    try:
        filehandler = open(file, "rb")
        machine_ref = pickle.load(filehandler)
        filehandler.close()
    except Exception as e:
        returningToMenu(f"Failed to open file {file}:{e}")
    if isinstance(machine_ref, machines.Machine):
        return machine_ref  # End
    else:
        returningToMenu(
            f"A non-machine type was loaded:{type(machine_ref)}", output_type="e"
        )


def _create_a_new_random_machine(machine_ref: machines.Machine | None = None):
    if machine_ref and machine_ref._do_objects_have_identical_charlists():
        try:
            _save_machine_in_its_folder(machine_ref=machine_ref,menu_call=False)
        except ReturnToMenuException as e:
            pass
    seed = getSeedFromUser()
    charlist = _get_a_charlist_from_storage()
    machine_ref = machines.Machine(
        seed=seed,
        charlist=charlist,
    )
    noRotors = askingInput(
        f"Input the desired number of rotors for your machine (from 1 to {Constants.MAX_NO_ROTORS})"
    )
    if noRotors=="":
        returningToMenu()
    noRotors=checkInputValidity(noRotors, int, (1,Constants.MAX_NO_ROTORS))
    while noRotors==None:
        noRotors = askingInput(
        f"Input the a valid number of rotors for your machine (from 1 to {Constants.MAX_NO_ROTORS})"
    )
        if noRotors=="":
            returningToMenu()
        noRotors=checkInputValidity(noRotors, int, (1,Constants.MAX_NO_ROTORS))
    machine_ref.setup_machine_randomly(noRotors=noRotors)
    return machine_ref


def _create_a_new_machine_from_scratch(machine_ref: machines.Machine | None = None):
    if machine_ref and machine_ref._do_objects_have_identical_charlists():
        try:
            _save_machine_in_its_folder(machine_ref=machine_ref,menu_call=False)
        except ReturnToMenuException as e:
            pass
    machine_ref = machines.Machine()
    return machine_ref


# def generate_n_random_reflectors(n, seed: int):
#     # Create and save into pickle objects 20 randomly generated rotors. Use seed to generate new seed, or simply add numbers
#     for index in range(0, n):
#         reflector = reflector.Reflector()
#         reflector.random_name(seed + index)
#         reflector.random_setup(seed + index)
#     utils_cli.printOutput(f"Created and saved {n} rotors.")


def exitMenu_machine(machine_ref: machines.Machine):
    if machine_ref and machine_ref._do_objects_have_identical_charlists():
        try:
            _save_machine_in_its_folder(machine_ref=machine_ref,menu_call=False)
        except ReturnToMenuException as e:
            pass
    # if CONFIG.SETUP
    exitMenu()

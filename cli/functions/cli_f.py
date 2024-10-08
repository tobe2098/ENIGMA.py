import json

from cli.menus.machines_m import _outer_menu_machine
from cli.functions.reflectors_f import _load_saved_reflector
from cli.functions.rotors_f import _load_saved_rotor
from cli.functions.machines_f import (
    _load_saved_machine,
    _create_a_new_machine_from_scratch,
    _create_a_new_random_machine,
)
from core.machines import Machine
from utils.utils import (
    Constants,
    get_charlist_json,
    get_config_json,
    save_charlist_json,
    _asign_defaults_to_config_json,
    save_config_json,
)
from ...utils.utils_cli import (
    askingInput,
    checkInputValidity,
    get_a_charlist_and_name_from_user,
    printError,
    printListOfOptions,
    printOutput,
    printWarning,
    returningToMenu,
    runNodeMenu,
)


def load_a_machine():
    machine_ref = _load_saved_machine()
    runNodeMenu(machine_ref, _outer_menu_machine)
    returningToMenu()


def create_a_new_machine_from_scratch_and_use():
    machine_ref = _create_a_new_machine_from_scratch()
    runNodeMenu(machine_ref, _outer_menu_machine)
    returningToMenu()


def create_a_new_random_machine():
    machine_ref = _create_a_new_random_machine()
    runNodeMenu(machine_ref, _outer_menu_machine)
    returningToMenu()


def _print_charlist_collection(dictionary=None):
    if not dictionary:
        dictionary = get_charlist_json()
    name_list = list(dictionary.keys())
    printListOfOptions(name_list)
    return name_list


def _store_and_return_a_new_charlist():
    charlist, name = get_a_charlist_and_name_from_user()
    dictionary = get_charlist_json()
    dictionary[name] = charlist
    with open(Constants.CHARLISTS_FILE_PATH) as file:
        json.dump(dictionary, file, indent=2)
    return charlist  # Only to be used if called with that intention


def _delete_a_charlist():
    dictionary = get_charlist_json()
    name_list = _print_charlist_collection(dictionary=dictionary)
    printWarning("Default character lists cannot be deleted")
    name_index = askingInput("Input the index of the character list to be deleted")
    if not name_index:
        returningToMenu()
    name_list = checkInputValidity(name_index, int, (0, len(name_list)))
    while not name_list:
        name_index = askingInput("Input a valid index")
        if not name_index:
            returningToMenu()
        name_list = checkInputValidity(name_index, int, (0, len(name_list)))
    dictionary.pop(name_list[name_index])
    save_charlist_json(dictionary=dictionary)
    returningToMenu("Character list was deleted")


def _print_a_particular_character_list():
    printOutput(_get_a_charlist_from_storage())


def _get_a_charlist_from_storage():
    dictionary = get_charlist_json()
    name_list = _print_charlist_collection(dictionary=dictionary)
    name_index = askingInput("Input the index of the desired character list")
    if not name_index:
        returningToMenu()
    name_list = checkInputValidity(name_index, int, (0, len(name_list)))
    while not name_list:
        name_index = askingInput("Input a valid index")
        if not name_index:
            returningToMenu()
        name_list = checkInputValidity(name_index, int, (0, len(name_list)))
    return dictionary[name_list[name_index]]


def _print_help():
    print("Help")
    print("Args for file/text in/out, and defaults")
    print("-f from file, -c from cli, then -tf + destination file or -tc")


def _set_defaults_config():
    config = get_config_json()
    _asign_defaults_to_config_json(dictionary=config)
    save_config_json(dictionary=config)
    returningToMenu("Configuration was reset to the defaults")


def _set_cli_machine():
    config = get_config_json()
    # Get list of saved machines, and offer choice
    # If success, set machine and set =true
    # If not, just return


def _unset_cli_machine():
    config = get_config_json()
    # Easy, unset the machine so that it changes to the last used machine


def _set_machine_unset_case(machine_ref: Machine):
    config = get_config_json()
    # Check if the machine is saved in its current state, then set that name for later retrieval.
    if not config["is_machine_set"]:
        config["set_machine"] = machine_ref.get_name()


def _load_set_machine():
    config = get_config_json()
    if not config["set_machine"]:
        printError("There is no machine set")


def _encrypt_decrypt_text_to_cli():
    # Always return to original position
    pass


def _encrypt_decrypt_text_to_file_cli():
    # Always return to original position
    pass


def _encrypt_decrypt_file_to_cli():
    # Always return to original position
    pass


def _encrypt_decrypt_file_to_file_cli():
    # Always return to original position
    pass


# def export_an_existing_reflector():
#     path_to_export = os.getcwd()
#     reflector_ref = _load_saved_reflector()
#     new_name = reflector_ref.get_name()
#     while not reflector_ref._is_name_valid(new_name):
#         new_name = askingInput(
#             f"Please assign a new name to the {getLowerCaseName(reflector_ref)}"
#         ).strip(chars=string.whitespace)
#     reflector_ref._change_name(new_name)

#     if checkIfFileExists(
#         path_to_export, reflector_ref._name, getLowerCaseName(reflector_ref)
#     ):
#         printOutput(
#             f"A {getLowerCaseName(reflector_ref)} with this name already exists"
#         )
#         accbool = ""
#         while not accbool == "n" or not accbool == "y":
#             accbool = askingInput(
#                 f"Do you want to overwrite the saved {getLowerCaseName(reflector_ref)}? [y/n]"
#             ).lower()
#         if accbool == "n":
#             returningToMenu(
#                 f"You did not overwrite the {getLowerCaseName(reflector_ref)}"
#             )
#     file_path = os.path.join(
#         path_to_export, f"{reflector_ref._name}.{getLowerCaseName(reflector_ref)}"
#     )
#     try:
#         save_file = open(file_path, "wb")
#         pickle.dump(reflector_ref, save_file)
#         save_file.close()
#     except Exception as e:
#         raise FileIOErrorException(
#             f"Failed to export the {getLowerCaseName(reflector_ref)} at {file_path}:{e}"
#         )
#     returningToMenu(
#         f"{reflector_ref._name} has been exported into {reflector_ref._name}.{getLowerCaseName(reflector_ref)} in {path_to_export}"
#     )


# def export_an_existing_rotor():
#     path_to_export = os.getcwd()
#     rotor_ref = _load_saved_rotor()
#     new_name = rotor_ref.get_name()
#     while not rotor_ref._is_name_valid(new_name):
#         new_name = askingInput(
#             f"Please assign a new name to the {getLowerCaseName(rotor_ref)}"
#         ).strip(chars=string.whitespace)
#     rotor_ref._change_name(new_name)

#     if not os.path.exists(path_to_export):
#         os.mkdir(path_to_export)
#         printOutput(f"Directory '{path_to_export}' created")
#     if checkIfFileExists(path_to_export, rotor_ref._name, getLowerCaseName(rotor_ref)):
#         printOutput(f"A {getLowerCaseName(rotor_ref)} with this name already exists")
#         accbool = ""
#         while not accbool == "n" or not accbool == "y":
#             accbool = askingInput(
#                 f"Do you want to overwrite the saved {getLowerCaseName(rotor_ref)}? [y/n]"
#             ).lower()
#         if accbool == "n":
#             returningToMenu(
#                 f"You discarded changes to the {getLowerCaseName(rotor_ref)}"
#             )
#     file_path = os.path.join(
#         path_to_export, f"{rotor_ref._name}.{getLowerCaseName(rotor_ref)}"
#     )
#     try:
#         save_file = open(file_path, "wb")
#         pickle.dump(rotor_ref, save_file)
#         save_file.close()
#     except Exception as e:
#         raise FileIOErrorException(
#             f"Failed to save the {getLowerCaseName(rotor_ref)} at {file_path}:{e}"
#         )
#     returningToMenu(
#         f"{rotor_ref._name} has been saved into {rotor_ref._name}.{getLowerCaseName(rotor_ref)} in {path_to_export}"
#     )


# def export_an_existing_machine():
#     path_to_export = os.getcwd()
#     machine_ref = _load_saved_machine()
#     if not machine_ref._do_objects_have_identical_charlists():
#         returningToMenu(
#             "Not all parts of the machine share the same character list", "e"
#         )
#     new_name = machine_ref.get_name()
#     while not machine_ref._is_name_valid(new_name):
#         new_name = askingInput(
#             f"Please assign a new name to the {getLowerCaseName(machine_ref)}"
#         ).strip(chars=string.whitespace)
#     machine_ref._change_name(new_name)

#     if checkIfFileExists(
#         path_to_export, machine_ref._name, getLowerCaseName(machine_ref)
#     ):
#         printOutput(f"A {getLowerCaseName(machine_ref)} with this name already exists")
#         accbool = ""
#         while not accbool == "n" or not accbool == "y":
#             accbool = askingInput(
#                 f"Do you want to overwrite the exported {getLowerCaseName(machine_ref)}? [y/n]"
#             ).lower()
#         if accbool == "n":
#             returningToMenu()
#     file_path = os.path.join(
#         path_to_export, f"{machine_ref._name}.{getLowerCaseName(machine_ref)}"
#     )
#     try:
#         save_file = open(file_path, "wb")
#         pickle.dump(machine_ref, save_file)
#         save_file.close()
#     except Exception as e:
#         returningToMenu(f"Failed to write on {file_path}:{e}")
#     returningToMenu(
#         f"{machine_ref.get_name()} has been saved into {machine_ref.get_name()}.{getLowerCaseName(machine_ref)} in {path_to_export,}"
#     )


# def export_an_existing_charlist():
#     pass

# def import_a_charlist():
#     pass

###

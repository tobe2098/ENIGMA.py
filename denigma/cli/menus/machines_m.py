# ALL MENUS MUST BE ABLE TO RETURN TO THE PREVIOUS MENU WITH THE SAME KEY?????
# ALL LOADING FUNCTIONS MUST BE HERE to load on the machine
# PUT A FUNCTION THAT SAVES EACH INDIVIDUAL COMPONENT to memory (EXCEPT THE PLUGBOARDS (AND ROTOR POSITIONS) FOR SAFETY PURPOSES)
from denigma.utils.utils_cli import exitMenu
from denigma.utils.utils import Constants
from denigma.cli.functions.machines_f import (
    _append_rotors,  # Rotor
    _change_all_rotors_character_position,  # Rotor
    _change_a_rotor_character_position,  # Rotor
    _backspace_machine_to_origin,  # Misc
    _change_machine_state_respect_to_origin,  # Misc
    _edit_a_rotors_config,  # Rotor
    _edit_plugboard_config,  # Reflector and plugboard
    _edit_ref_rotor_config,  # Rotor
    _edit_reflector_config,  # Reflector and plugboard
    _encrypt_decrypt_cliout,  # Outer
    _encrypt_decrypt_fileout,  # Outer
    _load_rotors_at_index,  # Rotor
    _set_new_no_ref_rotors_machine,  # Rotor
    _set_new_original_state,  # Misc
    _load_reflector,  # Reflector and plugboard
    _random_setup_all_rotors_machine,  # Random
    _random_setup_reflector_global_seed_machine,  # Random
    _random_setup_reflector_machine,  # Random
    _random_setup_single_rotor_machine,  # Random
    _randomize_entire_machine,  # Random
    _re_randomize_with_global_seed_machine,  # Random
    _reorder_all_rotors,  # Rotors
    _save_machine_in_its_folder,  # Outer
    _set_a_global_seed_machine,  # Random
    _show_full_config_machine,  # Outer
    _show_simple_config_machine,  # Outer
    _swap_two_rotors,  # Rotors
    exitMenu_machine,  # Outer
)


_menu_machines_rotors = {
    Constants.menu_id_string: "Rotors",
    "1": (
        "Edit the configuration of a rotor",
        _edit_a_rotors_config,
    ),
    "2": (
        "Edit the configuration of the reference rotor",
        _edit_ref_rotor_config,
    ),
    "3": ("Append reference rotors", _append_rotors),
    "4": ("Load saved rotors at any index of the rotor array", _load_rotors_at_index),
    "5": (
        "Change the character position of a rotor",
        _change_a_rotor_character_position,
    ),
    "6": (
        "Change the character position of all rotors",
        _change_all_rotors_character_position,
    ),
    "7": ("Swap the order of two rotors", _swap_two_rotors),
    "8": ("Reorder all rotors", _reorder_all_rotors),
    "9": (
        "Overwrite rotors with a number of reference rotors",
        _set_new_no_ref_rotors_machine,
    ),
    "10": ("Randomize a single rotor", _random_setup_single_rotor_machine),
    "11": ("Randomize all rotors", _random_setup_all_rotors_machine),
    "0": ("Exit menu", exitMenu),
}
_menu_machines_reflector_plugboard = {
    Constants.menu_id_string: "Reflector and plugboard",
    "1": ("Edit plugboard configuration", _edit_plugboard_config),
    "2": ("Edit reflector configuration", _edit_reflector_config),
    "3": ("Load a saved reflector", _load_reflector),
    "4": ("Randomize the setup of the reflector", _random_setup_reflector_machine),
    "5": (
        "Randomize the setup of the reflector using the machine's seed",
        _random_setup_reflector_global_seed_machine,
    ),
    "0": ("Exit menu", exitMenu),
}
_menu_miscellaneous = {
    Constants.menu_id_string: "Miscellaneous",
    "1": (
        "Set a new initial character position of the machine",
        _set_new_original_state,
    ),
    "2": (
        "Backspace to initial character position",
        _backspace_machine_to_origin,
    ),
    "3": (
        "Change machine's state respect to initial character position",
        _change_machine_state_respect_to_origin,
    ),
    "4": ("Show full configuration of the machine", _show_full_config_machine),
    "5": ("Show simplified configuration of the machine", _show_simple_config_machine),
    "0": ("Exit menu", exitMenu),
}

_outer_menu_machine = {
    Constants.menu_id_string: "Machine",
    "1": ("Save machine", _save_machine_in_its_folder),
    "2": ("Access plugbaord and reflector menu", _menu_machines_reflector_plugboard),
    "3": ("Access rotor menu", _menu_machines_rotors),
    "4": ("Access miscellaneous menu", _menu_miscellaneous),
    "5": ("Encrypt or decrypt message, console output", _encrypt_decrypt_cliout),
    "6": ("Encrypt or decrypt message, file output", _encrypt_decrypt_fileout),
    "7": ("Set a different global seed for the machine", _set_a_global_seed_machine),
    "8": (
        "Randomize all machine settings (CAUTION: Hard to reverse)",
        _randomize_entire_machine,
    ),
    "9": (
        "Re-randomize machine with global seed (CAUTION: Hard to reverse)",
        _re_randomize_with_global_seed_machine,
    ),
    "0": ("Exit menu", exitMenu_machine),
}  # Here we have a 1. Use machine, 2. Create a new one, etc, 9. discard (exit without saving).

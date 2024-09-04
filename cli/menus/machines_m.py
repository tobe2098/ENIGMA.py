# ALL MENUS MUST BE ABLE TO RETURN TO THE PREVIOUS MENU WITH THE SAME KEY?????
# ALL LOADING FUNCTIONS MUST BE HERE to load on the machine
# PUT A FUNCTION THAT SAVES EACH INDIVIDUAL COMPONENT to memory (EXCEPT THE PLUGBOARDS (AND ROTOR POSITIONS) FOR SAFETY PURPOSES)
from ..functions.machines_f import (
    _append_rotors,  # Rotor
    _change_all_rotors_character_position,  # Rotor
    _change_a_rotor_character_position,  # Rotor
    _backspace_machine_to_origin,  # Misc
    _change_machine_state_respect_to_origin,  # Misc
    _create_a_new_machine_from_scratch,  # Replace
    _create_a_new_random_machine,  # Replace
    _edit_a_rotors_config,
    _edit_plugboard_config,
    _edit_ref_rotor_config,
    _edit_reflector_config,
    _encrypt_decrypt_cliout,
    _encrypt_decrypt_fileout,
    _load_rotors_at_index,
    _load_saved_reflector,
    _set_new_no_blank_rotors_machine,
    _set_new_original_state,
    _get_a_charlist_from_storage,
    _load_machine,
    _load_reflector,
    _machine_get_message,
    _random_setup_all_rotors_machine,
    _random_setup_reflector_global_seed_machine,
    _random_setup_reflector_machine,
    _random_setup_single_rotor_machine,
    _randomize_entire_machine,
    _re_randomize_with_global_seed_machine,
    _reorder_all_rotors,
    _save_machine_in_its_folder,
    _set_a_global_seed_machine,
    _show_full_config_machine,
    _show_simple_config_machine,
)


_menu_machines_rotors = {}
_menu_machines_reflector = {}
_menu_machines_plugboard = {}
_menu_miscellaneous = {}

_menu_encrypt_decrypt = {}

_menu_saving_and_loading_machines = {}
_outer_menu_machine = (
    {}
)  # Here we have a 1. Use machine, 2. Create a new one, etc, 9. discard (exit without saving).

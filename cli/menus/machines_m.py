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
)


_menu_machines_rotors = {}
_menu_machines_reflector = {}
_menu_machines_plugboard = {}
_menu_miscellaneous = {}

_menu_encrypt_decrypt = {}

_menu_saving_and_loading_machines = {}
_outer_menu_machine = {}

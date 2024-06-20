from ..utils.exceptions import raiseBadInputException
from ..core.machines import Machine
from ..core.rotors import Rotor
from ..core.reflectors import Reflector
from ..core.plugboards import PlugBoard
from ..utils.utils import Constants


def getCapitalizedName(obj_ref):
    """The function's purpose is to avoid errors in output and file paths during development.

    Args:
        obj_ref (Custom_Object): python object reference of a part of an ENIGMA machine or an ENIGMA machine

    Raises:
        Exception: if called without one of the relevant types

    Returns:
        str: name of the object capitalized
    """
    return getLowerCaseName(obj_ref).capitalize()


def getUpperCaseName(obj_ref):
    """The function's purpose is to avoid errors in output and file paths during development.

    Args:
        obj_ref (Custom_Object): python object reference of a part of an ENIGMA machine or an ENIGMA machine

    Raises:
        Exception: if called without one of the relevant types

    Returns:
        str: name of the object in uppercase
    """
    return getLowerCaseName(obj_ref).upper()


def getLowerCaseName(obj_ref):
    """The function's purpose is to avoid errors in output and file paths during development.

    Args:
        obj_ref (Custom_Object): python object reference of a part of an ENIGMA machine or an ENIGMA machine

    Raises:
        Exception: if called without one of the relevant types

    Returns:
        str: name of the object in lowercase
    """
    if isinstance(obj_ref, Machine):
        return "machine"
    elif isinstance(obj_ref, Rotor):
        return "rotor"
    elif isinstance(obj_ref, Reflector):
        return "reflector"
    elif isinstance(obj_ref, PlugBoard):
        return "plugboard"
    else:
        raise raiseBadInputException()


def isDashedObject(obj_ref):
    """Returns a boolean on whether the object is the version with a dash in the dictionaries or not.
    Why do it this way? It would be quicker to just check the length of the dictionary or number of characters,
    but that could be changed by you if you are using a personalized script. This is intended as a safety measure for you.
    For the same reason, the usage of non-Dash objects cannot be mixed with Dash objects, as it would not work properly.

    Args:
        obj_ref (Custom_Object): python object reference of a part of an ENIGMA machine or an ENIGMA machine

    Raises:
        Exception: if called without one of the relevant types

    Returns:
        bool: Whether the object is using the extended dictionary
    """
    return obj_ref._conversion_in_use == Constants.EQUIVALENCE_DICT_dash

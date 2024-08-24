from ..utils.exceptions import raiseBadInputException
from ..core.machines import Machine
from ..core.rotors import Rotor
from ..core.reflectors import Reflector
from ..core.plugboards import PlugBoard


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

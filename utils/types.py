from ..core.machines import Machine, MachineDash
from ..core.rotors import Rotor, RotorDash
from ..core.reflectors import Reflector, ReflectorDash
from ..core.plugboards import PlugBoard, PlugBoardDash


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
        raise Exception("An unexpected object was used in getLowerCaseName")


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
    if (
        not isinstance(obj_ref, Machine)
        and not isinstance(obj_ref, Rotor)
        and not isinstance(obj_ref, Reflector)
        and not isinstance(obj_ref, PlugBoard)
    ):
        raise Exception("An unexpected object was used in isDashedObject")
    return (
        isinstance(obj_ref, MachineDash)
        or isinstance(obj_ref, RotorDash)
        or isinstance(obj_ref, ReflectorDash)
        or isinstance(obj_ref, PlugBoardDash)
    )

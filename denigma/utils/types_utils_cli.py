from .exceptions import raiseBadInputException
from core.machines import Machine
from core.rotors import Rotor
from core.reflectors import Reflector
from core.plugboards import PlugBoard

from denigma.cli.functions.rotors_f import _print_name_rt


def wrapperCall(obj_ref):
    if isinstance(obj_ref, Machine):
        machineWrapper(obj_ref)
    elif isinstance(obj_ref, Rotor):
        rotorWrapper(obj_ref)
    elif isinstance(obj_ref, Reflector):
        reflectorWrapper(obj_ref)
    elif isinstance(obj_ref, PlugBoard):
        plugboardWrapper(obj_ref)
    else:
        raise Exception("An unexpected object was used in wrapperCall")


def rotorWrapper(rotor_ref):
    _print_name_rt(rotor_ref)


def machineWrapper(machine_ref):
    raiseBadInputException()


def reflectorWrapper(reflector_ref):
    raiseBadInputException()


def plugboardWrapper(plugboard_ref):
    raiseBadInputException()

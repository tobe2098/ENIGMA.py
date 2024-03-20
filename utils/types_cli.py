from utils.utils_cli import DevOpsException
from ..core.machines import Machine, MachineDash
from ..core.rotors import Rotor, RotorDash
from ..core.reflectors import Reflector, ReflectorDash
from ..core.plugboards import PlugBoard, PlugBoardDash

from ..cli.functions.rotors_f import _show_config_rt


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
    _show_config_rt(rotor_ref)


def machineWrapper(machine_ref):
    raise DevOpsException("Incomplete")


def reflectorWrapper(reflector_ref):
    raise DevOpsException("Incomplete")


def plugboardWrapper(plugboard_ref):
    raise DevOpsException("Incomplete")

from utils_cli import formatAsOutput
import traceback
from main import get_is_cli_mode, get_is_gui_mode


class ExceptionOfExceptions(Exception):
    def __init__(
        self,
        message="Somehow you are not running CLI or GUI and you raised an exception",
    ):
        super().__init__(formatAsOutput(message))


class MenuExitException(Exception):
    def __init__(self, message="Exiting menu..."):
        super().__init__(formatAsOutput(message))


class ReturnToMenuException(Exception):
    def __init__(self, message="Returning to menu..."):
        super().__init__(formatAsOutput(message))


class DevOpsExceptionCLI(ReturnToMenuException):
    def __init__(self, message=None):
        super().__init__(message)
        self.type_msg += "\n" + formatAsOutput(
            "Development oversight. Something happened here:"
        )
        self.traceback = traceback.format_exc()

    def __str__(self):
        return f"{super().__str__()}\n{self.type_msg}\nTraceback:\n{self.traceback}"


class BadInputExceptionCLI(DevOpsExceptionCLI):
    def __init__(self, message=None):
        self.type_msg = formatAsOutput(
            "An incorrect input was received in the following core function:"
        )
        super().__init__(message)


def raiseBadInputException():
    if get_is_cli_mode():
        raise BadInputExceptionCLI()
    elif get_is_gui_mode():
        raise ExceptionOfExceptions()
    else:
        raise ExceptionOfExceptions()

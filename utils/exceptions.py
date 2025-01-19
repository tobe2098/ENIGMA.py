import traceback
from .formatting import formatAsError, formatAsOutput
from .utils import get_is_cli_mode, get_is_gui_mode


class ExceptionOfExceptions(Exception):
    def __init__(
        self,
        message=formatAsOutput(
            "Somehow you are not running CLI or GUI and you raised an exception"
        ),
    ):
        super().__init__(message)


class FileIOErrorException(Exception):
    def __init__(self, message=("Failed to save file")):
        super().__init__(formatAsError(message))


class MenuExitException(Exception):
    def __init__(self, message=formatAsOutput("Exiting menu...")):
        super().__init__(message)


class ReturnToMenuException(Exception):
    def __init__(self, message=formatAsOutput("Returning to menu...")):
        super().__init__(message)


class DevOpsExceptionCLI(ReturnToMenuException):
    def __init__(self, message=None):
        # message += "\n" + formatAsError(
        #     "Development oversight. Something happened here:"
        # )
        super().__init__(message)
        self.traceback = traceback.format_exc()

    def __str__(self):
        return f"{super().__str__()}\n{self.type_msg}\nTraceback:\n{self.traceback}"


class BadInputExceptionCLI(DevOpsExceptionCLI):
    def __init__(self, message=None):
        message += "\n" + formatAsError(
            "An incorrect input was received in the following core function:"
        )
        super().__init__(message)


class MachineBadSetupExceptionCLI(DevOpsExceptionCLI):
    def __init__(self, message=None):
        message += "\n" + formatAsError("The machine was not properly set up")
        super().__init__(message)


def raiseBadInputException():
    if get_is_cli_mode():
        raise BadInputExceptionCLI()
    elif get_is_gui_mode():
        raise ExceptionOfExceptions()
    else:
        raise ExceptionOfExceptions()


def raiseBadSetupException():
    if get_is_cli_mode():
        raise MachineBadSetupExceptionCLI()
    elif get_is_gui_mode():
        raise ExceptionOfExceptions()
    else:
        raise ExceptionOfExceptions()

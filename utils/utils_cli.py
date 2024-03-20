import os
from subprocess import call
from utils.utils import is_valid_seed
import traceback
from utils.types_cli import wrapperCall

SCREEN_CLEAR_CONVENIENCE = True
SCREEN_CLEAR_SAFETY = True


def askForMenuOption():
    return askingInput("Choose a menu option: ")


def formatOutput(*args):
    return ">" + args + "."


def printOutput(*args):
    print(">", args, end=".")


def askingInput(*args):
    return input(">>>", args, end=" ")


def printMenuOption(*args):
    print(">$ ", args)


class MenuExitException(Exception):
    def __init__(self, message=formatOutput("Exiting menu...")):
        super().__init__(self.message)


class ReturnToMenuException(Exception):
    def __init__(self, message=formatOutput("Returning to menu...")):
        super().__init__(message)


class DevOpsException(ReturnToMenuException):
    def __init__(
        self, message=formatOutput("Development oversight. Returning to menu...")
    ):
        super().__init__(message)
        self.traceback = traceback.format_exc()

    def __str__(self):
        return f"{super().__str__()}\nTraceback:\n{self.traceback}"


def exitMenu(*args):
    raise MenuExitException()


def returningToMenuMessage(*args):
    printOutput(args)
    raise ReturnToMenuException()


def returningToMenuNoMessage():
    raise ReturnToMenuException()


def invalidChoice(*args):
    printOutput("Choice was invalid")


def printListOfOptions(list_):
    for i in range(len(list_)):
        print(i, ":", list_[i])


# def getAnInputFromList(
#     list_, message: str
# ):  ## DO not use, this could open a window for induced stack overflowing
#     inp = askingInput(message)
#     if inp not in list_:
#         printOutput("Invalid input")
#         return getAnInputFromList(list_, message)


def clearScreenSafety():
    if not SCREEN_CLEAR_SAFETY:
        return
    _ = call("clear" if os.name == "posix" else "cls")
    printOutput("Screen cleared for safety purposes")


def clearScreenConvenience():
    if not SCREEN_CLEAR_CONVENIENCE:
        return
    _ = call("clear" if os.name == "posix" else "cls")
    printOutput("Screen cleared for convenience")


def checkIfFileExists(path, name, suffix):
    return os.path.isfile(r"{}\\{}.{}".format(path, name, suffix))


def getSeedFromUser():
    """Guaranteed to return a valid seed for random.seed()

    Returns:
        int: seed
    """
    seed = "a"
    while not is_valid_seed(seed):
        seed = askingInput("Introduce a positive integer as a seeds:")
        if not seed:
            returningToMenuNoMessage()
    seed = int(seed)
    if seed < 0:
        seed *= -1
    return seed


# In development


def runLeafMenu(object_for_call, menu: dict):
    try:
        for key in sorted(menu.keys()):
            printMenuOption(key, ":", menu[key][0])

        answer = input(askForMenuOption())
        menu.get(answer, [None, invalidChoice])[1](object_for_call)
    except ReturnToMenuException:
        print(ReturnToMenuException.message)
    except MenuExitException:
        clearScreenConvenience()
        exitMenu()


def runNodeMenu(object_for_call, menu: dict):
    while True:
        wrapperCall(object_for_call)
        try:
            for key in sorted(menu.keys()):
                printMenuOption(key, ":", menu[key][0])

            answer = input(askForMenuOption())
            next_menu = menu.get(answer, [None, None])[1](object_for_call)
        except ReturnToMenuException:
            print(ReturnToMenuException.message)
        except MenuExitException:
            clearScreenConvenience()
            exitMenu()


def runStandardMenu(object_for_call, menu: dict):
    try:
        for key in sorted(menu.keys()):
            printMenuOption(key, ":", menu[key][0])

        answer = input(askForMenuOption())
        menu.get(answer, [None, invalidChoice])[1](object_for_call)
    except ReturnToMenuException:
        print(ReturnToMenuException.message)
    except MenuExitException:
        clearScreenConvenience()
        exitMenu()

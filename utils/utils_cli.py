import os
from subprocess import call
from utils import utils.utils.is_valid_seed

SCREEN_CLEAR_CONVENIENCE = True
SCREEN_CLEAR_SAFETY = True


def askForMenuOption():
    return askingInput("Choose a menu option: ")


def printOutput(*args):
    print(">", args, end=".")


def askingInput(*args):
    return input(">>>", args, end=" ")


def printMenuOption(*args):
    print(">$ ", args)


class MenuExitException(Exception):
    def __init__(self, message=printOutput("Exiting menu...")):
        self.message = message
        super().__init__(self.message)


class ReturnToMenuException(Exception):
    def __init__(self, message=printOutput("Returning to menu...")):
        self.message = message
        super().__init__(self.message)


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
    for i in range (len(list_)):
        print(i,":", list_[i])


def getAnInputFromList(list_, message: str):  ##Use this
    inp = askingInput(message)
    if inp not in list_:
        printOutput("Invalid input")
        return getAnInputFromList(list_, message)


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
    while not utils.is_valid_seed(seed):
        seed = askingInput("Introduce a positive integer as a seeds:")
        if not seed:
            returningToMenuNoMessage()
    seed = int(seed)
    if seed < 0:
        seed *= -1
    return seed


def runStandardMenu(object_for_call, menu: dict):
    try:
        for key in sorted(menu.keys()):
            printMenuOption(key, ":", menu[key][0])

        answer = str(input(askForMenuOption()))
        menu.get(answer, [None, invalidChoice])[1](object_for_call)
    except ReturnToMenuException:
        print(ReturnToMenuException.message)
    except MenuExitException:
        clearScreenConvenience()
        exitMenu()

import os
from subprocess import call

SCREEN_CLEAR_CONVENIENCE = True
SCREEN_CLEAR_SAFETY = True


def askForMenuOption():
    return askingInput("Choose a menu option: ")


def printOutput(message: str):
    print(">" + message)


def askingInput(message: str):
    return input(">>>" + message + " ")


def printMenuOption(message: str):
    print(">$ " + message)


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


def returningToMenuMessage(specific_message: str):
    printOutput(specific_message)
    raise ReturnToMenuException()


def returningToMenuNoMessage():
    raise ReturnToMenuException()


def invalidChoice(*args):
    printOutput("Choice was invalid.")


def getAnInputFromList(list_, message: str):
    input = askingInput(message)
    if input not in list_:
        printOutput("Invalid input.")
        getAnInputFromList(list_, message)


def clearScreenSafety():
    if not SCREEN_CLEAR_SAFETY:
        return
    _ = call("clear" if os.name == "posix" else "cls")
    printOutput("Screen cleared for safety purposes.")


def clearScreenConvenience():
    if not SCREEN_CLEAR_CONVENIENCE:
        return
    _ = call("clear" if os.name == "posix" else "cls")
    printOutput("Screen cleared for convenience.")


def checkIfFileExists(path, name, suffix):
    return os.path.isfile(r"{}\\{}.{}".format(path, name, suffix))

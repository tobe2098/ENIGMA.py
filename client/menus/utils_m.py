import os
from subprocess import call

SCREEN_CLEAR_CONVENIENCE = True
SCREEN_CLEAR_SAFETY = True


def askForMenuOption():
    return askingInput("Choose a menu option: ")


def stringOutput(message: str):
    return ">" + message


def askingInput(message: str):
    return ">>>" + message


def menuOption(message: str):
    return ">$ " + message


class MenuExitException(Exception):
    def __init__(self, message=stringOutput("Exiting menu...")):
        self.message = message
        super().__init__(self.message)


class ReturnToMenuException(Exception):
    def __init__(self, message=stringOutput("Returning to menu...")):
        self.message = message
        super().__init__(self.message)


def exitMenu(*args):
    raise MenuExitException()


def returningToMenuMessage(specific_message: str):
    print(stringOutput(specific_message))
    raise ReturnToMenuException()


def returningToMenuNoMessage():
    raise ReturnToMenuException()


def invalidChoice(*args):
    print(stringOutput("Choice was invalid"))


def getAnInputFromList(list_, message: str):
    input = input(askingInput(message))
    if input not in list_:
        print(stringOutput("Invalid input."))
        getAnInputFromList(list_, message)


def clearScreenSafety():
    if not SCREEN_CLEAR_SAFETY:
        return
    _ = call("clear" if os.name == "posix" else "cls")
    print(stringOutput("Screen cleared for safety purposes."))


def clearScreenConvenience():
    if not SCREEN_CLEAR_CONVENIENCE:
        return
    _ = call("clear" if os.name == "posix" else "cls")
    print(stringOutput("Screen cleared for convenience."))

import os
from subprocess import call
from utils.utils import is_valid_seed
import traceback
from utils.types_utils_cli import wrapperCall

SCREEN_CLEAR_CONVENIENCE = True
SCREEN_CLEAR_SAFETY = True


def askForMenuOption():
    return askingInput("Choose a menu option: ")


def formatAsOutput(*args):
    args_list = list(args)

    args_list.insert(0, ">")
    args_list.append(".")
    updated_args = tuple(args_list)

    return updated_args


def formatAsWarning(*args):
    args_list = list(args)

    args_list.insert(0, "%.%Warning: ")
    updated_args = tuple(args_list)

    return updated_args


def formatAsError(*args):
    args_list = list(args)

    args_list.insert(0, "$ERROR$: ")
    updated_args = tuple(args_list)

    return updated_args


def printOutput(*args):
    print(formatAsOutput(args))


def printWarning(*args):
    print(formatAsWarning(args))


def printError(*args):
    print(formatAsError(args))


def askingInput(*args):
    prompt = ">>>"
    for arg in args:
        prompt += arg
    prompt += ": "
    return input(prompt)


def printMenuOption(*args):
    print(">$ ", args)


class MenuExitException(Exception):
    def __init__(self, message="Exiting menu..."):
        super().__init__(formatAsOutput(message))


class ReturnToMenuException(Exception):
    def __init__(self, message="Returning to menu..."):
        super().__init__(formatAsOutput(message))


class DevOpsException(ReturnToMenuException):
    def __init__(self, message):
        super().__init__(message)
        self.type_msg = formatAsOutput(
            "Development oversight. Something happened here:"
        )
        self.traceback = traceback.format_exc()

    def __str__(self):
        return f"{super().__str__()}\n{self.type_msg}\nTraceback:\n{self.traceback}"


class BadInputException(DevOpsException):
    def __init__(self, message):
        super().__init__(message)
        self.type_msg = formatAsOutput(
            "An incorrect input was received in the following core function:"
        )


def exitMenu(*args):
    raise MenuExitException()


def returningToMenu(*args):
    if args:
        print(args)
    # args_list = list(args)

    # # Get the first argument
    # if args_list and args_list[0] == "E":
    #     first_arg = args_list.pop(0)
    #     remaining_args = tuple(args_list)
    #     printError(remaining_args)
    # elif args_list:
    #     remaining_args = tuple(args_list)
    #     printOutput(args_list)
    raise ReturnToMenuException()


# def returningToMenu():
#     raise ReturnToMenuException()


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


def clearScreenSafetyCLI():
    if not SCREEN_CLEAR_SAFETY:
        return
    _ = call("clear" if os.name == "posix" else "cls")
    printOutput("Screen cleared for safety purposes")


def clearScreenConvenienceCli():
    if not SCREEN_CLEAR_CONVENIENCE:
        return
    _ = call("clear" if os.name == "posix" else "cls")
    printOutput("Screen cleared for convenience")


def checkIfFileExists(path, name, suffix):
    return os.path.isfile(r"{}\\{}.{}".format(path, name, suffix))


def checkInputValidity(_input, _type=str, _range=None):
    return isinstance(_input, _type) and (not _range or _input in _range)


def getSeedFromUser():
    """Guaranteed to return a valid seed for random.seed()

    Returns:
        int: seed
    """
    seed = "a"
    while not is_valid_seed(seed):
        seed = askingInput("Introduce a positive integer as a seeds:")
        if not seed:
            returningToMenu()
    seed = int(seed)
    if seed < 0:
        seed *= -1
    return seed


# In development


def runNodeMenu(object_for_call, menu: dict):
    while True:
        try:
            # Exit option check: ["0"]==exitMenu(), function should be universal? Or just try and get exception seems to work
            wrapperCall(object_for_call)
            for key in sorted(menu.keys()):
                printMenuOption(key, ":", menu[key][0])

            answer = input(askForMenuOption())
            result = menu.get(answer, (None, None))[1]
            if not result:
                invalidChoice()
            elif callable(result):
                result(object_for_call)
            else:  # Here we assume it is a dictionary
                runNodeMenu(object_for_call, result)
        except ReturnToMenuException:
            print(ReturnToMenuException)
        except MenuExitException:
            clearScreenConvenienceCli()
            exitMenu()


# def runLeafMenu(object_for_call, menu: dict):
#     while True:
#         try:
#             wrapperCall(object_for_call)
#             for key in sorted(menu.keys()):
#                 printMenuOption(key, ":", menu[key][0])

#             answer = input(askForMenuOption())
#             menu.get(answer, (None, invalidChoice))[1](object_for_call)
#         except ReturnToMenuException:
#             print(ReturnToMenuException)
#         except MenuExitException:
#             clearScreenConvenienceCLI()
#             exitMenu()


# Deprecated now
# def runStandardMenu(object_for_call, menu: dict):
#     try:
#         for key in sorted(menu.keys()):
#             printMenuOption(key, ":", menu[key][0])

#         answer = input(askForMenuOption())
#         menu.get(answer, [None, invalidChoice])[1](object_for_call)
#     except ReturnToMenuException:
#         print(ReturnToMenuException.message)
#     except MenuExitException:
#         clearScreenConvenienceCLI()
#         exitMenu()

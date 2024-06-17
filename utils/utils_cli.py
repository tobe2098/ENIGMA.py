import os
from subprocess import call

from utils.utils import is_valid_seed
from utils.types_utils_cli import wrapperCall
from exceptions import (
    BadInputExceptionCLI,
    MenuExitException,
    ReturnToMenuException,
)

SCREEN_CLEAR_CONVENIENCE = True
SCREEN_CLEAR_SAFETY = True


def askForMenuOption():
    return askingInput("Choose a menu option: ")


def formatAsOutput(args_tuple):
    args_list = list(args_tuple)
    args_list.insert(0, ">")
    args_list.append(".")
    prompt = ""
    for i in args_list:
        prompt += str(i)
    return prompt


def formatAsWarning(args_tuple):
    args_list = list(args_tuple)
    args_list.insert(0, "%.%Warning: ")
    prompt = ""
    for i in args_list:
        prompt += str(i)
    return prompt


def formatAsError(args_tuple):
    args_list = list(args_tuple)

    args_list.insert(0, "$ERROR$: ")
    prompt = ""
    for i in args_list:
        prompt += str(i)
    return prompt


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


def exitMenu(*args):
    raise MenuExitException()


def returningToMenu(*args, output_type="o"):
    if args:
        if output_type == "o":
            printOutput(args)
        elif output_type == "e":
            printError(args)
        elif output_type == "w":
            printWarning(args)
        else:
            raise BadInputExceptionCLI()
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


def checkInputValidity(_input: str, _type=str, _range=None):
    if _type == int:
        if _input.isnumeric() and (not _range or int(_input) in _range):
            return int(_input)
    elif _type == str:
        if isinstance(_input, str) and (not _range or _input in _range):
            return _input
    else:
        raise BadInputExceptionCLI()
    return None


def getSeedFromUser():
    """Guaranteed to return a valid seed for random.seed()

    Returns:
        int: seed
    """
    seed = "a"
    while not is_valid_seed(seed):
        seed = askingInput("Introduce a positive integer as a seed:")
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

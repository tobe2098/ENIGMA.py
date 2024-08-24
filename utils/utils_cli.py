import os
from subprocess import call
import string

from core.abstract import AbstractBaseClass

from ..utils.utils import is_valid_seed
from ..utils.types_utils_cli import wrapperCall
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
    REVIEW THE MENU EXIT PARADIGM
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


def checkIfFileExists(path, name=None, suffix=None):
    # return os.path.isfile(rf"{path}\\{name}.{suffix}")
    if name and suffix:
        return os.path.isfile(os.path.join(path, f"{name}.{suffix}"))
    else:
        return os.path.isfile(path)


def checkInputValidity(_input: str, _type=str, rangein=[]):
    if _type == int:
        if _input.isnumeric() and (
            (isinstance(rangein, list) and (not rangein or int(_input) in rangein))
            or (
                isinstance(rangein, tuple)
                and int(_input) < rangein[1]
                and int(_input) >= rangein[0]
            )
        ):
            return int(_input)
    elif _type == str:
        if isinstance(_input, str) and (not rangein or _input in rangein):
            return _input
    else:
        raise BadInputExceptionCLI()
    return None


def getSeedFromUser(ask="seed"):
    """Guaranteed to return a valid seed for random.seed()

    Returns:
        int: seed
    """
    seed = "a"
    while not is_valid_seed(seed):
        seed = askingInput(f"Introduce a positive integer as a {ask}:")
        if not seed:
            returningToMenu()
        elif seed.isnumeric():
            seed = int(seed)
    if seed < 0:
        seed *= -1
    return seed


# In development


def runNodeMenu(object_for_call: AbstractBaseClass, menu: dict):
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
                try:
                    runNodeMenu(object_for_call, result)
                except MenuExitException:
                    pass
        except ReturnToMenuException as e:
            print(e)
        except MenuExitException:
            clearScreenConvenienceCli()
            exitMenu()


def get_a_charlist_and_name_from_user():
    name = askingInput("Write a name for your character list")
    charlist = list(
        askingInput(
            "Write a string of characters to create your list (only unique characters will be considered)"
        ).strip(chars=string.whitespace)
    )
    unique_charlist = []
    for i in charlist:
        if i not in unique_charlist:
            unique_charlist.append(i)
    return charlist, name


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

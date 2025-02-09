import os
from subprocess import call
import string
import sys

from denigma.core.abstract import AbstractBaseClass

from .utils import is_valid_seed, Constants, get_charlist_json
from .exceptions import (
    BadInputExceptionCLI,
    MenuExitException,
    ReturnToMenuException,
)
from .formatting import printOutput, printError, printWarning, printMenuOption, printMenuStack,formatMenuReturn


menu_stack=[]

def askForMenuOption():
    ans=askingInput("Choose a menu option")
    if ans==Constants.menu_id_string:
        return None
    return ans


def askingInput(*args):
    prompt = "\n<¿?> "
    for arg in args:
        prompt += arg
    prompt += ": "
    ans=str(input(prompt))
    print("")
    return ans


def exitProgram():
    clearScreen()
    sys.exit(0)


# def returningToMenu():
#     raise ReturnToMenuException()


def invalidChoice(*args):
    printOutput("Choice was invalid")


def printListOfOptions(list_):
    for i in range(len(list_)):
        print("|"+str(i)+"|"+ ":"+ str(list_[i]))


# def getAnInputFromList(
#     list_, message: str
# ):  ## DO not use, this could open a window for induced stack overflowing
#     inp = askingInput(message)
#     if inp not in list_:
#         printOutput("Invalid input")
#         return getAnInputFromList(list_, message)


def _print_charlist_collection(dictionary=None):
    if not dictionary:
        dictionary = get_charlist_json()
    name_list = list(dictionary.keys())
    printListOfOptions(name_list)
    return name_list


def _get_a_charlist_from_storage():
    dictionary = get_charlist_json()
    name_list = _print_charlist_collection(dictionary=dictionary)
    name_index = askingInput("Input the index of the desired character list")
    # print(name_index)
    # print(name_list)
    if name_index=="":
        returningToMenu()
    name_index = checkInputValidity(name_index, int, (0, len(name_list)))
    while name_index==None:
        name_index = askingInput("Input a valid index")
        if name_index=="":
            returningToMenu()
        name_index = checkInputValidity(name_index, int, (0, len(name_list)))
    return dictionary[name_list[name_index]]


def exitMenu(*args):
    raise MenuExitException()


def returningToMenu(*args, output_type="o"):
    global menu_stack
    if args:
        message=""
        for i in args:
            message+=i
        if output_type == "o":
            printOutput(message)
        elif output_type == "e":
            printError(message)
        elif output_type == "w":
            printWarning(message)
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


def clearScreen():
    command = "clear" if os.name == "posix" else "cls"
    _ = call([command], shell=True)


def clearScreenSafetyCLI():
    if not Constants.SCREEN_CLEAR_SAFETY:
        return
    clearScreen()
    printOutput("Screen cleared for safety purposes")


def clearScreenConvenienceCli():
    if not Constants.SCREEN_CLEAR_CONVENIENCE:
        return
    clearScreen()
    printOutput("Screen cleared for convenience\n")


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
        seed = askingInput(f"Introduce a positive integer as a {ask}")
        if not seed:
            returningToMenu()
        elif seed.isnumeric():
            seed = int(seed)
    if seed < 0:
        seed *= -1
    return seed


# In development


def runNodeMenu(object_for_call: AbstractBaseClass, menu: dict):
    global menu_stack
    if menu[Constants.menu_obj_base_string]:
        menu_stack.append(menu[Constants.menu_id_string]+":"+object_for_call.get_name())
    else:
        menu_stack.append(menu[Constants.menu_id_string])
    while True:
        try:
            printMenuStack(menu_stack)
            # Exit option check: ["0"]==exitMenu(), function should be universal? Or just try and get exception seems to work
            # wrapperCall(object_for_call)
            for key in sorted([x for x in menu.keys() if x.isdigit()], key=int):
                printMenuOption(key, ":", menu[key][0])

            answer = askForMenuOption()
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
            print(e,formatMenuReturn(menu_stack[-1]))
        except MenuExitException:
            menu_stack.pop()
            clearScreenConvenienceCli()
            returningToMenu()


def runNodeMenuObjectless(menu: dict):
    global menu_stack
    menu_stack.append(menu[Constants.menu_id_string])
    while True:
        try:
            # Exit option check: ["0"]==exitMenu(), function should be universal? Or just try and get exception seems to work
            printMenuStack(menu_stack)
            for key in sorted([x for x in menu.keys() if x.isdigit()], key=int):
                if key==Constants.menu_id_string:
                    continue
                printMenuOption(key, ":", menu[key][0])

            answer = askForMenuOption()
            result = menu.get(answer, (None, None))[1]
            if not result:
                invalidChoice()
            elif callable(result):
                result()
            else:  # Here we assume it is a dictionary
                try:
                    runNodeMenuObjectless(result)
                except MenuExitException:
                    pass
        except ReturnToMenuException as e:
            print(e,formatMenuReturn(menu_stack[-1]),"\n")
        except MenuExitException:
            menu_stack.pop()
            clearScreenConvenienceCli()
            returningToMenu()


def get_a_charlist_and_name_from_user():
    name = askingInput("Write a name for your character list")
    charlist = list(
        askingInput(
            "Write a string of characters to create your list (only unique characters will be considered)"
        ).strip(string.whitespace)
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

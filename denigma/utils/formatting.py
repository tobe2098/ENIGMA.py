def formatAsOutput(args_tuple):
    prompt = "--> "
    for i in args_tuple:
        prompt += str(i)
    prompt+=".";
    return prompt


def formatAsWarning(args_tuple):
    prompt = "%.%Warning: "
    for i in args_tuple:
        prompt += str(i)
    return prompt


def formatAsError(args_tuple):
    prompt = "$>ERROR<$: "
    for i in args_tuple:
        prompt += str(i)
    return prompt


def formatAsMenuOption(args_tuple):
    args_list = list(args_tuple)
    args_list.insert(0, "|")
    args_list.insert(2, "|")
    # args_list.insert(3, " ")
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


def printMenuOption(*args):
    print(formatAsMenuOption(args))

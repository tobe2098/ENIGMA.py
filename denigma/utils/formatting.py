def formatAsOutput(args_tuple):
    prompt = "--> "
    for i in args_tuple:
        prompt += str(i)
    prompt+=".";
    return prompt

def formatAsListing(args_tuple):
    prompt = "--"+args_tuple[0]+"--\n"
    for i in range(1,len(args_tuple)):
        prompt += str(args_tuple[i])
    return prompt

def formatMenuStack(args_tuple):
    prompt = "./"
    for i in args_tuple[0]:
        prompt += str(i)
        prompt += "/"
    prompt+='\n'
    return prompt

def formatMenuReturn(args_tuple):
    # prompt=args_tuple[0]
    # prompt += "</"
    # prompt += args_tuple[-1]
    # prompt+='/>\n'
    return f"</{args_tuple}/>"


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

def printListing(*args):
    print(formatAsListing(args))

def printMenuStack(*args):
    print(formatMenuStack(args))

def printMenuReturn(*args):
    print(formatMenuReturn(args))


def printWarning(*args):
    print(formatAsWarning(args))


def printError(*args):
    print(formatAsError(args))


def printMenuOption(*args):
    print(formatAsMenuOption(args))

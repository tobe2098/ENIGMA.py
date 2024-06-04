from ..core import *

## Put here all imports
## This is mainly oriented to imports and that is it.
# import sys

# # from tkinter import Y
# import os

# path = os.path.dirname(os.path.dirname((__file__)))
# sys.path.append(path)
# from ENIGMA_py.ENIGMA import *

machine = Machine()
print(
    """>RECOMMENDATIONS FOR USE:
-No writing down the seed, no sending it over unsecured channels. Preferably agree on a modification of the seed-generated machine.
-Read README.md
-Always keep a security copy of the machine.
-Short messages are more secure. Changing the machine periodically, or its settings is recommended. Once you have an open comm channel that should not be a problem.
-Passing the pickled machine on a USB is possibly the safest way to do it.
-Save the module and the pickled objects in a separate folder if possible.
-Do NOT write repeated sequences of words or predictable things like calling by name, saying "Hi", or "Goodbye".
-Remember that using simple or small seeds is going to make your channel more easy to crack, as a simple programme iterating this code could do it.
-Read the rest of the python files! I wrote a ton of functions to alter and personalize your machine, as well as tools to make it harder to crack.
-As far as I am aware, unless you commit predictable mistakes, your channel should not be cracked in any realistic framework.
-Communicate safely!
"""
)
# IMPLEMENT A FULL MENU WITH OPTIONS TO TUNE AND DO A BUNCH OF STUFF
if input(">>>Do you want to use a saved machine?[y/n]").lower() == "y":
    machine = load_existing_machine()
else:
    machine.random_machine()
    new_name = input(
        ">>>Put a name to your new ENIGMA machine so it is easier to ID afterwards. \nDo NOT put a overly revealing name related to your communications"
    )
    machine.change_name(new_name)
    machine.save_machine()
    print("Delete the randomly generated pickle file, keep the named one for you")
    if (
        input(
            ">>>Do you want to do an adjustment on the randomly generated machine?[y/n]:"
        )
        == "y"
    ):
        machine.manual_complete_config()
machine.encrypt_decrypt()

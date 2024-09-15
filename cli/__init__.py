# from ..core import *
__version__ = "1.0.0"


machine = Machine()
print()
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

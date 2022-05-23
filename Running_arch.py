import sys
from tkinter import Y
sys.path.append('C:\\Users\\Darkest White\\Desktop\\PROJECTTT\\PROGRAMMATICS\\Git_repos')
from ENIGMA_py.ENIGMA import *
machine=ENIGMAmachine()
if input("Do you want to use a saved machine?[y/n]").lower()=="y":
    machine.load_machine()
else:
    machine.random_machine()
machine.encrypt_decrypt()
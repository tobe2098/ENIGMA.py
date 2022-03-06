# ENIGMA_py.py
Personal adaptation of the classic ENIGMA machine to a python environment, with random seed setups and setup storage.

## Stage:
Still in development

## Instructions for use:
-Obtain a brand new ENIGMA machine with just some simple lines! Ready for use in one go!
```python
from ENIGMA import *
machine=ENIGMAmachine()
machine.random_machine()
```
-The machine is automatically saved in a folder as a pickled object. The folder is located in the same folder as the file.py you used to create the machine.
-Look into the documentation for manual configuration of the machine, not a recommended feature for now (hard to communicate setup)
-Now you can start encrypting or decrypting your messages with:

-Load previously saved machine with the code:

-To get the same configuration as someone else, you can physically receive the pickled object and load it with:

-Or, you can receive the seed number, insert it into the machine and perform a random setup:

## Recommendations:
-For easy use and fun, randomly generated setups are the best. You can previously agree to a number or deliver it after generating it. Random generation of the seed is recommended, even if delivery can be tricky (always use secure channels ;)). If you agree to a number, remember, the bigger the better! It will be harder for someone using the same software to predict your seed number that way.
-If you are using random generation it is always recommended to do a minor adjustment in either rotors, board or reflector. Simple enough to be replicable but it will make it much much harder to decrypt your messages without indications.
-For airtight security, setup your ENIGMA machine manually and keep the machine saved. Communicating the setup to another party is considerably harder, but if done appropiately should be as secure as encryption is able to be.
-Use a fourth rotor always. Many more will be implemented in the future ;)

#### Disclaimer:
Not suitable for military or commercial purposes

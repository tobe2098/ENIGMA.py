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

## Recommendations:
-For easy use and fun, randomly generated setups are the best.
-For airtight security, setup your ENIGMA machine manually and keep the machine saved. Communicating the setup to another party is considerably harder, but if done appropiately should be as secure as encryption is able to be.
-Use a fourth rotor always. Many more will be implemented in the future ;)

#### Disclaimer:
Not suitable for military or commercial purposes

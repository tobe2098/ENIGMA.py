# For current version
- Last machine folder/name is set in yaml. If not there, the auto-encrypt does not work. 
- Folders with the pickled objects are in the module folder, fixed path. Allow the user to save a machine/component in current folder (export).
- Look how to make yaml accessible to the script: file in the module.
- Change constructors to not have child and parent classes. The machines can be constructed using the available strings, and more stored by the user. Done
- Pathing has to be standardized to os module Done
- Reference return for loading, creating different machines requires that runNode assigns the return from the function, at least in cli and machine menus. Review.
- Review the exitMenu functionality

## Testing
- TESTING: RESULT MUST ALWAYS HAVE CURRENT DISTANCE EQUAL TO ZERO

## Last tasks
- Unify the error messages in file IO
- Re-write README.md in core folder
- Need to take care of the imports
- Re-write README.md in outer folder


# Planned changes
## v1.1 (Internal and quality of life update)
- The creation of dictionaries should be part of the constructor (a function call, not the entire thing). That way the code only needs to care about the list of characters itself (where order would matter).
- Program should store and load the last used machine.
- export_an_existing_charlist or not

## v1.2 (Feature addition and safety update)
- MaxNoRotors can be changed in yaml config (with limits itself)
- Add configuration of bools for safety and clarity screen clearance, MAX NOTCHES (configuration.something?)
- Add waiting when clearing the screen
- Enigma message when deleting screen, countdown

## v2.0 (Great feature addition)
- I can add the posibility of customizing the character table. Because it is all dictionaries and relative positions in the rotors, it should not spell any trouble. Requires checks on loading that depend on the character lists, requires a new class of every object for Custom, or changing current paradigm so that the base class admits any character list. Make sure there is no arithmetic on the characters.
- Rotating reflectors with their own position too.
- Non-reciprocal plugboard and reflector: This is not novel, the construction also does not need an odd number of characters by making the entry and exit pins of the reflector not symmetric. Same thing should be possible for the plugboard, the thing would be that encryption-decryption would require a switch between the modes.
- Single theoretical encryption that is not reciprocal, needs no reflector. But reflector doubles encryption.

## v3.0
- Setup compression. This would only work with the pre-set classes, unless the user also stores the character list and inputs it, or the entire string is also part of the compressed setup. It would look like a string of characters, where sets of characters determine the configuration (excluding names? Yes).
- 255 chars and \0 is not encrypted, for byte encription. 
### Backspace encryption
Enigma encrypt using backspaces from 0 to 255 with one of the bytes to sign when the char is not possible. Or mark it in a different way (using the plaintext, we can skip that section while writing non-sense in that section, as it is not going to be used, it is just signalling to add a number of forward steps).

## v4.0
-GUI

# Possible changes
- Scripted creation of Wermacht rotors
- Introduce Type_sth class for string printing? Lowecase, uppercase, plural and singular. Maybe not necessary
- API INTERACTIONS WITH A CHATTING PROGRAM (CHOOSE, OR ALL). A WAY OF INPUTTING AND OUTPUTTING STRINGS OF TEXT FROM A PROGRAM AND SENDING THEM, WHILE ONLY DISPLAYING THE TRANSLATED MESSAGE (WHICH HAS TO BE STORED LOCALLY). THE INIT OF SUCH A COMMS SYSTEM IS COMPLICATED. TO DO SO, THERE IS PROBABLY A NEED TO FIND A SAFE WAY TO SEND CONFIGS (double key does not work, at least in non-dash)
- Put better character prints so that it looks more aesthetic
- Put print("\a") somewhere? Does not work
- Hyper-safe settings. Bigger rotors, more rotors, possibility of rotor bypassing through 'void' character.
- Enigma encrypt using backspaces from 0 to 255 with one of the bytes to sign when the char is not possible. Or mark it in a different way (using the plaintext, we can skip that section while writing non-sense in that section, as it is not going to be used, it is just signalling to add a number of forward steps).

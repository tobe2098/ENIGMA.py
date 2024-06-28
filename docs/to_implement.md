# Planned changes
## v1.1 (Internal and quality of life update)
- The creation of dictionaries should be part of the constructor (a function call, not the entire thing). That way the code only needs to care about the list of characters itself (where order would matter).
- Program should store and load the last used machine.

## v1.2 (Feature addition and safety update)
- Add configuration of bools for safety and clarity screen clearance, MAX NOTCHES (configuration.something?)
- Add waiting when clearing the screen
- Enigma message when deleting screen, countdown

## v2.0 (Great feature addition)
- I can add the posibility of customizing the character table. Because it is all dictionaries and relative positions in the rotors, it should not spell any trouble. Requires checks on loading that depend on the character lists, requires a new class of every object for Custom, or changing current paradigm so that the base class admits any character list. Make sure there is no arithmetic on the characters.
-Rotating reflectors with their own position too.
## v3.0
- Setup compression. This would only work with the pre-set classes, unless the user also stores the character list and inputs it, or the entire string is also part of the compressed setup. It would look like a string of characters, where sets of characters determine the configuration (excluding names? Yes).

## v4.0
-GUI

# Possible changes
- Scripted creation of Wermacht rotors
- Introduce Type_sth class for string printing? Lowecase, uppercase, plural and singular. Maybe not necessary
- API INTERACTIONS WITH A CHATTING PROGRAM (CHOOSE, OR ALL). A WAY OF INPUTTING AND OUTPUTTING STRINGS OF TEXT FROM A PROGRAM AND SENDING THEM, WHILE ONLY DISPLAYING THE TRANSLATED MESSAGE (WHICH HAS TO BE STORED LOCALLY). THE INIT OF SUCH A COMMS SYSTEM IS COMPLICATED. TO DO SO, THERE IS PROBABLY A NEED TO FIND A SAFE WAY TO SEND CONFIGS (double key does not work, at least in non-dash)
- Put better character prints so that it looks more aesthetic
- Put print("\a") somewhere? Does not work
- Hyper-safe settings. Bigger rotors, more rotors, possibility of rotor bypassing through 'void' character.


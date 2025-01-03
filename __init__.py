# Tasks
# Exit from every menu option (universal)
# Review that all menus are ste according to utils_cli.py standards
# rotors_m
# Reflectors_m
# Machine_m
# Plugboards_m
# Review that all functions use standardized I/O from utils_cli.py and other utils
# rotors_m
# Reflectors_m
# Machine_m
# Plugboards_m
# Start main menu and encryption (on the go [this is interactive and I do not know how to do it]and text)
# Finish __init__.pys and CLI.py. Look on how to organize the library for both cli and GUI calls
## For current version v1.0
## IMPORTANT TO SET TIMEOUTS IN ALL FILE I/O
## ADD MAx DEPTH for recursive calls
# Move constants somewhere that is not utils? If I can make them static somehow (or constants.py file)
# Do type checking before encryption## REMEMBER TO DO THE DASH NOT DASH CHECKS!!!!
# Machine has to store initial state before starting to encrypt/decrypt
# Put exceptions for every core function that manipulates the objects. ARGUMENT CHECKING SHOULD BE A SINGLE FUNCTION INSIDE THE CORE
# In case pickling does not work: "a" is for appending, "w" for writing, "b" for binary
# Develop unit tests
# with open('mypickle.pickle', 'wb') as f:
#    pickle.dump(some_obj, f)
# Editing pre-existing rotors and reflectors has to be outside the machine menu
# Valid input checking in reflectors, machines and rotors
# Dictionary of dictionaries for menu calls summarized functions
# Write down how the script is supposed to run with CLI options.
# Make a check to avoid any menus that do not have an exit option.
# Write a white paper on the encryption novelty (?)
## Here we have the menuing functions outside the machine menus
# Docs

## Add option to translate entire files (skipping non-standard characters) (txt)
# Code the other encryption method, using character for character (no backspace<=26) and bitwise too.

##FLOW: in all inits, there should be the code related to loading default/saved setups/preferences
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


# Creating a Python library involves organizing your code into a package or module that can be easily distributed and used by others. Here's a step-by-step guide to creating a Python library:

# ### 1. Structure your code:

# - **Choose a Structure:** Organize your code into a directory structure. For a simple library, this might include a main package directory and subdirectories for different modules or functionalities.

# - **Write your Code:** Create Python files (.py) containing the functions, classes, or other code you want to include in your library.

# ### 2. Create a setup.py file:

# The `setup.py` file is used to describe your library to the Python packaging tools and to specify how your package should be installed. Here's an example of a simple `setup.py` file:

# ```python
# from setuptools import setup, find_packages

# setup(
#     name='your_library_name',
#     version='0.1',
#     packages=find_packages(),
#     description='Your library description',
#     author='Your Name',
#     author_email='your@email.com',
#     url='https://github.com/your_username/your_library_repo',
#     classifiers=[
#         'Programming Language :: Python :: 3',
#         # Add other classifiers as needed
#     ],
# )
# ```

# ### 3. Add documentation:

# - **README:** Write a README file explaining what your library does, how to install it, and provide examples of usage.

# - **Docstrings:** Include docstrings in your code to describe functions, classes, and modules. This documentation can be extracted using tools like Sphinx.

# ### 4. Testing:

# - **Write Tests:** Create test files to ensure that your library functions as expected. Use a testing framework like `unittest` or `pytest`.

# ### 5. Publish your library:

# - **Package:** Create a distribution package of your library. Run the following command in the directory containing `setup.py`:

#   ```bash
#   python setup.py sdist bdist_wheel
#   ```

# - **Upload:** Upload your package to the Python Package Index (PyPI) or a private repository. You can use `twine` to upload to PyPI:

#   ```bash
#   pip install twine
#   twine upload dist/*
#   ```

# ### 6. Installation:

# - **Install:** Users can install your library using `pip`:

#   ```bash
#   pip install your_library_name
#   ```

# ### Additional Tips:

# - **Version Control:** Use version control (e.g., Git) to manage your code and host it on platforms like GitHub.

# - **Licensing:** Choose an appropriate license for your library to define how others can use and contribute to it.

# - **Documentation:** Maintain good documentation to help users understand and utilize your library effectively.

# By following these steps, you can create a Python library that can be easily installed, used, and shared by others.

__all__ = ["core", "utils"]
# from ..core import *
__version__ = "1.0.0"
from utils.utils import (
    get_charlist_json,
    get_config_json,
    save_charlist_json,
    save_config_json,
)

## Put here all imports
## This is mainly oriented to imports and that is it.
# import sys

# # from tkinter import Y
# import os

# path = os.path.dirname(os.path.dirname((__file__)))
# sys.path.append(path)
# from ENIGMA_py.ENIGMA import *

## Set-up functions (only if running as a script!), not necessary
save_charlist_json(dictionary=get_charlist_json())
save_config_json(dictionary=get_config_json())

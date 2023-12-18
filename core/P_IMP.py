from ENIGMA_py.ROTOR import ROTOR
from ENIGMA_py.REFLECTOR import REFLECTOR
import pickle
import random
#Look into installation of the module
def create_real_rotor(rotor_name):
    #Scripted creation of Wermacht rotors
    if rotor_name=="I":
        rotor=ROTOR
        return rotor
def import_rotor(filename): 
    # Import all available rotors into a list? Or just return a rotor from the saved ones?
    filehandler = open(filename, 'r') 
    object = pickle.load(filehandler)
def seed_list_show():
    pass #.txt with a list of seeds and attached non-related names?
def import_rotor_list(self): FOR ROTOR PREVIEW
    return #list_of_rotors
    #Not finished, for ENIGMA_py.pyç
def encrypt_decrypt_txt_file(self, filepath):
    pass #Basically loop every character and if .upper() is between 65 and 65+25, decrypt, otherwise input the same character (like spaces)

ON API INTERACTIONS WITH A CHATTING PROGRAM (CHOOSE). A WAY OF INPUTTING AND OUTPUTTING STRINGS OF TEXT FROM A PROGRAM AND SENDING THEM, 
WHILE ONLY DISPLAYING THE TRANSLATED MESSAGE (WHICH HAS TO BE STORED LOCALLY). THE INIT OF SUCH A COMMS SYSTEM IS COMPLICATED. 
TO DO SO, THERE IS PROBABLY A NEED TO FIND A SAFE WAY TO SEND CONFIGS (double key does not work)
#Put better character prints so that it looks more aesthetic
#Put print("\a") somewhere? Does not work
#In case pickling does not work: "a" is for appending, "w" for writing, "b" for binary
# with open('mypickle.pickle', 'wb') as f:
#    pickle.dump(some_obj, f)
#ord(" ")=32
#randomE is not implemented yet

###
#Include numbers: before incrypt you add 65 to the number, after you subsgtract, and you treat corresponding caracter as the number, transofrming all the time
#Problems?

################################## IMPORTANT POSSIBILITY IS TO MAKE THE REFLECTOR HAVE TWO LETTERS (OR ONE, SEE BELOW) THAT CONNECT TO THEMSELVES TO ALLOW FOR 
A SELF-LETTER ENCRYPTION, BYPASSING ENIGMA'S FIRST FLAW.' ALTERNATIVELY, YOU CAN ADD A SINGLE LETTER 'VOID' THAT BYPASSES THAT ROTOR OR REFLECTOR, 
HAVING THE SAME EFFECT WITHOUT BREAKING THE MACHINE. THIS LAST OPTION DOES NOT WORK IN ELECTROMECHANICAL VERSION UNLESS EVERY ELECTRODE HAS TWO PATHWAYS, ONE FW ONE BW.

# #### Implement a random distribution with min 3 and max 100 for rotors.
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
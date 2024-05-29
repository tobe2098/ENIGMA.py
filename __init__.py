import core
import cli
import gui

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

## Add option to translate entire files (skipping non-standard characters) (txt)
# Think about how to store functions

##FLOW: in all inits, there should be the code related to loading default/saved setups/preferences


# This should be in main.py
if __name__ == "__main__":
    # This should be in main.py
    import sys
    import argparse

# def main():
#     parser = argparse.ArgumentParser(description="My Library CLI")

#     # Add command-line arguments
#     parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose mode")
#     parser.add_argument('name', type=str, help="Name to greet")

#     args = parser.parse_args()

#     if args.verbose:
#         print(f"Verbose mode enabled. Greeting {args.name}.")

#     print(f"Hello, {args.name}!")

# if __name__ == "__main__":
#     main()

# From here we should go to either the CLI or the GUI.


def save_n_random_rotors(n, seed):
    for i in range(0, n):
        rotor = rotors.Rotor()
        rotor._random_setup(seed + i)
    return ">Done"


def tune_existing_rotor():
    rotor = rotors.Rotor()
    rotor.import_rotor()
    rotor.configure()
    rotor.export_rotor()
    return ">Rotor was edited and saved"
    # Extract args
    # Run client or gui


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

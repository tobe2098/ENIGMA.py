from utils.utils import Constants

__all__ = ["core", "cli", "gui"]
# from ..core import *

"""Denigma - A message and file encryption tool"""

import cli.cli
import core
import cli.functions

# Import your existing functions
from .functions.cli_f import encrypt_message
from .functions.machines_f import encrypt_file

__version__ = Constants.VERSION

__all__ = ["encrypt_message", "encrypt_file", "cli_main"]
## Set-up functions (only if running as a script!), not necessary

from denigma.utils.utils import Constants

__all__ = ["core", "cli", "gui"]
# from ..core import *

"""Denigma - A message and file encryption tool"""

# import denigma.cli.cli
import denigma.core
import denigma.cli.functions

__version__ = Constants.VERSION

__all__ = ["encrypt_message", "encrypt_file", "cli_main"]
## Set-up functions (only if running as a script!), not necessary

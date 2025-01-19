"""Start the CLI for denigma."""

from .menus.cli_m import _outer_cli_menu
from utils.utils_cli import runNodeMenuObjectless


def start_cl_interface():
    runNodeMenuObjectless(_outer_cli_menu)

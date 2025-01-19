"""Start the CLI for denigma."""

from .menus.cli_m import _outer_cli_menu
from utils.utils_cli import runNodeMenuObjectless
from utils.utils import (
    get_charlist_json,
    get_config_json,
    save_charlist_json,
    save_config_json,
)


def start_cl_interface():
    save_charlist_json(dictionary=get_charlist_json())
    save_config_json(dictionary=get_config_json())

    try:
        runNodeMenuObjectless(_outer_cli_menu)
    except Exception as e:
        print(e)

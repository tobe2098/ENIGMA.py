from copy import deepcopy
from denigma.utils.utils import Constants
import string
from denigma.utils.exceptions import raiseBadInputException

class AbstractBaseClass:
    def __init__(self, charlist: list = [],name="name") -> None:
        self._charlist = deepcopy(charlist)
        self._name=name

    def get_charlist(self) -> list:
        return self._charlist
    def get_name(self)->str:
        return self._name
    def _is_name_valid(self, name):
        return (
        name != "name" and name != "" and all(c in Constants.FILESAFE_CHARS for c in name)
    )
    
    def _change_name(self, new_name):
        """_summary_

        Args:
            new_name (_type_): _description_

        Raises:
            Exception: _description_
        """

        new_name = new_name.strip(string.whitespace)
        if not self._is_name_valid(new_name):
            raiseBadInputException()
        self._name = new_name
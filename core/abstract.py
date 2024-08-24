from copy import deepcopy


class AbstractBaseClass:
    def __init__(self, charlist=[]) -> None:
        self._charlist = deepcopy(charlist)

    def _get_charlist(self):
        return self._charlist

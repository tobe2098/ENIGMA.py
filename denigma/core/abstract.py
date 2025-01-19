from copy import deepcopy


class AbstractBaseClass:
    def __init__(self, charlist: list = []) -> None:
        self._charlist = deepcopy(charlist)

    def get_charlist(self) -> list:
        return self._charlist

from ...core import plugboards





def main_plugboard_menu(plugboard_ref:plugboards.PlugBoard):
    menu = {"1":("Sum",func1),
        "2":("Quit",func2)
       }
for key in sorted(menu.keys()):
     print "$$ "+key+":" + menu[key][0]

ans = raw_input("Make A Choice")
menu.get(ans,[None,invalid])[1]()


def show_board_config():
    pass


def edit_board_config():
    pass



    def manual_board_setup(self):
        # Configuration of the cable board
        # PENDING: Make it stop after 26 letters have been assigned
        if len(self._board_dict) > 0:
            print("Current board setup is:", simplify_board_dict(self.board_dict))
            accbool = input("Input N if you do NOT want to change the board setup:")
            if accbool == "N":
                return
        seen_letters = []
        board_dict = dict(zip(self._characters_in_use, self._characters_in_use))
        all_letters = copy.copy(self._characters_in_use)
        while True:
            print("If you want to stop configurating the board, press Enter")
            configpair = input("Enter pair of letters for board configuration:").upper()
            if configpair.isalpha() or not configpair:
                pass
            else:
                print("Error: Input 2 letters please")
                continue
            configpair = list(configpair)
            if (
                len(list(set(all_letters) - set(seen_letters))) == 0
                or len(configpair) == 0
            ):
                break
            if len(configpair) != 2:
                print("Error: Input 2 letters please")
                continue
            if any(map(lambda v: v in configpair, seen_letters)):
                print("Already plugged")
                continue
            else:
                seen_letters.append(configpair[0])
                seen_letters.append(configpair[1])
                board_dict[configpair[0]] = configpair[1]
                board_dict[configpair[1]] = configpair[0]
            print("Current config:\n", simplify_board_dict(board_dict))
            print(
                "Not connected letters:\n", list(set(all_letters) - set(seen_letters))
            )
        self._board_dict = board_dict
        self._update_dicts()
        print("Finished")

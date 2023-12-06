
    def configure(self):
        # Configuration of the cable reflector
        # PENDING: Make it stop after 26 letters have been assigned
        if self.reflector_dict:
            print(">Current reflector setup is:")
            print(">Connections:\n", simplify_board_dict(self.reflector_dict))
            print(">Name:", self.name)
            accbool = input(
                ">>>Input N if you do NOT want to change the reflector setup:"
            )
            if accbool == "N":
                return
        if self.name == "name":
            print(">Changing the name is necessary for exporting it")
        new_name = input(">>>Input new name for the reflector (Press Enter to skip):")
        if new_name:
            self.change_name(new_name)
        seen_letters = []
        reflector_dict = {letter: letter for letter in self.characters_in_use}
        all_letters = self.characters_in_use
        while True:
            if len(list(set(all_letters) - set(seen_letters))) == 0:
                break
            print(">If you want to stop configurating the reflector, press Enter")
            configpair = input(
                ">>>Enter pair of letters for reflector configuration:"
            ).upper()
            if configpair and not configpair.isalpha():
                print(">Error: Input 2 letters please")
                continue
            configpair = [i for i in configpair]
            if len(configpair) == 2:
                pass
            elif len(configpair) == 0:
                break
            else:
                print(">Error: Input 2 letters please")
                continue
            if any(map(lambda v: v in configpair, seen_letters)):
                print(">One of the letters was already plugged")
                continue
            else:
                seen_letters.append(configpair[0])
                seen_letters.append(configpair[1])
                reflector_dict[configpair[0]] = configpair[1]
                reflector_dict[configpair[1]] = configpair[0]
            print(">Current config:\n", simplify_board_dict(reflector_dict))
            remaining_letters = list(set(all_letters) - set(seen_letters))
            print(">Not connected letters:\n", remaining_letters)
        if len(remaining_letters) == 1:
            reflector_dict[remaining_letters[0]] = remaining_letters[0]
        self.show_config()
        self.reflector_dict = copy.copy(reflector_dict)
        self._update_dicts()
        self.export_reflector()
        print(">Finished")

def save_n_random_reflectors(n, seed):
    # Create and save into pickle objects 20 randomly generated rotors. Use seed to generate new seed, or simply add numbers
    for i in range(0, n):
        reflector = Reflector()
        reflector.random_setup(seed + i)
    return ">Done"


def tune_existing_reflector():
    reflector = Reflector()
    reflector.import_reflector()
    reflector.configure()
    reflector.export_reflector()
    return ">Reflector was edited and saved"
    # Conda activation: conda info --envs, conda activate {}

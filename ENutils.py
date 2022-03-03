import pandas as pd
import random
from ROTOR import ROTOR
from REFLECTOR import REFLECTOR
def split_into_list(string):
    return [character for character in string]
def gen_rnd_26list(seed=None): #Deprecated, random.sample(range(1,27), n) does exactly the same
    if not seed:
        print("Problem in gen_rnd_26list()'s call")
    random.seed(seed) 
    poplist=[i+1 for i in range (26)]
    endlist=[]
    for i in range(len(poplist)):
        rm=random.randint(1, len(poplist))
        endlist.append(poplist.pop(rm-1))
    return endlist
def simplify_board_config(board_dict):
    seen_pairs=[]
    pairs=[]
    all_letters=split_into_list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    for letter_a, letter_b in board_dict.items():
        if letter_a in seen_pairs or letter_b in seen_pairs:
            continue
        elif letter_b==letter_a:
            continue
        else:
            pass
        pairs.append([letter_a, letter_b])
        seen_pairs.append(letter_a)
        seen_pairs.append(letter_b)
    unpaired=list(set(all_letters)-set(seen_pairs))
    board_config_simpl=pd.DataFrame(pairs, columns=["Letter A", "Letter B"])
    board_config_simpl["Unpaired"]=unpaired
    return board_config_simpl
def transform_single_dict(dictio):
    #Code of this function replaces the original functions in ROTOR.py, if there are errors check them here
    if 1 in dictio.values(): 
        new_values=[chr(i+64) for i in dictio.values()]
        new_keys=[chr(i+64) for i in dictio.keys()]
        convdict=dict(zip(new_keys, new_values))
        return convdict
    elif "A" in dictio.values():
        new_values=[ord(i)-64 for i in dictio.values()]
        new_keys=[ord(i)-64 for i in dictio.keys()]
        convdict=dict(zip(new_keys, new_values))
        return convdict
def save_n_random_rotors(n, seed):
    for i in range(0,n):
        rotor=ROTOR()
        rotor.random_rotor_setup(seed+i)
    return "Done"
def save_n_random_reflectors(n, seed):
    #Create and save into pickle objects 20 randomly generated rotors. Use seed to generate new seed, or simply add numbers
    for i in range(0,n):
        rotor=REFLECTOR()
        rotor.random_reflector_setup(seed+i)
    return "Done"
    ##Conda activation: conda info --envs, conda activate {}
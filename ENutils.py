import pandas as pd
import random
def split_into_list(string):
    return [character for character in string]
def gen_rnd_26list(seed=None):
    if not seed:
        print("Problem in gen_rnd_26list()'s call")
    random.seed(seed) 
    poplist=[i+1 for i in range (26)]
    endlist=[]
    for i in range(len(poplist)):
        rm=random.randint(1, len(poplist))
        endlist.append(poplist.pop(rm-1))
    return endlist
def pull_n_rnd_numbers(n, maxrange):
    numberlist=list(range(1,maxrange))
    
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
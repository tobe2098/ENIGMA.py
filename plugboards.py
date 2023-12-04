import copy
import random
from .utils import CHARACTERS, CHARACTERS_dash, transform_single_dict, transform_single_dict_dash, simplify_board_dict


class PlugBoard():
  def __init__(self) -> None:
    self._characters_in_use=copy.copy(CHARACTERS)
    self._board_dict=dict()
    self._board_num_dict=dict()

  def _update_dicts(self, letter_to_num=True):
      if letter_to_num:
          self._board_num_dict = transform_single_dict(
              self._board_dict)
      else:
          self._board_dict = transform_single_dict(
              self._board_num_dict)
          
  def show_config(self):
     print(simplify_board_dict(self.board_dict))

  def randomize_board_dict(self, seed):
    random.seed(seed)
    #Now set the connections
    ### !!! Make sure board is composed of pairs and is symmetrical!!! It is not as of now.
    num_list=list(range(0,len(self._characters_in_use)))
    random.shuffle(num_list)
    cable_num=random.randint(0,int(len(self._characters_in_use)/2))
    while cable_num>0 and len(num_list)>1:
        letterA=num_list.pop()
        letterB=num_list.pop()
        self._board_num_dict[letterA]=letterB
        self._board_num_dict[letterB]=letterA

    self._update_dicts(False)
    #Show final configuration
    #print(">>>Board config:\n", simplify_board_dict(self.board_dict))
    return ">>>Board setup is generated"
  

  def manual_board_dict(self):
      #Configuration of the cable board
      #PENDING: Make it stop after 26 letters have been assigned
      if len(self._board_dict)>0:
          print("Current board setup is:", simplify_board_dict(self.board_dict))
          accbool=input("Input N if you do NOT want to change the board setup:")
          if accbool=="N":
              return
      seen_letters=[]
      board_dict=dict(zip(self._characters_in_use, self._characters_in_use))
      all_letters=copy.copy(self._characters_in_use)
      while True:
          print("If you want to stop configurating the board, press Enter")
          configpair=input("Enter pair of letters for board configuration:").upper()
          if configpair.isalpha() or not configpair:
              pass
          else:
              print("Error: Input 2 letters please")
              continue
          configpair=list(configpair)
          if len(list(set(all_letters)-set(seen_letters)))==0:
              break
          if len(configpair)==2:
              pass
          elif len(configpair)==0:
              break
          else:
              print("Error: Input 2 letters please")
              continue
          if any(map(lambda v: v in configpair, seen_letters)):
              print("Already plugged")
              continue
          else:
              seen_letters.append(configpair[0])
              seen_letters.append(configpair[1])
              board_dict[configpair[0]]=configpair[1]
              board_dict[configpair[1]]=configpair[0]
          print("Current config:\n", simplify_board_dict(board_dict))
          print("Not connected letters:\n", list(set(all_letters)-set(seen_letters)))
      self._board_dict=board_dict
      self._update_dicts()
      print("Finished")


class PlugBoardDash(PlugBoard):
  def __init__(self) -> None:
     super().__init__()
     self._characters_in_use=copy.copy(CHARACTERS_dash)

  def _update_dicts(self, letter_to_num=True):
      if letter_to_num:
          self._board_num_dict = transform_single_dict_dash(
              self._board_dict)
      else:
          self._board_dict = transform_single_dict_dash(
              self._board_num_dict)
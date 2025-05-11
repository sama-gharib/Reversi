from model.move import Move
from model.player import Player

from random import choice

class Stupidity (Player):

    def _think(self, board) -> Move:

        c = choice(board.get_valid_moves())
        
        return Move(c[1], c[0]) 

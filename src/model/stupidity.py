from model.move import Move
from model.player import Player

from random import choice, uniform

from time import sleep

class Stupidity (Player):

    def _think(self, board) -> Move:
        sleep(uniform(0.5, 1)) # Simulate thinking time
        c = choice(board.get_valid_moves())
        return Move(c[1], c[0]) 
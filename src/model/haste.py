from model.move import Move
from model.player import Player

from random import uniform

from time import sleep

class Haste (Player):

    def _think(self, board) -> Move:
        sleep(uniform(0.5, 1)) # Simulate thinking time

        nb_flips = []
        for v_move in board.get_valid_moves():
            nb_flips.append(board.flipped_pieces(v_move[0], v_move[1]))
        
        c = board.get_valid_moves()[nb_flips.index(max(nb_flips))]
        return Move(c[1], c[0]) 
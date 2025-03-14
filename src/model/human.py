from model.move import Move
from model.player import Player

from time import sleep

class Human (Player):

    def __init__(self):
        super().__init__()
        self._result = None

    def should_play(self, column, line):
        if not self._done:
            self._result = Move(line, column)
        else:
            print('[DEBUG] A player tried to play but it wasn\'t his turn')

    def _think(self, board) -> Move:
        while self._result == None:
            sleep(0.01)
        r = self._result
        self._result = None
        return r
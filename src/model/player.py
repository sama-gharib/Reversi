from model.move import Move
from model.board import Board
from threading import Thread

class Player:

    def __init__(self):
        self._done = True

    def is_done(self):
        return self._done

    def play_on(self, board):
        if self._done:
            self._thread = Thread(target = self._work, args = [board], daemon=True)
            self._thread.start()
        else:
            raise ValueError('`Player` is not done yet.')

    def _work(self, board):
        self._done = False
        while True: # While move is not valid
            result = self._think(board)
            try:
                board.make_move(result.column, result.line)
                break
            except:
                print("[DEBUG] `Player` tried to play an invalid move.")

        self._done = True

    def _think(self, board) -> Move:
        raise NotImplementedError('Please override the `think` methode on every `Player` subclass.')
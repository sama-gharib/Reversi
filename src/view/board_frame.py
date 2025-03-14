import pygame as pg

from view.frame import Frame
from view.slot_button import SlotButton

class BoardFrame (Frame):
    '''
        This widget makes displaying a board easy !
    '''

    def __init__(self, board, humans = [], fill = "dark grey", position = pg.Vector2(0, 0), size = pg.Vector2(1, 1), children = []):
        super().__init__(True, fill, position, size, children)
        self._board = board
        self._humans = humans

        for line in range(self._board.board_size):
            for column in range(self._board.board_size):
                # SlotButton position is expected to be in board
                # position, so this works :
                self._children.append(SlotButton(board, humans, pg.Vector2(column, line)))

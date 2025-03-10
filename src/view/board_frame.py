import pygame as pg

from view.frame import Frame
from view.slot_button import SlotButton

class BoardFrame (Frame):
    def __init__(self, board, fill = "dark grey", position = pg.Vector2(0, 0), size = pg.Vector2(1, 1), children = []):
        super().__init__(True, fill, position, size, children)
        self._board = board
        
        slot_size = 1/self._board.board_size
        for line in range(self._board.board_size):
            for column in range(self._board.board_size):
                self._children.append(
                    SlotButton(
                        (pg.Vector2(column, line) +  pg.Vector2(0.05, 0.05)) * slot_size,
                        slot_size * 0.9
                    )
                )

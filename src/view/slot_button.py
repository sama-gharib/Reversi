import pygame as pg

from view.button import Button
from model.board import Board

class SlotButton (Button):
    '''
        This widget holds a reference to a board in order
        to auto update when player puts a new token.
    '''

    def __init__(self, board, position = pg.Vector2(0, 0), children = []):
        '''
            Warning ! Here, position is expected to be in board
            coordinates format, not in proportion as expected
            usually with widgets !!
            I.e : For an 8 slots wide board, position is expected
            to be between (0, 0) and (7, 7)
        '''

        slot_size = 1/board.board_size # In proportion

        super().__init__(
            lambda: print("TODO!!"),
            (200, 200, 200),
            (position +  pg.Vector2(0.05, 0.05)) * slot_size,
            slot_size * 0.9,
            children
        )
        self._board = board
        self._slot = position # (column, line)

    # Overrides

    def draw(self, surface):
        super().draw(surface)
        
        # Available since Python 3.10
        match self._board.get_at(int(self._slot.y), int(self._slot.x)):
            case Board.WHITE:
                pg.draw.ellipse(surface, 'white', self._absolute.as_rect())
            case Board.BLACK:
                pg.draw.ellipse(surface, 'black', self._absolute.as_rect())
            case Board.EMPTY:
                pass

        # Draw little cursor on hover
        if self._state == "hover":
            col = [i * 0.9 for i in self.get_true_color()]
            rec = self._absolute.as_rect()
            rec.left += 10
            rec.top += 10
            rec.width -= 20
            rec.height -= 20

            pg.draw.rect(surface, col, rec, border_radius = 10)

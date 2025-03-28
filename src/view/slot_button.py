import pygame as pg

from view.button import Button
from model.board import Board
from model.human import Human

class SlotButton (Button):
    '''
        This widget holds a reference to a board in order
        to auto update when player puts a new token.
    '''

    TOKEN_SPRITESHEET = None
    IMAGE_SCALE = 0.8
    MAX_FLIP_DELAY = 4

    def __init__(self, board, humans = [], position = pg.Vector2(0, 0), children = []):
        '''
            Warning ! Here, position is expected to be in board
            coordinates format, not in proportion as expected
            usually with widgets !!
            I.e : For an 8 slots wide board, position is expected
            to be between (0, 0) and (7, 7)
        '''
        slot_size = 1/board.board_size # In proportion

        super().__init__(
            lambda: self._on_click(),
            (200, 200, 200),
            (position +  pg.Vector2(0.05, 0.05)) * slot_size,
            slot_size * 0.9,
            children
        )
        self._board = board
        self._humans = humans
        self._slot = position # (column, line)
        self._image_rect = [0, 0, 64 * self.IMAGE_SCALE, 64 * self.IMAGE_SCALE]
        self._flip_delay = self.MAX_FLIP_DELAY

        # Load the spritesheet only if this
        # is the first SlotButton created
        if self.TOKEN_SPRITESHEET == None:
            self.TOKEN_SPRITESHEET = pg.image.load('res/token.png')
            target_size = self._absolute.as_rect()

            self.TOKEN_SPRITESHEET= pg.transform.scale(
                self.TOKEN_SPRITESHEET,
                #(target_size.width * 5, target_size.height)
                (320 * self.IMAGE_SCALE, 64 * self.IMAGE_SCALE)
            )

    def _on_click(self):
        for h in self._humans:
            if isinstance(h, Human):
                h.should_play(int(self._slot.y), int(self._slot.x))

    # Overrides

    def draw(self, surface):
        super().draw(surface)
        
        # Drawing token
        token = self._board.get_at(int(self._slot.y), int(self._slot.x))
            # case Board.WHITE:
            #     # pg.draw.ellipse(surface, 'white', self._absolute.as_rect())
            #     image_rect = (0, 0, 64, 64)
            # case Board.BLACK:
            #     # pg.draw.ellipse(surface, 'black', self._absolute.as_rect())
            #     image_rect = (254 * self.IMAGE_SCALE, 0, 64, 64)
            # case Board.EMPTY:
            #     pass
        self._flip_delay -= 1
        if self._flip_delay == 0:
            self._flip_delay = self.MAX_FLIP_DELAY
            
            if token == Board.WHITE and self._image_rect[0] > 0:
                self._image_rect[0] -= 64 * self.IMAGE_SCALE
                if self._image_rect[0] < 0:
                    self._image_rect[0] = 0
            elif token == Board.BLACK and self._image_rect[0] < 254 * self.IMAGE_SCALE:
                self._image_rect[0] += 64 * self.IMAGE_SCALE 
                if self._image_rect[0] > 254 * self.IMAGE_SCALE:
                    self._image_rect[0] = 254 * self.IMAGE_SCALE
            

        if token != Board.EMPTY:
            image_coords = self._absolute.as_rect()

            surface.blit(self.TOKEN_SPRITESHEET, (image_coords.x, image_coords.y), self._image_rect)

        # Draw little cursor on hover
        if self._state == "hover":
            col = [i * 0.9 for i in self.get_true_color()]
            rec = self._absolute.as_rect()
            rec.left += 10
            rec.top += 10
            rec.width -= 20
            rec.height -= 20

            pg.draw.rect(surface, col, rec, border_radius = 10)

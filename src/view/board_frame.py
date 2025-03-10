import pygame as pg

from view.frame import Frame

class BoardFrame (Frame):
    def __init__(self, board, fill = "dark grey", position = pg.Vector2(0, 0), size = pg.Vector2(1, 1), children = []):
        super().__init__(True, fill, position, size, children)
        self._board = board

    # Overrides

    def draw(self, surface):
        super().draw(surface)

        rect = self._absolute.as_rect()
        rect.left += 15
        rect.top += 15
        rect.width -= 30
        rect.height -= 30
        pg.draw.rect(surface, "grey", rect)

        slot_size = pg.Vector2(rect.width, rect.height)/self._board.board_size

        for i in range(self._board.board_size+1):
            # Draw horizontal line
            pg.draw.line(
                surface,
                "black",
                (
                    rect.left,
                    rect.top + slot_size.y * i
                ),
                (
                    rect.left + rect.width,
                    rect.top + slot_size.y * i
                )
            )
            # Draw vertical line
            pg.draw.line(
                surface,
                "black",
                (
                    rect.left + slot_size.x * i,
                    rect.top
                ),
                (
                    rect.left + slot_size.x * i,
                    rect.top + rect.height
                )
            )

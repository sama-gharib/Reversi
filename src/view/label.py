from view.widget import Widget

import pygame as pg

class Label (Widget):
    def __init__(self, text = "placeholder", position = pg.Vector2(0, 0), size = pg.Vector2(1, 1), children = []):
        self._string = text
        self._font_size = 32
        self._font = pg.font.Font(None, self._font_size)
        super().__init__(position, size, children)

    def _recalculate_font_size(self):
        if self._absolute.size.x < 10:
            return
        current_width = self._font.size(self._string)[0]
        desired_width = self._absolute.size.x
        self._font_size *= desired_width / current_width
        self._font = pg.font.Font(None, int(self._font_size))
        self._text = self._font.render(self._string, True, "black")

    # Override
    def event(self, e):
        # Label are non-interactible
        return False

    def _recalculate_absolutes(self, parent_absolute):
        super()._recalculate_absolutes(parent_absolute)
        self._recalculate_font_size()

    def draw(self, surface):
        surface.blit(self._text, self._absolute.position)
import pygame as pg

from view.widget import Widget

class Frame (Widget):
    
    def __init__(self, rounded = True, fill = "dark grey", position = pg.Vector2(0, 0), size = pg.Vector2(1, 1), children = []):
        super().__init__(position, size, children)
        self._fill = fill
        self._rounded = rounded

    # Overrides

    def draw(self, surface):
        
        br = 20 if self._rounded else 0

        super().draw(surface, self._fill, br)

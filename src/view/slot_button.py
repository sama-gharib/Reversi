import pygame as pg

from view.button import Button

class SlotButton (Button):

    def __init__(self, position = pg.Vector2(0, 0), size = pg.Vector2(1, 1), children = []):
        super().__init__(lambda: print("TODO!!"), (200, 200, 200), position, size, children)

    # Overrides

    def draw(self, surface):
        super().draw(surface)
        
        if self._state == "hover":
            col = [i * 0.9 for i in self.get_true_color()]
            rec = self._absolute.as_rect()
            rec.left += 10
            rec.top += 10
            rec.width -= 20
            rec.height -= 20

            pg.draw.rect(surface, col, rec, border_radius = 10)

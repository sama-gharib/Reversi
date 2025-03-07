from view.widget import Widget
from view.label import Label
from view.frame import Frame

import pygame as pg

class Button (Widget):
    COLORS = {
        "rest"    : (1, 1, 1),
        "hover"   : (0.75, 0.75, 0.75),
        "press"   : (0.25, 0.25, 0.25)
    }

    def __init__(self, callback = None, color = (255, 255, 255), position = pg.Vector2(0, 0), size = pg.Vector2(1, 1), children = []):
        super().__init__(position, size, children)
        self._callback = callback
        self._color = color
        self._state = "rest"

    def get_true_color(self):
        return (
            self._color[0] * self.COLORS[self._state][0],
            self._color[1] * self.COLORS[self._state][1],
            self._color[2] * self.COLORS[self._state][2]
        )

    # Overrides

    def draw(self, surface):
        super().draw(surface, self.get_true_color())

    def has_event(self, e):
        if e.type == pg.MOUSEMOTION and self._state != "press":
            self._state = "hover"
        elif e.type == pg.MOUSEBUTTONDOWN:
            self._state = "press"
        elif e.type == pg.MOUSEBUTTONUP:
            self._state = "hover"
            self._callback()

    def miss_event(self, e):
        if e.type == pg.MOUSEBUTTONUP or e.type == pg.MOUSEMOTION and self._state != "press":
            self._state = "rest"


def demo():
    # Button demo
    pg.init()
    surface = pg.display.set_mode((800, 600))

    
    w = Frame(
        False, (98, 111, 71),
        pg.Vector2(0, 0),
        pg.Vector2(800, 600),
        [
            Label(
                "Exemple d'interface",
                pg.Vector2(0.1, 0.1),
                pg.Vector2(0.8, 0.3)
            ),
            Frame(
                True, (164, 180, 101),
                pg.Vector2(0.1, 0.3),
                pg.Vector2(0.8, 0.6),
                [
                    Button(
                        (255, 207, 80),
                        pg.Vector2(0.1, 0.1),
                        pg.Vector2(0.3, 0.1),
                        [
                            Label(
                                "Bouton exemple",
                                pg.Vector2(0.1, 0.1),
                                pg.Vector2(0.8, 0.8)
                            )
                        ]
                    ),
                    Button(
                        (255, 207, 80),
                        pg.Vector2(0.6, 0.1),
                        pg.Vector2(0.3, 0.1),
                        [
                            Label(
                                "Autre bouton",
                                pg.Vector2(0.1, 0.1),
                                pg.Vector2(0.8, 0.8)
                            )
                        ]
                    )
                ]
            )
        ]
    )
    
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            else:
                w.event(event)

        surface.fill("black")
        w.draw(surface)
        pg.display.flip()
from view.widget import Widget
from utils import ReactiveStr

import pygame as pg

class Label (Widget):
    def __init__(self, text: ReactiveStr, position = pg.Vector2(0, 0), size = pg.Vector2(1, 1), children = []):
        if not isinstance(text, ReactiveStr):
            raise TypeError(
"Please only use `utils.ReactiveStr` as text argument for `Label`.\nPlease change the following : \n\
``` \n\
\ta = Label('[your str]'), [...]) \n\
```\n\
To : \n\
``` \n\
\ta = Label(ReactiveStr('[your str]', [...])\n\
```\
"         )
        
        self._string = text
        self._font_size = 32
        self._font = pg.font.Font(None, self._font_size)
        super().__init__(position, size, children)

    def _update_text(self):
        self._text = self._font.render(self._string.value, True, "black")
        
    def _recalculate_font_size(self):
        if self._absolute.size.x < 10:
            return
        current_width = self._font.size(self._string.value)[0]
        desired_width = self._absolute.size.x
        self._font_size *= desired_width / current_width
        self._font = pg.font.Font(None, int(self._font_size))
        self._update_text()

    # Override
    def event(self, e):
        # Label are non-interactible
        return False

    def _recalculate_absolutes(self, parent_absolute):
        super()._recalculate_absolutes(parent_absolute)
        self._recalculate_font_size()

    def draw(self, surface):
        self._update_text()
        surface.blit(self._text, self._absolute.position)
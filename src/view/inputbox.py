import pygame as pg
from view.widget import Widget

class InputBox(Widget):
    def __init__(self, on_change, position=pg.Vector2(0, 0), size=pg.Vector2(1, 1), default_text="98"):
        super().__init__(position, size)
        self.on_change = on_change  # Callback function triggered when the input value changes
        self.text = default_text
        self.active = False

    def draw(self, surface, color="white", border_radius=0):
        # Change border color when selected
        border_color = (0, 0, 255) if self.active else (0, 0, 0)
        
        # Draw the input box background
        pg.draw.rect(surface, color, (*self._absolute.position, *self._absolute.size), border_radius=border_radius)
        pg.draw.rect(surface, border_color, (*self._absolute.position, *self._absolute.size), 2, border_radius)
        
        # Draw the text
        font = pg.font.Font(None, 32)
        text_surface = font.render(self.text, True, (0, 0, 0))
        surface.blit(text_surface, (self._absolute.position.x + 5, self._absolute.position.y + 5))

    def event(self, e):
        if e.type == pg.MOUSEBUTTONDOWN:
            mouse = pg.Vector2(pg.mouse.get_pos())
            if (self._absolute.position.x <= mouse.x <= self._absolute.position.x + self._absolute.size.x and
                self._absolute.position.y <= mouse.y <= self._absolute.position.y + self._absolute.size.y):
                self.active = True
                if self.text in ["98", "111", "71"]:
                    self.text = ""  # Clear default text when selected
            else:
                if self.text == "":
                    self.text = "98"  # Set to default value if empty when losing focus
                else:
                    self.text = str(min(int(self.text), 255))  # Limit the maximum value to 255
                self.active = False
                self.on_change(self.text)  # Trigger callback to ensure value update
        
        if e.type == pg.KEYDOWN and self.active:
            if e.key == pg.K_BACKSPACE:
                self.text = self.text[:-1]
            elif e.unicode.isdigit():  # Only accept numeric input
                if len(self.text) < 3:
                    self.text += e.unicode
                self.text = str(min(int(self.text), 255))  # Limit the maximum value to 255
                self.on_change(self.text)  # Call the callback function
        return True
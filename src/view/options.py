from view.frame import Frame
import random

class Options:
    def __init__(self, ui, default_color=(98, 111, 71), default_difficulty="medium"):
        self.ui = ui  # Reference to the Ui object for updating the interface
        self.current_color = default_color  # Current interface color
        self.current_difficulty = default_difficulty  # Current difficulty level
        self.temp_color = list(default_color)  # Temporarily stores user-input RGB values

    def set_color(self, color):
        self.current_color = color
        self._update_ui_color()

    def set_temp_color(self, r, g, b):
        self.temp_color = [r, g, b]

    def apply_temp_color(self):
        self.set_color(tuple(self.temp_color))

    def random_color(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        self.set_temp_color(r, g, b)
        self.apply_temp_color()

    def set_difficulty(self, difficulty):
        if difficulty in ["easy", "medium", "hard"]:
            self.current_difficulty = difficulty
            print(f"Difficulty set to: {difficulty}")
        else:
            raise ValueError("Invalid difficulty level. Choose from 'easy', 'medium', or 'hard'.")

    def _update_ui_color(self):
        for tab_name, tab_frame in self.ui._tabs.items():
            if isinstance(tab_frame, Frame): 
                tab_frame.set_background_color(self.current_color)
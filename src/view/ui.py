from view.button import Button
from view.frame import Frame
from view.label import Label
from view.options import Options
from view.inputbox import InputBox

import pygame as pg

# Gère l'affichage et l'interaction avec les différents onglets
class Ui:
	def __init__(self, tabs: dict, start_on: str):
		self._tabs = tabs # Dictionnaire de widgets racines
		self._current_tab = start_on
		self._font = pg.font.Font(None, 32)
		self._error_text = self._font.render("Erreur: Aucun onglet selectionné", True, "black")
		self._request_quit = False

	def request_quit(self):
		self._request_quit = True

	def has_quit(self):
		return self._request_quit

	def set_tab(self, new_tab: str):
		if new_tab in self._tabs.keys():
			self._current_tab = new_tab
		else:
			raise ValueError(f'Unexisting tab : {new_tab}')

	def draw(self, screen):
		if self._current_tab == None:
			screen.blit(self._error_text, (100, 100))
		else:
			self._tabs[self._current_tab].draw(screen)

	def event(self, event):
		if self._current_tab != None:
			self._tabs[self._current_tab].event(event)

def default_ui():
    default_callback = lambda: print("Not implemented.")
    options = Options(None)  

    default = Ui({}, None)
    default._tabs = {
        "main_menu": Frame(
            rounded=False,
            fill=(98, 111, 71),  
            position=pg.Vector2(0, 0),
            size=pg.Vector2(800, 600),
            children=[
                Label(
                    "Reversi",
                    pg.Vector2(0.25, 0.05),
                    pg.Vector2(0.5, 0.1)
                ),
                Frame(
                    rounded=True,
                    fill=(164, 180, 101),
                    position=pg.Vector2(0.35, 0.3),
                    size=pg.Vector2(0.3, 0.6),
                    children=[
                        Button(
                            default_callback,
                            (255, 207, 80),
                            pg.Vector2(0.25, 0.15),
                            pg.Vector2(0.5, 0.2),
                            [
                                Label(
                                    "Play !",
                                    pg.Vector2(0.25, 0.3),
                                    pg.Vector2(0.55, 0.6)
                                )
                            ]
                        ),
                        Button(
                            lambda: default.set_tab("options"),
                            (255, 207, 80),
                            pg.Vector2(0.25, 0.4),
                            pg.Vector2(0.5, 0.2),
                            [
                                Label(
                                    "Options",
                                    pg.Vector2(0.1, 0.3),
                                    pg.Vector2(0.8, 0.6)
                                )
                            ]
                        ),
                        Button(
                            lambda: default.set_tab("quit"),
                            (255, 207, 80),
                            pg.Vector2(0.25, 0.65),
                            pg.Vector2(0.5, 0.2),
                            [
                                Label(
                                    " Quit ",
                                    pg.Vector2(0.2, 0.3),
                                    pg.Vector2(0.55, 0.6)
                                )
                            ]
                        )
                    ]
                )
            ]
        ),
        "options": Frame(
            rounded=False,
            fill=(98, 111, 71),  
            position=pg.Vector2(0, 0),
            size=pg.Vector2(800, 600),
            children=[
                Label(
                    "Options",
                    pg.Vector2(0.25, 0.05),
                    pg.Vector2(0.5, 0.1)
                ),
                Frame(
                    rounded=True,
                    fill=(164, 180, 101),
                    position=pg.Vector2(0.35, 0.3),
                    size=pg.Vector2(0.3, 0.6),
                    children=[
                        Button(
                            lambda: default.set_tab("options_color"),
                            (255, 207, 80),
                            pg.Vector2(0.25, 0.15),
                            pg.Vector2(0.5, 0.2),
                            [
                                Label(
                                    "Color",
                                    pg.Vector2(0.25, 0.3),
                                    pg.Vector2(0.55, 0.6)
                                )
                            ]
                        ),
                        Button(
                            default_callback,
                            (255, 207, 80),
                            pg.Vector2(0.25, 0.4),
                            pg.Vector2(0.5, 0.2),
                            [
                                Label(
                                    "Difficult",
                                    pg.Vector2(0.1, 0.3),
                                    pg.Vector2(0.8, 0.6)
                                )
                            ]
                        ),
                        Button(
                            lambda: default.set_tab("main_menu"),
                            (255, 207, 80),
                            pg.Vector2(0.25, 0.65),
                            pg.Vector2(0.5, 0.2),
                            [
                                Label(
                                    "Back",
                                    pg.Vector2(0.2, 0.3),
                                    pg.Vector2(0.55, 0.6)
                                )
                            ]
                        )
                    ]
                )
            ]
        ),
        "options_color": Frame(
            rounded=False,
            fill=(98, 111, 71),  
            position=pg.Vector2(0, 0),
            size=pg.Vector2(800, 600),
            children=[
                Label(
                    "Color Options",
                    pg.Vector2(0.25, 0.05),
                    pg.Vector2(0.5, 0.1)
                ),
                Frame(
                    rounded=True,
                    fill=(164, 180, 101),
                    position=pg.Vector2(0.35, 0.3),
                    size=pg.Vector2(0.3, 0.6),
                    children=[
                        Label(
                            "R:",
                            pg.Vector2(0.1, 0.1),
                            pg.Vector2(0.1, 0.1)
                        ),
                        InputBox(
                            lambda val: options.set_temp_color(int(val), options.temp_color[1], options.temp_color[2]),
                            pg.Vector2(0.2, 0.1),
                            pg.Vector2(0.2, 0.1)
                        ),
                        Label(
                            "G:",
                            pg.Vector2(0.1, 0.25),
                            pg.Vector2(0.1, 0.1)
                        ),
                        InputBox(
                            lambda val: options.set_temp_color(options.temp_color[0], int(val), options.temp_color[2]),
                            pg.Vector2(0.2, 0.25),
                            pg.Vector2(0.2, 0.1)
                        ),
                        Label(
                            "B:",
                            pg.Vector2(0.1, 0.4),
                            pg.Vector2(0.1, 0.1)
                        ),
                        InputBox(
                            lambda val: options.set_temp_color(options.temp_color[0], options.temp_color[1], int(val)),
                            pg.Vector2(0.2, 0.4),
                            pg.Vector2(0.2, 0.1)
                        ),
                        Button(
                            options.random_color,
                            (200, 200, 200),
                            pg.Vector2(0.5, 0.1),
                            pg.Vector2(0.3, 0.1),
                            [
                                Label(
                                    "Random",
                                    pg.Vector2(0.1, 0.1),
                                    pg.Vector2(0.8, 0.8)
                                )
                            ]
                        ),
                        Button(
                            options.apply_temp_color,
                            (200, 200, 200),
                            pg.Vector2(0.5, 0.25),
                            pg.Vector2(0.3, 0.1),
                            [
                                Label(
                                    "Apply",
                                    pg.Vector2(0.1, 0.1),
                                    pg.Vector2(0.8, 0.8)
                                )
                            ]
                        ),
                        Button(
                            lambda: default.set_tab("options"),
                            (200, 200, 200),
                            pg.Vector2(0.5, 0.4),
                            pg.Vector2(0.3, 0.1),
                            [
                                Label(
                                    "Back",
                                    pg.Vector2(0.1, 0.1),
                                    pg.Vector2(0.8, 0.8)
                                )
                            ]
                        )
                    ]
                )
            ]
        ),
        "quit": Frame(
            rounded=False,
            fill=(98, 111, 71),  
            position=pg.Vector2(0, 0),
            size=pg.Vector2(800, 600),
            children=[
                Label(
                    "Êtes vous sur de vouloir quitter ?",
                    pg.Vector2(0.1, 0.1),
                    pg.Vector2(0.8, 0.2)
                ),
                Button(
                    lambda: default.set_tab("main_menu"),
                    (200, 200, 200),
                    pg.Vector2(0.2, 0.45),
                    pg.Vector2(0.1, 0.1),
                    [
                        Label(
                            "Rester",
                            pg.Vector2(0.1, 0.1),
                            pg.Vector2(0.8, 0.8)
                        )
                    ]
                ),
                Button(
                    default.request_quit,
                    (255, 0, 0),
                    pg.Vector2(0.7, 0.45),
                    pg.Vector2(0.1, 0.1),
                    [
                        Label(
                            "Quitter",
                            pg.Vector2(0.1, 0.1),
                            pg.Vector2(0.8, 0.8)
                        )
                    ]
                )
            ]
        )
    }

    default.set_tab("main_menu")
    options.ui = default  # Permet à Options de mettre à jour la couleur de l'onglet actuel
    return default
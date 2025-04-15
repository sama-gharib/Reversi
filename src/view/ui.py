from view.button import Button
from view.frame import Frame
from view.label import Label
from view.options import Options
from view.inputbox import InputBox
from view.board_frame import BoardFrame
from utils import ReactiveStr

import sqlite3 as sql
import pygame as pg
from copy import deepcopy

# Gère l'affichage et l'interaction avec les différents onglets
class Ui:
	def __init__(self, tabs: dict, start_on: str):
		self._tabs = tabs # Dictionnaire de widgets racines
		self._current_tab = start_on
		self._font = pg.font.Font(None, 32)
		self._error_text = self._font.render("Erreur: Aucun onglet selectionné", True, "black")
		self._request_quit = False
		self._mode = False

	def request_quit(self):
		self._request_quit = True

	def has_quit(self):
		return self._request_quit

	def set_tab(self, new_tab: str):
		if new_tab in self._tabs.keys():
			self._current_tab = new_tab
		else:
			raise ValueError(f'Unexisting tab : {new_tab}')
	
	def get_tab_name(self):
		return self._current_tab

	def mode_change(self):
		print("[DEBUG] Mode change triggered!")
		self._mode = True

	def draw(self, screen):
		if self._current_tab == None:
			screen.blit(self._error_text, (100, 100))
		else:
			self._tabs[self._current_tab].draw(screen)

	def event(self, event):
		if self._current_tab != None:
			self._tabs[self._current_tab].event(event)


def default_ui(app):
	default_callback = lambda: print("Not implemented.")
	options = Options(None)

	black_callbacks, white_callbacks = create_player_callbacks(app)
	black_player_choices = create_player_choices(black_callbacks, app.KNOWN_BLACK_PLAYERS, "black")
	white_player_choices = create_player_choices(white_callbacks, app.KNOWN_WHITE_PLAYERS, "white")

	default = Ui({}, "main_menu")
	default._tabs = {
		"main_menu": create_main_menu_frame(default),
		"history": create_history_menu_frame(default),
		"options": create_options_frame(default, default_callback),
		"options_color": create_color_options_frame(default, options),
		"game_ui": create_game_ui_frame(default, app),
		"game": create_game_frame(default, app, black_player_choices, white_player_choices),
		"quit": create_quit_frame(default)
	}

	default.set_tab("main_menu")
	options.ui = default
	return default

def create_player_callbacks(app):
	black_callbacks = [lambda p=a_player: app.set_black_key(p) for a_player in app.KNOWN_BLACK_PLAYERS]
	white_callbacks = [lambda p=a_player: app.set_white_key(p) for a_player in app.KNOWN_WHITE_PLAYERS]
	return black_callbacks, white_callbacks

def create_player_choices(callbacks, players, player_type):
	return [
		Button(
			callbacks[i],
			(255, 207, 80),
			pg.Vector2(0.1, 0.2 + i * 0.78 / len(players)),
			pg.Vector2(0.8, 0.6/len(players)), 
			[
				Label(
					ReactiveStr(a_player),
					pg.Vector2(0.1, 0.1),
					pg.Vector2(0.8, 0.8)
				)
			]
		)
		for a_player, i in zip(players.keys(), range(len(players)))
	]

def create_main_menu_frame(default):
	return Frame(
		rounded=False,
		fill=(98, 111, 71),
		position=pg.Vector2(0, 0), 
		size=pg.Vector2(800, 600),
		children=[
			Label(
				ReactiveStr("Reversi"),
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
						lambda: default.set_tab("game"),
						(255, 207, 80),
						pg.Vector2(0.25, 0.15),
						pg.Vector2(0.5, 0.15),
						[
							Label(
								ReactiveStr("Play !"),
								pg.Vector2(0.25, 0.3),
								pg.Vector2(0.55, 0.6)
							)
						]
					),
					Button(
						lambda: default.set_tab("history"),
						(255, 207, 80),
						pg.Vector2(0.25, 0.32),
						pg.Vector2(0.5, 0.15),
						[
							Label(
								ReactiveStr("History"),
								pg.Vector2(0.15, 0.3),
								pg.Vector2(0.7, 0.6)
							)
						]
					),
					Button(
						lambda: default.set_tab("options"),
						(255, 207, 80),
						pg.Vector2(0.25, 0.49),
						pg.Vector2(0.5, 0.15),
						[
							Label(
								ReactiveStr("Options"),
								pg.Vector2(0.1, 0.3),
								pg.Vector2(0.8, 0.6)
							)
						]
					),
					Button(
						lambda: default.set_tab("quit"),
						(255, 207, 80),
						pg.Vector2(0.25, 0.66),
						pg.Vector2(0.5, 0.15),
						[
							Label(
								ReactiveStr(" Quit "),
								pg.Vector2(0.2, 0.3),
								pg.Vector2(0.55, 0.6)
							)
						]
					)
				]
			)
		]
	)

def create_history_menu_frame(default):
	# Récupération des parties depuis la BD
	bd = sql.connect('res/database/saved_games.sqlite')
	past_games = bd.execute('''
		select
			g.precedence, w.strategy, w.score, b.strategy, b.score
		from
			Game g, Player w, Player b
		where
			g.white = w.id and
			g.black = b.id
		order by
			g.precedence
	''').fetchall()

	to_return = Frame(
		rounded = False,
		fill=(98, 111, 71),
		position=pg.Vector2(0, 0),
		size=pg.Vector2(800, 600),
		children = [
			Label(
				ReactiveStr("History"),
				pg.Vector2(0.3, 0.05),
				pg.Vector2(0.4, 0.1)
			),
			Button(
				lambda: default.set_tab("main_menu"),
				(200, 200, 200),
				pg.Vector2(0.01, 0.01),
				pg.Vector2(0.2, 0.05),
				[
					Label(
						ReactiveStr("Main menu"),
						pg.Vector2(0.1, 0.1),
						pg.Vector2(0.8, 0.8)
					)
				]
			),

		] + [
			Frame(
				rounded = True,
				fill = (200, 200, 200) if game[2] > game[4] else (100, 100, 100),
				position = pg.Vector2(0.25, 0.25 + i * 0.11),
				size = pg.Vector2(0.5, 0.1),
				children = [
					Label(
						ReactiveStr(f'Game {game[0]}'),
						pg.Vector2(0.42, 0.1),
						pg.Vector2(0.16, 0.1)
					),
					Label(
						ReactiveStr(f'White ({game[1]})'),
						pg.Vector2(0.05, 0.2),
						pg.Vector2(0.35, 0.1)
					),
					Label(
						ReactiveStr(f'Score : {game[2]}'),
						pg.Vector2(0.05, 0.55),
						pg.Vector2(0.2, 0.1)
					),
					Label(
						ReactiveStr(f'Black ({game[3]})'),
						pg.Vector2(0.6, 0.2),
						pg.Vector2(0.35, 0.1)
					),
					Label(
						ReactiveStr(f'Score : {game[4]}'),
						pg.Vector2(0.74, 0.55),
						pg.Vector2(0.2, 0.1)
					),
				]
			)
			for i, game in enumerate(past_games)
		]

	)

	return to_return

def create_options_frame(default, default_callback):
	return Frame(
		rounded=False,
		fill=(98, 111, 71),
		position=pg.Vector2(0, 0),
		size=pg.Vector2(800, 600),
		children=[
			Label(
				ReactiveStr("Options"),
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
								ReactiveStr("Color"),
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
								ReactiveStr("Difficult"),
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
								ReactiveStr("Back"),
								pg.Vector2(0.2, 0.3),
								pg.Vector2(0.55, 0.6)
							)
						]
					)
				]
			)
		]
	)

def create_color_options_frame(default, options):
	return Frame(
		rounded=False,
		fill=(98, 111, 71),
		position=pg.Vector2(0, 0),
		size=pg.Vector2(800, 600),
		children=[
			Label(
				ReactiveStr("Color Options"),
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
						ReactiveStr("R:"),
						pg.Vector2(0.1, 0.1),
						pg.Vector2(0.1, 0.1)
					),
					InputBox(
						lambda val: options.set_temp_color(int(val), options.temp_color[1], options.temp_color[2]),
						pg.Vector2(0.2, 0.1),
						pg.Vector2(0.2, 0.1)
					),
					Label(
						ReactiveStr("G:"),
						pg.Vector2(0.1, 0.25),
						pg.Vector2(0.1, 0.1)
					),
					InputBox(
						lambda val: options.set_temp_color(options.temp_color[0], int(val), options.temp_color[2]),
						pg.Vector2(0.2, 0.25),
						pg.Vector2(0.2, 0.1)
					),
					Label(
						ReactiveStr("B:"),
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
								ReactiveStr("Random"),
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
								ReactiveStr("Apply"),
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
								ReactiveStr("Back"),
								pg.Vector2(0.1, 0.1),
								pg.Vector2(0.8, 0.8)
							)
						]
					)
				]
			)
		]
	)

def create_game_ui_frame(default, app):
	return Frame(
		False,
		(98, 111, 71),
		pg.Vector2(0, 0),
		pg.Vector2(800, 600),
		[
			Button(
				lambda: default.set_tab("game"),
				(200, 200, 200),
				pg.Vector2(0.01, 0.01),
				pg.Vector2(0.1, 0.05),
				[
					Label(
						ReactiveStr("Back"),
						pg.Vector2(0.1, 0.1),
						pg.Vector2(0.8, 0.6)
					)
				]
			),
			Button(
				lambda: app.restart(),
				(200, 200, 200),
				pg.Vector2(0.88, 0.01),
				pg.Vector2(0.1, 0.05),
				[
					Label(
						ReactiveStr("Restart"),
						pg.Vector2(0.13, 0.18),
						pg.Vector2(0.8, 0.8)
					)
				]
			),
			BoardFrame(
				app._board,
				[app.KNOWN_WHITE_PLAYERS['human'], app.KNOWN_BLACK_PLAYERS['human']],
				(100, 100, 100),
				pg.Vector2(0.2, 0.1),
				pg.Vector2(0.6, 0.6 * 4/3)
			)
		]
	)

def create_game_frame(default, app, black_player_choices, white_player_choices):
	return Frame(
		rounded=False,
		fill=(98, 111, 71),
		position=pg.Vector2(0, 0),
		size=pg.Vector2(800, 600),
		children=[
			Label(
				ReactiveStr("Players"),
				pg.Vector2(0.35, 0.05),
				pg.Vector2(0.3, 0.05)
			),
			Label(
				app.get_black_key(),
				pg.Vector2(0.35, 0.15),
				pg.Vector2(0.1, 0.02)
			),
			Label(
				app.get_white_key(),
				pg.Vector2(0.55, 0.15),
				pg.Vector2(0.1, 0.02)
			),
			Button(
				lambda: default.set_tab("game_ui"),
				(255, 207, 80),
				pg.Vector2(0.45, 0.45),
				pg.Vector2(0.1, 0.1),
				[
					Label(
						ReactiveStr("Start"),
						pg.Vector2(0.1, 0.3),
						pg.Vector2(0.8, 0.8)
					)
				]
			),
			Button(
				lambda: default.set_tab("main_menu"),
				(200, 200, 200),
				pg.Vector2(0.01, 0.01),
				pg.Vector2(0.2, 0.05),
				[
					Label(
						ReactiveStr("Main menu"),
						pg.Vector2(0.1, 0.1),
						pg.Vector2(0.8, 0.8)
					)
				]
			),
			Frame(
				rounded = True,
				fill = (164, 180, 101),
				position=pg.Vector2(0.1, 0.2),
				size=pg.Vector2(0.25, 0.7),
				children=[
					Label(
						ReactiveStr("Black"),
						pg.Vector2(0.1, 0.05),
						pg.Vector2(0.8, 0.2)
					)
				] + black_player_choices
			),
			Frame(
				rounded = True,
				fill = (164, 180, 101),
				position=pg.Vector2(0.65, 0.2),
				size=pg.Vector2(0.25, 0.7),
				children=[
					Label(
						ReactiveStr("White"),
						pg.Vector2(0.1, 0.05),
						pg.Vector2(0.8, 0.2)
					)
				] + white_player_choices
			)
		]
	)

def create_quit_frame(default):
	return Frame(
		rounded=False,
		fill=(98, 111, 71),
		position=pg.Vector2(0, 0),
		size=pg.Vector2(800, 600),
		children=[
			Label(
				ReactiveStr("Êtes vous sur de vouloir quitter ?"),
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
						ReactiveStr("Rester"),
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
						ReactiveStr("Quitter"),
						pg.Vector2(0.1, 0.1),
						pg.Vector2(0.8, 0.8)
					)
				]
			)
		]
	)

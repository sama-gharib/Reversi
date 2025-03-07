import application
import pygame as pg

from view.button import demo
from view.ui import default_ui
from application import Application

import sys

if __name__ == '__main__':
	argc = len(sys.argv)

	if argc == 1:
		print('Bienvenue dans le Reversi !')

		pg.init()
		app = Application(default_ui())
		app.run()

		print('Fini.')

	elif argc == 2 and sys.argv[1] == "uidemo":
		demo()
	else:
		print("/!\\ Suite d'argument inconnue /!\\")
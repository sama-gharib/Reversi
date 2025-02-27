import application
import pygame as pg
from view.button import demo

import sys

if __name__ == '__main__':
	argc = len(sys.argv)

	if argc == 1:
		print('Bienvenue dans le Reversi !')

		# Le jeu n'est pas encore implémenté, on affiche une erreur
		raise NotImplementedError

	elif argc == 2 and sys.argv[1] == "uidemo":
		demo()
	else:
		print("/!\\ Suite d'argument inconnue /!\\")
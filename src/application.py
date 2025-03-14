from model.board import Board
from model.human import Human
from model.stupidity import Stupidity
from view.ui import default_ui

import pygame

class Application:
	def __init__(self):
		self._board = Board()
		self._white_player = Stupidity()
		self._black_player = Human()

		self._ui = default_ui(self._board, [self._white_player, self._black_player])

	def run(self):
		screen = pygame.display.set_mode((800, 600))
		clock = pygame.time.Clock()
		running = True

		black_playing = False
		while running and not self._ui.has_quit():

			# Player turn rules
			if black_playing and self._black_player.is_done():
				print("[DEBUG] White's turn")
				black_playing = False
				self._white_player.play_on(self._board)

			if not black_playing and self._white_player.is_done():
				print("[DEBUG] Black's turn")
				black_playing = True
				self._black_player.play_on(self._board)

			# Check if the game is over
			if self._board.is_game_over():
				winner = self._board.get_winner()
				if winner == self._board.BLACK:
					print("[DEBUG] Game Over! Black wins!")
				elif winner == self._board.WHITE:
					print("[DEBUG] Game Over! White wins!")
				else:
					print("[DEBUG] Game Over! It's a tie!")
				running = False  # End the game

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
				else:
					self._ui.event(event)

			screen.fill("white")

			self._ui.draw(screen)

			pygame.display.flip()

			clock.tick(60)

		pygame.quit()
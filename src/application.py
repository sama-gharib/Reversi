import model.model

import pygame

class Application:
	def __init__(self, ui):
		self._ui = ui


	def run(self):
		screen = pygame.display.set_mode((800, 600))
		clock = pygame.time.Clock()
		running = True

		while running and not self._ui.has_quit():

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
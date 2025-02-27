import pygame as pg

from utils import Box

# Root class for every interactive UI component
# (buttons, text fields, drop down list...)
class Widget:
	
	# A widget is a tree

	def __init__(self, position = pg.Vector2(0, 0), size = pg.Vector2(1, 1), children = []):
		self._relative = Box(position, size) # Coordinates relative to the parent widget
		self._children = list(children) # Shallow copy to avoid reference conflicts
		self._absolute = Box() # Coordinates relative to the window

		self._recalculate_absolutes(Box())


	def _apply_to_children(self, procedure):
		for child in self._children:
			procedure(child)

	def _recalculate_absolutes(self, parent_absolute):
		self._absolute.position = parent_absolute.position + self._relative.position.elementwise() * parent_absolute.size
		self._absolute.size = parent_absolute.size.elementwise() * self._relative.size

		self._apply_to_children(lambda x: x._recalculate_absolutes(self._absolute))

	def draw(self, surface):
		pg.draw.rect(surface, "white", self._absolute.as_rect(), 2)

		self._apply_to_children(lambda x: x.draw(surface))

if __name__ == "__main__":
	# Widget demo
	pg.init()
	surface = pg.display.set_mode((800, 600))

	
	w = Widget(
		pg.Vector2(100, 100),
		pg.Vector2(300, 200),
		[
			Widget(
				pg.Vector2(0.1, 0.1),
				pg.Vector2(0.8, 0.8),
				[
					Widget(
						pg.Vector2(0.1, 0.1),
						pg.Vector2(0.3, 0.8)
					),
					Widget(
						pg.Vector2(0.6, 0.1),
						pg.Vector2(0.3, 0.8)
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

		surface.fill("black")
		w.draw(surface)
		pg.display.flip()
	
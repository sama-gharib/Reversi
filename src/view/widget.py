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
		results = []
		for child in self._children:
			results.append(procedure(child))
		return results

	def _recalculate_absolutes(self, parent_absolute):
		self._absolute.position = parent_absolute.position + self._relative.position.elementwise() * parent_absolute.size
		self._absolute.size = parent_absolute.size.elementwise() * self._relative.size

		self._apply_to_children(lambda x: x._recalculate_absolutes(self._absolute))

	def draw(self, surface, color = "red", border_radius = 10):
		pg.draw.rect(surface, color, self._absolute.as_rect(), border_radius = border_radius)

		self._apply_to_children(lambda x: x.draw(surface))

	def event(self, e):
		if not (True in self._apply_to_children(lambda x: x.event(e))):
			# Event has not been caught by any child
			mouse = pg.Vector2(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
			if  mouse.x >= self._absolute.position.x \
			and mouse.x <= self._absolute.position.x + self._absolute.size.x \
			and mouse.y >= self._absolute.position.y \
			and mouse.y <= self._absolute.position.y + self._absolute.size.y:
				# The mouse is hovering the widget's position : we catch the event

				self.has_event(e)

				return True
			else:

				self.miss_event(e)

				return False

	def has_event(self, e):
		# Do not modify ! This function should fail if
		# the child class on which it is calls does not override it.
		# raise NotImplementedError
		pass

	def miss_event(self, e):
		pass


	
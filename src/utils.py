# This script contains utilities classes and functions

import pygame as pg

class Box:
    def __init__(self, position = pg.Vector2(0, 0), size = pg.Vector2(1, 1)):
        self._position = position
        self._size = size

    def get_position(self):
        return self._position

    def set_position(self, p: pg.Vector2):
        old_pos = self._position
        self._position = p
        return old_pos

    def get_size(self):
        return self._size

    def set_size(self, s):
        if s.x < 0 or s.y < 0:
            raise ValueError("Tried to set negative size for Box")
        old_size = self._size
        self._size = s
        return old_size 

    def as_rect(self):
        return pg.Rect(self._position.x, self._position.y, self._size.x, self._size.y)

    position = property(get_position, set_position)
    size     = property(get_size, set_size)
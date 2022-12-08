#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""main.py: high level game logic"""

__author__ = "Travis Mann"
__version__ = "1.0"
__maintainer__ = "Travis Mann"
__email__ = "tmann.eng@gmail.com"
__status__ = "Production"


# --- imports ---
import pygame
from pygame.math import Vector2


# --- classes ---
class Fruit:
    """
    purpose: fruit object for snake to eat
    """
    def __init__(self, radius: int):
        # attr from params
        self.position = Vector2(0, 0)
        self.radius = radius

        # color
        self.color = (200, 150, 150)

    def draw(self, screen, tile_thickness: int, border_thickness: int) -> None:
        """
        purpose: draw fruit on screen
        :param screen: screen to draw fruit on
        :param border_thickness: grid offset from edge of screen
        """
        # get pixel position from grid position
        x_position = self.position.x * tile_thickness + border_thickness + tile_thickness / 2
        y_position = self.position.y * tile_thickness + border_thickness + tile_thickness / 2


        # draw fruit
        pygame.draw.circle(screen, (183, 111, 122), (x_position, y_position), self.radius)



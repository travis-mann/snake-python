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
class Snake:
    """
    purpose: player controlled snake object
    """
    def __init__(self, segment_size: int):
        self.segment_positions = [Vector2(0, 0), Vector2(0, 1), Vector2(0, 2)]
        self.segment_size = segment_size
        self.direction = Vector2(1, 0)
        self.grow = False  # used to queue growth on next move

        # color
        self.color = [0, 0, 255]

        # track self collision
        self.colliding = False

    def draw(self, screen, border_thickness: int) -> None:
        """
        purpose: draw snake on the screen
        """
        # draw each segment
        for idx, segment_position in enumerate(self.segment_positions):
            x_position = int(segment_position.x * self.segment_size) + border_thickness
            y_position = int(segment_position.y * self.segment_size) + border_thickness
            segment = pygame.Rect(x_position, y_position, self.segment_size, self.segment_size)
            segment_color = (self.color[0], self.color[1],
                             max(0, self.color[2] - idx * 5))
            pygame.draw.rect(screen, segment_color, segment)

    def move(self):
        """
        purpose: move snake between tiles
        """
        if self.grow:  # copy all segments
            new_segment_positions = self.segment_positions[:]
            self.grow = False
        else:  # copy all but last segment
            new_segment_positions = self.segment_positions[:-1]
        # insert new front segment based on current direction
        new_segment_positions.insert(0, new_segment_positions[0] + self.direction)

        # check for collision
        if new_segment_positions[0] in self.segment_positions:
            self.colliding = True
        else:
            self.colliding = False

        # update segment positions
        self.segment_positions = new_segment_positions



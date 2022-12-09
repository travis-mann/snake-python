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
    def __init__(self, segment_size: int,
                 segment_positions: list,
                 starting_direction: Vector2):
        self.segment_positions = segment_positions
        self.segment_size = segment_size
        self.direction = starting_direction
        self.next_direction = starting_direction  # direction to load on next move
        self.grow = True  # used to queue growth on next move
        self.vertical_head_image = pygame.transform.scale(pygame.image.load('./img/snake1/vertical_snake_head.png'),
                                                          (segment_size, segment_size))

        # color
        self.color = [0, 0, 255]

        # track self collision
        self.colliding = False

    def draw(self, board) -> None:
        """
        purpose: draw snake on the screen
        """
        # draw each segment
        for idx, segment_position in enumerate(self.segment_positions):
            x_position = int(segment_position.x * self.segment_size)
            y_position = int(segment_position.y * self.segment_size)
            segment = pygame.Rect(x_position, y_position, self.segment_size, self.segment_size)
            segment_color = (self.color[0], self.color[1],
                             max(0, self.color[2] - idx * 5))
            if idx == 0:
                board.blit(self.vertical_head_image, segment)
            else:
                pygame.draw.rect(board, segment_color, segment)

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
        self.direction = self.next_direction  # update current direction
        new_segment_positions.insert(0, new_segment_positions[0] + self.direction)

        # check for collision
        if new_segment_positions[0] in self.segment_positions:
            self.colliding = True
        else:
            self.colliding = False

        # update segment positions
        self.segment_positions = new_segment_positions


# --- func ---
def rotate_image():
    """
    purpose: rotates an image about its center
    :return: 
    """
    pass


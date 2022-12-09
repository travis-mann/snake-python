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
class Fruit(pygame.sprite.Sprite):
    """
    purpose: fruit object for snake to eat
    """
    def __init__(self,
                 side_length: int,
                 image_fl: str):
        # init parent sprite class
        super().__init__()

        # attr from params
        self.image = pygame.image.load(image_fl)
        self.image = pygame.transform.scale(self.image, (side_length, side_length))  # scale image
        self.rect = self.image.get_rect()  # rectangle around image for placing
        self.position = Vector2(0, 0)
        self.side_length = side_length

    def update(self, tile_offset: Vector2, tile_length: int) -> None:
        """
        purpose: update sprite
        :param tile_offset: pixel offset of tiles top left corner
        :param tile_length: pixel length of a single tile
        """
        self.rect.center = [(self.position.x + 0.5) * tile_length + tile_offset.x,
                            (self.position.y + 0.5) * tile_length + tile_offset.y]

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
        self.image_fl = image_fl
        self.image = pygame.image.load(image_fl)
        self.image = pygame.transform.scale(self.image, (side_length, side_length))  # scale image
        self.rect = self.image.get_rect()  # rectangle around image for placing
        self.position = Vector2(0, 0)
        self.base_side_length = side_length
        self.side_length = side_length

        # animation sizes
        self.grow_direction = 1  # positive or negative tto indicate growing vs shrinking
        self.max_size_ratio = 1.1
        self.min_size_ratio = 0.9
        self.growing = True

    def update(self, tile_length: int) -> None:
        """
        purpose: update sprite
        :param tile_offset: pixel offset of tiles top left corner
        :param tile_length: pixel length of a single tile
        """
        # position fruit
        self.rect.center = [(self.position.x + 0.5) * tile_length,
                            (self.position.y + 0.6) * tile_length]

        # add pulsing animation
        self.pulse()

    def pulse(self) -> None:
        """
        purpose: add pulsing animation to fruit, speed based on a parabola
        """
        # get current growth ratio & grow rate
        size_ratio = self.side_length / self.base_side_length
        grow_rate = self.get_growth_rate_magnitude(size_ratio)

        # swap grow direction if too small or too big
        if size_ratio >= self.max_size_ratio or size_ratio <= self.min_size_ratio:
            self.grow_direction = - self.grow_direction

        # apply growth rate
        self.side_length += grow_rate * self.grow_direction * self.base_side_length

        # update image size
        self.image = pygame.image.load(self.image_fl)
        self.image = pygame.transform.scale(self.image, (self.side_length, self.side_length))  # scale image

    def get_growth_rate_magnitude(self, size_ratio):
        """
        purpose: determine growth rate based on a parabola so it slows as it approaches max size
        """
        magnification_factor = 1.2
        min_growth_rate = 0.006
        # parabola equation
        magnitude = magnification_factor * (size_ratio - self.max_size_ratio)**2 + min_growth_rate
        return magnitude




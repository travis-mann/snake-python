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
class Background:
    """
    purpose: background tiles and border for snake game
    """

    def __init__(self, screen: pygame.display, tile_count: int):
        # attr from params
        self.screen = screen
        self.tile_count = tile_count

        # colors
        self.background_color = (0, 50, 0)  # rgb
        self.tile_colors = ((0, 100, 0), (0, 200, 0))

        # other attr
        self.border_percent = 10
        self.border_thickness = self.screen.get_width() * self.border_percent / 100
        self.tile_size = (self.screen.get_width() - self.border_thickness * 2) / self.tile_count

        # adjust border thickness and tile_size so that the tiles are ints
        self.border_thickness += (self.tile_size - int(self.tile_size)) / 2 * self.tile_count
        self.tile_size = int(self.tile_size)

        # generate tile list
        self.tiles = [Vector2(column_idx, row_idx) for row_idx in range(tile_count) for column_idx in range(tile_count)]

    def draw(self):
        """
        purpose: draw background
        """
        # fill background
        self.screen.fill(self.background_color)

        # draw tiles
        self.draw_tiles()

    def draw_tiles(self) -> None:
        """
        purpose: draw tiles on screen
        """
        # draw tiles
        tile_counter = 0
        for tile_col_idx in range(self.tile_count):
            for tile_row_idx in range(self.tile_count):
                # get tile color
                if tile_counter % 2 == 0:
                    tile_color = self.tile_colors[0]
                else:
                    tile_color = self.tile_colors[1]

                # get tile position
                tile_position_x = self.border_thickness + tile_col_idx * self.tile_size
                tile_position_y = self.border_thickness + tile_row_idx * self.tile_size

                # draw tile
                pygame.draw.rect(self.screen, tile_color,
                                 (tile_position_x, tile_position_y, self.tile_size, self.tile_size))

                # inc counter
                tile_counter += 1





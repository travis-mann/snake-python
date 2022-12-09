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
class Board:
    """
    purpose: main playing board to place items and snake on
    """
    def __init__(self,
                 tile_count: int,
                 length: int):
        # attr from params
        self.tile_count = tile_count

        # create new surface
        self.board = pygame.Surface((length, length))
        self.board_rect = self.board.get_rect()

        # colors
        self.tile_colors = ((0, 100, 0), (0, 200, 0))

        # tiles
        self.tile_size = int(length / self.tile_count)
        # adjust border thickness and tile_size so that the tiles are ints
        self.tile_size = int(self.tile_size)
        # generate tile list
        self.tiles = [Vector2(column_idx, row_idx) for row_idx in range(tile_count) for column_idx in range(tile_count)]

    def draw(self, screen: pygame.display):
        """
        purpose: draw background
        """
        # draw tiles
        self.draw_tiles()

        # place board on screen
        screen.blit(self.board, screen.get_rect().center)

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
                tile_position_x = tile_col_idx * self.tile_size
                tile_position_y = tile_row_idx * self.tile_size

                # draw tile
                pygame.draw.rect(self.board, tile_color,
                                 (tile_position_x, tile_position_y, self.tile_size, self.tile_size))

                # inc counter
                tile_counter += 1


# test
if __name__ == "__main__":
    pygame.init()
    # create screen
    screen = pygame.display.set_mode((1000, 1000))
    # create board
    board = Board(11, 500)
    # game loop
    running = True
    while running:
        board.draw(screen)

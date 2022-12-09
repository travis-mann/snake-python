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

from src.panels.panel import Panel


# --- classes ---
class Board(Panel):
    """
    purpose: main playing board to place items and snake on
    """
    def __init__(self,
                 tile_count: int,
                 size: Vector2,
                 position: Vector2):
        # attr from params
        self.tile_count = tile_count
        print(f'board init pos: {position.x}, {position.y}')

        # colors
        self.tile_colors = ((125, 200, 75),
                            (125, 210, 75))

        # tiles
        self.tile_size = int(size.x / self.tile_count)
        # adjust size and tile_size so that the tiles are ints
        self.tile_size = int(self.tile_size)
        adjusted_length = self.tile_size * tile_count
        self.size = Vector2(adjusted_length, adjusted_length)
        # generate tile list
        self.tiles = [Vector2(column_idx, row_idx) for row_idx in range(tile_count) for column_idx in range(tile_count)]

        # init parent Panel class
        super().__init__(size=self.size,
                         position=position)

    def draw(self) -> None:
        """
        purpose: draw board design and tiles
        """
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
                tile_position_x = tile_col_idx * self.tile_size
                tile_position_y = tile_row_idx * self.tile_size

                # draw tile
                pygame.draw.rect(self.surface, tile_color,
                                 (tile_position_x, tile_position_y, self.tile_size, self.tile_size))

                # inc counter
                tile_counter += 1


# --- test ---
if __name__ == "__main__":
    pygame.init()
    # create screen
    screen = pygame.display.set_mode((1000, 1000))
    length = int(screen.get_width()/2)
    # create board
    board = Board(11,
                  Vector2(length, length),
                  Vector2(screen.get_rect().center))
    # game loop
    print('starting game loop')
    running = True
    while running:
        # handle quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # add delay between loops
        pygame.time.delay(50)
        board.draw()
        pygame.draw.rect(board.surface, (255, 0, 0), (0, 0, 50, 50))
        board.show(screen)
        pygame.display.flip()

    # quit when game loop exited
    pygame.quit()

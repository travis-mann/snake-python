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
        self.length = length

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

    def draw(self) -> None:
        """
        purpose: draw board design and tiles
        """
        # draw tiles
        self.draw_tiles()

    def show(self, screen: pygame.display) -> None:
        """
        purpose: show board on a screen, should be done after everything else is drawn to the board
        """
        # blit board to the screen
        board_x_position = int(screen.get_width() / 2 - self.length / 2)
        board_y_position = int(screen.get_height() / 2 - self.length / 2)
        screen.blit(self.board, (board_x_position, board_y_position))

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
    pos = int(screen.get_height()/2)
    # create board
    board = Board(11, pos)
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
        pygame.draw.rect(board.board, (255, 0, 0), (0, 0, 50, 50))
        board.show(screen)
        pygame.display.flip()

    # quit when game loop exited
    pygame.quit()

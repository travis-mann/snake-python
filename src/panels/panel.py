#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""panel.py: parent class for panels to draw on the screen"""

__author__ = "Travis Mann"
__version__ = "1.0"
__maintainer__ = "Travis Mann"
__email__ = "tmann.eng@gmail.com"
__status__ = "Production"


# --- imports ---
import pygame
from pygame.math import Vector2


# --- classes ---
class Panel:
    """
    purpose: parent class to other display surface panels
    """
    def __init__(self,
                 size: Vector2,
                 position: Vector2,
                 color: tuple = (255, 255, 255),
                 position_on: str = 'center'):

        # attr from params
        self.size = size
        self.position = position
        self.color = color
        self.position_on = position_on

        # main surface
        self.surface = pygame.Surface((size.x, size.y))
        self.surface_rect = self.surface.get_rect()

    def draw(self) -> None:
        """
        purpose: draw panel, to be replaced with more complex draw methods when extended
        """
        print('drawing panel')
        self.surface.fill(self.color)

    def show(self, screen: pygame.display) -> None:
        """
        purpose: show board on a screen, should be done after everything else is drawn to the board
        """
        # draw surface to screen, centered position by default
        surface_rect_kwargs = {self.position_on: self.position}
        self.surface_rect = self.surface.get_rect(**surface_rect_kwargs)
        screen.blit(self.surface, self.surface_rect)



# --- test ---
if __name__ == "__main__":
    pygame.init()
    # create screen
    screen = pygame.display.set_mode((1000, 1000))
    pos = int(screen.get_height() / 2)
    # create board
    panel = Panel(size=Vector2(200, 100),
                  position=Vector2(100, 100),
                  color=(255, 0, 0))
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
        panel.draw()
        pygame.draw.rect(panel.surface, (255, 0, 0), (0, 0, 50, 50))
        panel.show(screen)
        pygame.display.flip()

    # quit when game loop exited
    pygame.quit()

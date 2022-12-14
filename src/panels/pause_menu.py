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
from src.panels.button import Button


# --- classes ---
class PauseMenu(Panel):
    """
    purpose: general pause menu
    """

    def __init__(self,
                 size: Vector2,
                 position: Vector2,
                 color: tuple):

        # init parent Panel class
        super().__init__(size=size,
                         position=position,
                         color=color)

        # buttons
        button_size = Vector2(self.size.x * 0.35, self.size.y * 0.1)
        quit_button_center = Vector2((self.surface_rect.width - button_size.x * 2) / 3 + button_size.x / 2,
                                     self.surface_rect.height - button_size.x)
        continue_button_center = Vector2(self.surface_rect.width - quit_button_center.x,
                                         quit_button_center.y)
        self.quit_button = Button(size=button_size,
                                  position=quit_button_center,
                                  text='Quit?')
        self.continue_button = Button(size=button_size,
                                      position=continue_button_center,
                                      text='Continue!')

        # add image
        image_size = self.size.x * 0.8
        self.image = pygame.transform.scale(pygame.image.load('./img/snake1/head.png'),
                                            (image_size, image_size))
        self.image_rect = self.image.get_rect()
        self.image_rect.center = self.surface_rect.center

        # make surface transparent
        self.surface.set_colorkey((0, 0, 0))

        # background attributes
        self.border_radius = 12

    def draw(self) -> None:
        """
        purpose: draw all elements to pause menu surface
        """
        # fill in pause menu background
        pygame.draw.rect(self.surface, self.color, self.surface.get_rect(), border_radius=self.border_radius)

        # add image
        self.surface.blit(self.image, self.image_rect)

        # add buttons
        self.quit_button.draw(self.surface,
                              self.surface_rect)
        self.continue_button.draw(self.surface,
                                  self.surface_rect)




# --- test ---
if __name__ == "__main__":
    # initialize pygame
    pygame.init()

    # create screen
    screen = pygame.display.set_mode((1000, 1000))
    length = int(screen.get_width() / 2)

    # create button
    pm = PauseMenu(size=Vector2(screen.get_width() * 0.5, screen.get_height() * 0.7),
                   position=Vector2(screen.get_rect().center[0], screen.get_rect().center[0]),
                   color=(200, 200, 200))
    pm.position_on = 'center'

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
        pm.draw()
        pm.show(screen)
        # update screen
        pygame.display.flip()

    # quit when game loop exited
    pygame.quit()
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""score_panel.py: show score and other stats"""

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
class ScorePanel(Panel):
    """
    purpose: panel to display score and other stats
    """
    def __init__(self,
                 size: Vector2,
                 position: Vector2,
                 color: tuple):
        # init parent Panel class
        super().__init__(size=size,
                         position=position,
                         color=color)

        # track score
        self.score = 0
        # text
        self.font = pygame.font.Font('freesansbold.ttf', int(self.size.y * 0.4))

        # place fruit icon
        self.fruit_image = pygame.transform.scale(pygame.image.load('./img/fruit/peach.png'),
                                                  (self.size.y * 0.4, self.size.y * 0.4))
        self.fruit_rect = self.fruit_image.get_rect()
        self.fruit_rect.center = (self.size.x * 0.09, self.size.y * 0.5)

    def draw(self):
        """
        purpose: draw score panel
        """
        # fill background
        self.surface.fill(self.color)

        # draw fruit
        self.surface.blit(self.fruit_image, self.fruit_rect)

        # place score
        score_text = self.font.render(str(self.score), True, (255, 255, 255), self.color)
        text_rect = score_text.get_rect()
        text_rect.midleft = (self.fruit_rect.right + 0.01 * self.size.x, self.fruit_rect.center[1])
        self.surface.blit(score_text, text_rect)


# --- test ---
if __name__ == "__main__":
    pygame.init()
    # create screen
    screen = pygame.display.set_mode((1000, 1000))
    length = int(screen.get_width()/2)
    # create score_panel
    score_panel = ScorePanel(Vector2(screen.get_width(), screen.get_height() * 0.1),
                             Vector2(screen.get_width()/2, 0), color=(0, 50, 0))
    score_panel.position_on = 'midtop'

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
        score_panel.draw()
        score_panel.show(screen)
        pygame.display.flip()

    # quit when game loop exited
    pygame.quit()

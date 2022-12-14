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
class Button:
    """
    purpose: basic clickable button, centered on position
    """
    def __init__(self,
                 size: Vector2,
                 position: Vector2,
                 text: str,
                 top_color: tuple = (0, 0, 255),
                 hover_color: tuple = (255, 0, 0),
                 bottom_color: tuple = (100, 100, 100),
                 font_color: tuple = (255, 255, 255)):

        # params from attr
        self.size = size
        self.position = position
        self.text = text
        self.default_top_color = top_color
        self.top_color = top_color
        self.hover_color = hover_color
        self.bottom_color = bottom_color
        self.font_color = font_color

        # rectangles to form button
        bottom_offset_percent = 0.2  # percent of size shifted down from top
        bottom_position_y = position.y + self.size.y * bottom_offset_percent
        self.top_rectangle = pygame.Rect((0, 0), (size.x, size.y * (1 - bottom_offset_percent)))
        self.bottom_rectangle = pygame.Rect((0, 0), (size.x, size.y * (1 - bottom_offset_percent)))

        # center rects on pos and round corners
        self.top_rectangle.center = position
        self.bottom_rectangle.center = Vector2(position.x, bottom_position_y)
        self.border_radius = 12

        # text
        font = pygame.font.Font(None, int(min(size) * 0.5))
        self.text_surface = font.render(text, True, font_color)
        self.text_rectangle = self.text_surface.get_rect(center=self.top_rectangle.center)

        # track click
        self.pressing = False  # tracks clicking animation
        self.pressed = False  # used to trigger events from button elsewhere

    def draw(self, surface: pygame.Surface,
             surface_rect: pygame.rect) -> None:
        """
        purpose: draw button elements to the given surface
        """
        # draw button side
        pygame.draw.rect(surface, self.bottom_color, self.bottom_rectangle, border_radius=self.border_radius)

        # draw top of the button
        if self.pressing:  # overlap top rect with bottom rect
            pygame.draw.rect(surface, self.top_color, self.bottom_rectangle, border_radius=self.border_radius)
            self.text_rectangle = self.text_surface.get_rect(center=self.bottom_rectangle.center)
        else:  # place top rect above bottom rect
            pygame.draw.rect(surface, self.top_color, self.top_rectangle, border_radius=self.border_radius)
            self.text_rectangle = self.text_surface.get_rect(center=self.top_rectangle.center)

        # draw text to top surface
        surface.blit(self.text_surface, self.text_rectangle)

        # check for a click
        self.check_click(surface_rect)

    def check_click(self, surface_rect: pygame.rect):
        """
        purpose: check if the button has been clicked
        """
        # get mouse position
        mouse_position = pygame.mouse.get_pos()

        # adjust relative to surface
        adjusted_mouse_position_x = mouse_position[0] - surface_rect.left
        adjusted_mouse_position_y = mouse_position[1] - surface_rect.top
        mouse_position = (adjusted_mouse_position_x, adjusted_mouse_position_y)

        # check mouse/button collision
        if self.top_rectangle.collidepoint(mouse_position):
            # update top rectangle color on hover
            self.top_color = self.hover_color

            # check if left click occurred
            if pygame.mouse.get_pressed()[0]:
                # check if current press is already been handled
                if not self.pressing:
                    print('click!')
                    self.pressing = True
            else:  # current press over, reset pressed status
                if self.pressing:  # triggers on the end of a press
                    self.pressing = False
                    self.pressed = True

        else:  # reset top rectangle color
            self.top_color = self.default_top_color


# --- test ---
if __name__ == "__main__":
    # initialize pygame
    pygame.init()

    # create screen
    screen = pygame.display.set_mode((1000, 1000))
    length = int(screen.get_width() / 2)

    # create button
    button = Button(size=Vector2(100, 50),
                    position=Vector2(100, 100),
                    text='Click Me',
                    top_color=(0, 0, 255),
                    hover_color=(255, 0, 0),
                    bottom_color=(100, 100, 100)
                    )
    button.position_on = 'center'

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
        button.draw(screen)
        # update screen
        pygame.display.flip()

    # quit when game loop exited
    pygame.quit()

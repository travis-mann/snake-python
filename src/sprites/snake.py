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
class Snake:
    """
    purpose: player controlled snake object
    """
    def __init__(self, segment_size: int,
                 segment_positions: list,
                 starting_direction: Vector2):
        self.segment_positions = segment_positions
        self.segment_size = segment_size
        self.direction = starting_direction
        self.next_direction = starting_direction  # direction to load on next move
        self.grow = True  # used to queue growth on next move

        # segment images
        self.head = pygame.transform.scale(pygame.image.load('./img/snake1/head.png'),(segment_size, segment_size))
        self.body = pygame.transform.scale(pygame.image.load('./img/snake1/body.png'), (segment_size, segment_size))
        self.l = pygame.transform.scale(pygame.image.load('./img/snake1/l.png'), (segment_size, segment_size))
        self.tail = pygame.transform.scale(pygame.image.load('./img/snake1/tail.png'), (segment_size, segment_size))

        # track self collision
        self.colliding = False

        # track smooth slithering
        self.offset = 0
        self.offset_speed = 0.1


    def draw(self, board) -> None:
        """
        purpose: draw snake on the screen
        """
        # draw each segment
        for idx, segment_position in enumerate(self.segment_positions):
            x_position = int(segment_position.x * self.segment_size)
            y_position = int(segment_position.y * self.segment_size)


            # add smooth slither to head and tail
            if idx == 0:  # head
                x_position += self.direction.x * self.offset * self.segment_size
                y_position += self.direction.y * self.offset * self.segment_size
            elif idx == len(self.segment_positions) - 1:  # tail
                last_segment_position = self.segment_positions[idx - 1] - self.segment_positions[idx]
                x_position += last_segment_position.x * self.offset * self.segment_size
                y_position += last_segment_position.y * self.offset * self.segment_size


            # draw segment
            segment = pygame.Rect(x_position, y_position, self.segment_size, self.segment_size)
            part = self.get_part(idx)
            board.blit(part, segment)

            # telescope neck to connect stationary body to moving head
            if idx == 1:
                x_position += self.direction.x * self.offset * self.segment_size
                y_position += self.direction.y * self.offset * self.segment_size
                segment = pygame.Rect(x_position, y_position, self.segment_size, self.segment_size)
                part = self.get_part(idx)
                board.blit(part, segment)
            # telescope tail to connect stationary body to moving tail
            if idx == len(self.segment_positions) - 2:
                x_position += self.direction.x * self.offset * self.segment_size
                y_position += self.direction.y * self.offset * self.segment_size
                segment = pygame.Rect(x_position, y_position, self.segment_size, self.segment_size)
                part = self.get_part(idx)
                board.blit(part, segment)


    def move(self):
        """
        purpose: move snake between tiles
        """

        # check if movement between tiles is occuring
        # accept new movement if near center of tile
        if self.offset >= 0.3:
            # reset offset
            self.offset = -0.4

            # check for and handle growth
            if self.grow:  # copy all segments
                new_segment_positions = self.segment_positions[:]
                self.grow = False
            else:  # copy all but last segment
                new_segment_positions = self.segment_positions[:-1]

            # insert new front segment based on current direction
            self.direction = self.next_direction  # update current direction
            new_segment_positions.insert(0, new_segment_positions[0] + self.direction)

            # check for collision
            if new_segment_positions[0] in self.segment_positions:
                print(f'new segment positions: {new_segment_positions}')
                self.colliding = True
            else:
                self.colliding = False

            # update segment positions
            self.segment_positions = new_segment_positions

            # prep next move to be a slither
            self.slither = True

        else:
            # increase offset by speed
            self.offset += self.offset_speed

    def get_part(self, idx: int):
        """
        purpose: get proper image to draw for a given segment
        :return part: image for snake part correctly rotated
        """
        # get head
        if idx == 0:
            # rotate image
            if self.direction.x == 1:  # rotate right
                rotated_head = pygame.transform.rotate(self.head, -90)
            elif self.direction.x == -1:  # rotate left
                rotated_head = pygame.transform.rotate(self.head, 90)
            elif self.direction.y == 1:  # rotate down
                rotated_head = pygame.transform.rotate(self.head, 180)
            else:  # vertical
                rotated_head = self.head

            return rotated_head

        # get body
        else:
            # get direction of next segment from current segment
            last_segment_position = self.segment_positions[idx - 1] - self.segment_positions[idx]

            # swap body for tail if last piece
            if idx == len(self.segment_positions) - 1:
                return self.get_rotated_body(last_segment_position, self.tail)
            else:
                # check for L piece
                next_segment_position = self.segment_positions[idx + 1] - self.segment_positions[idx]

                # L piece for right/down
                if (last_segment_position.y == -1 and next_segment_position.x == 1) or (
                        last_segment_position.x == 1 and next_segment_position.y == -1):
                    return pygame.transform.rotate(self.l, 90)
                # L piece for right/up
                elif (last_segment_position.x == 1 and next_segment_position.y == 1) or (
                    last_segment_position.y == 1 and next_segment_position.x == 1):
                    return pygame.transform.rotate(self.l, 0)
                # L piece for left/up
                elif (last_segment_position.y == 1 and next_segment_position.x == -1) or (
                    last_segment_position.x == -1 and next_segment_position.y == 1):
                    return pygame.transform.rotate(self.l, 270)
                # L piece for left/down
                elif (last_segment_position.y == -1 and next_segment_position.x == -1) or (
                        last_segment_position.x == -1 and next_segment_position.y == -1):
                    return pygame.transform.rotate(self.l, 180)

                # body piece
                else:
                    return self.get_rotated_body(last_segment_position, self.body)

    def get_rotated_body(self, last_segment_position, piece):
        """
        purpose: rotate body or tail image based on the last segment position
        :param last_segment_position:
        :param piece: tail or body piece
        :return:
        """
        # rotate image to align with next segment
        if last_segment_position.x == 1:  # rotate right
            rotated_part = pygame.transform.rotate(piece, -90)
        elif last_segment_position.x == -1:  # rotate left
            rotated_part = pygame.transform.rotate(piece, 90)
        elif last_segment_position.y == 1:  # rotate down
            rotated_part = pygame.transform.rotate(piece, 180)
        else:  # vertical
            rotated_part = piece

        # output
        return rotated_part


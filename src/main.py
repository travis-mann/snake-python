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
from random import randint
from pygame import mixer

from src.panels.board import Board
from src.panels.score_panel import ScorePanel
from src.panels.pause_menu import PauseMenu
from src.sprites.snake import Snake
from src.sprites.fruit import Fruit


# --- funcs ---
# N/A


# --- classes ---
class SnakeGame:
    """
    purpose: main high level logic for snake game
    """
    def __init__(self,
                 fruit_count: int,
                 tile_count: int):
        # initialize pygame
        print('starting pygame...')
        pygame.init()
        pygame.mixer.init()

        # create screen
        self.screen = pygame.display.set_mode((600, 675))

        # various panels
        board_length = int(self.screen.get_width() * 0.9)
        border_size = (self.screen.get_width() - board_length) / 2
        # center board under score panel
        self.board = Board(tile_count,
                           size=Vector2(board_length, board_length),
                           position=Vector2(self.screen.get_width()/2,
                                            self.screen.get_height() - border_size))
        self.board.position_on = 'midbottom'  # position based on midbottom of board

        # pause menu
        self.pause_menu = PauseMenu(size=Vector2(self.screen.get_width() * 0.5, self.screen.get_height() * 0.7),
                                    position=Vector2(self.screen.get_rect().center[0], self.screen.get_rect().center[0]),
                                    color=(200, 200, 200))

        # center score panel along the top
        self.score_panel = ScorePanel(size=Vector2(self.screen.get_width(),
                                                   self.screen.get_height() - board_length - border_size * 2),
                                      position=Vector2(0, 0),
                                      color=(0, 50, 0))
        self.score_panel.position_on = 'topleft'

        # main game objects
        self.snake_starting_position = [Vector2(3, self.board.tile_count/2+0.5),
                                        Vector2(2, self.board.tile_count/2+0.5),
                                        Vector2(1, self.board.tile_count/2+0.5)]  # to reset to on loss
        self.snake_starting_direction = Vector2(1, 0)
        self.snake = Snake(self.board.tile_size,
                           self.snake_starting_position,
                           self.snake_starting_direction)
        self.fruits = pygame.sprite.Group()
        # add specified number of fruits
        for i in range(fruit_count):
            self.fruits.add(Fruit(self.board.tile_size * 1.1,
                                  './img/fruit/peach.png'))

        # basic game attributes
        self.paused = False
        self.running = True  # tracks if game should keep running

        # time
        self.loop_delay = 50
        self.update_objects_delay = 20

        # events
        self.update_objects_event = pygame.USEREVENT
        pygame.time.set_timer(self.update_objects_event, self.update_objects_delay)

        # initialize game
        self.init_game()

    def run(self):
        """
        purpose: run main game loop
        """
        # create pygame clock to set game tick
        clock = pygame.time.Clock()

        # play background music loop
        # mixer.music.load('./sound/walking.wav')
        # mixer.music.play(-1)

        # execute continuous game loop
        while self.running:
            # delay between loops so that game doesnt run too fast
            clock.tick(120)

            # draw scene
            self.draw_scene()

            # get input
            self.get_input()

            # respond to events, includes moving snake and checking various conditions
            self.handle_events()

            # check for win
            if not self.fruits:
                self.paused = True
                print('you win!')

        # end game if loop is exited
        print('exiting game...')
        pygame.quit()

    def init_game(self):
        """
        purpose: set game in initial state
        """
        for fruit in self.fruits:
            self.spawn_fruit(fruit)

    def draw_scene(self) -> None:
        """
        purpose: update background and objects based on changes from last loop
        """
        # branch between pause menu and running game
        if self.paused:
            self.pause_menu.draw()
            self.pause_menu.show(self.screen)
            # handle continue
            if self.pause_menu.continue_button.pressed:
                # reset continue button for next click
                self.pause_menu.continue_button.pressed = False
                # cycle game pause state
                self.paused = not self.paused
            # handle quit
            if self.pause_menu.quit_button.pressed:
                # reset quit button for next click
                self.pause_menu.quit_button.pressed = False
                # cycle game pause state
                self.running = False
        else:
            self.draw_scene_running()
            # debug data
            self.show_debug_info()

        # update screen
        pygame.display.update()

    def draw_scene_running(self):
        """
        purpose: draw the scene when the game is running
        """
        # fill background
        self.screen.fill((0, 100, 0))  # color background green

        # draw objects
        self.score_panel.draw()
        self.board.draw()
        self.snake.draw(self.board.surface)
        self.fruits.draw(self.board.surface)
        self.fruits.update(self.board.tile_size)

        # show panels
        self.score_panel.show(self.screen)
        self.board.show(self.screen)

    def get_input(self) -> None:
        """
        purpose: get player input
        """
        # get keys pressed
        keys = pygame.key.get_pressed()

        # update snake direction based on wsad
        if keys[pygame.K_w] and self.snake.direction.y == 0:
            self.snake.next_direction = Vector2(0, -1)
        elif keys[pygame.K_a] and self.snake.direction.x == 0:
            self.snake.next_direction = Vector2(-1, 0)
        elif keys[pygame.K_s] and self.snake.direction.y == 0:
            self.snake.next_direction = Vector2(0, 1)
        elif keys[pygame.K_d] and self.snake.direction.x == 0:
            self.snake.next_direction = Vector2(1, 0)

    def update_objects(self) -> None:
        """
        purpose: update objects on screen
        """
        # game updates
        self.snake.move()
        # eat fruit if snake on fruit
        for fruit in self.fruits:
            if self.snake.segment_positions[0] == fruit.position:
                self.score_panel.score += 1

                # move fruit
                self.spawn_fruit(fruit)

                # queue snake growth on next move
                self.snake.grow = True

        # check for loss
        if any([self.snake.colliding,  # check if snake is self colliding
                # check if snake off board
                self.snake.segment_positions[0].x < 0,
                self.snake.segment_positions[0].y < 0,
                self.snake.segment_positions[0].x > self.board.tile_count - 1,
                self.snake.segment_positions[0].y > self.board.tile_count - 1
                ]):
            print('you lose!')
            # reset snake
            self.snake.segment_positions = self.snake_starting_position
            self.snake.direction = Vector2(1, 0)
            self.snake.next_direction = Vector2(1, 0)
            self.snake.grow = True
            # reset score
            self.score_panel.score = 0
            # pause game
            self.paused = True

    def handle_events(self) -> None:
        """
        purpose: high left logic for responding to events
        """
        # search events for items to respond to
        for event in pygame.event.get():
            # handle game quit
            if event.type == pygame.QUIT:
                print('close button clicked')
                self.running = False  # exit loop

            # move snake slower than once/loop
            if event.type == self.update_objects_event and not self.paused:
                self.update_objects()

            # handle game pause
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused

    def get_open_tiles(self) -> [Vector2]:
        """
        purpose: get a list of vectors for the open tiles
        """
        # find new tile for fruit
        open_tiles = self.board.tiles[:]
        # remove tiles with the snake
        for segment_position in self.snake.segment_positions:
            try:
                open_tiles.remove(segment_position)
            except ValueError:  # tile already removed from open tiles
                pass
        # remove tiles with a fruit
        for fruit in self.fruits:
            try:
                open_tiles.remove(fruit.position)
            except ValueError:  # tile already removed from open tiles
                pass

        return open_tiles

    def spawn_fruit(self, fruit) -> None:
        """
        purpose: place a fruit on a open tile
        """
        open_tiles = self.get_open_tiles()
        open_tile_count = len(open_tiles)
        if open_tile_count >= 1:
            tile_idx = randint(0, open_tile_count - 1)
            fruit.position = open_tiles[tile_idx]
        else:  # no open tiles left, remove fruit
            print('no open tiles left, removing fruit')
            self.fruits.remove(fruit)

    def show_debug_info(self):
        """
        purpose: add stats for debugging
        """
        font_size = 15
        font = pygame.font.Font('freesansbold.ttf', font_size)
        data = {'position': self.snake.segment_positions[0:2],
                'head offset': self.snake.offset,
                'next direction': self.snake.next_direction,
                'tail position': self.snake.segment_positions[-2:],
                'snake colliding?': self.snake.colliding
                }
        idx = 0
        for label, value in data.items():
            text = font.render(f'{label}: {value}', True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.y += idx * font_size
            self.screen.blit(text, text_rect)
            idx += 1


# --- main ---
if __name__ == "__main__":
    SG = SnakeGame(fruit_count=1,
                   tile_count=17)
    SG.run()

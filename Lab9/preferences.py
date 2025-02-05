"""
Author: Prof. Alyssa
Stores values for constant variables.
This is good practice to avoid "magic numbers"

Assignment adapted from HMC CS60


Updated by: Zeke Foster
Date: 12/2/24
Changes:
    -Updated various preference values
    -COLOR_EMPTY is now randomized between three colors
    -COLOR_HEAD and COLOR_BODY are now randomized between six pairs of colors
"""

import pygame
import random

class Preferences:
    pygame.init()

    ##########
    # Timing #
    ##########

    # How frequently to move the snake
    REFRESH_RATE = 2
    # How frequently to add food to the board
    FOOD_ADD_RATE = 40
    # How long to sleep between updates
    SLEEP_TIME = 10

    ##########
    # Sizing #
    ##########

    # Dimensions of the board
    NUM_CELLS_WIDE = 50
    NUM_CELLS_TALL = 30 

    # Size of each cell in pixels
    CELL_SIZE = 20

    # Dimensions of the board in pixels
    GAME_BOARD_WIDTH = NUM_CELLS_WIDE * CELL_SIZE
    GAME_BOARD_HEIGHT = NUM_CELLS_TALL * CELL_SIZE

    ##########
    # Colors #
    ##########
    SNAKE_LIST = [['red2', 'red3'], ['orange2', 'orange3'], ['yellow2', 'yellow3'], ['green2', 'green3'], ['blue2', 'blue3'], ['purple2', 'purple3'], ['pink2', 'pink3']]
    RANDOM_CHOICE = random.choice(SNAKE_LIST)
    SNAKE_LIST.remove(RANDOM_CHOICE)

    COLOR_BACKGROUND = pygame.Color('lavender')
    COLOR_WALL = pygame.Color('gray40')
    COLOR_FOOD = pygame.Color('firebrick')
    COLOR_EMPTY = [pygame.Color('palegreen'), pygame.Color('palegreen1'), pygame.Color('palegreen2')]
    COLOR_HEAD = pygame.Color(RANDOM_CHOICE[1])
    COLOR_BODY = pygame.Color(RANDOM_CHOICE[0])

    ##########################
    # Game over text display #
    ##########################
    
    GAME_OVER_X = GAME_BOARD_HEIGHT / 2
    GAME_OVER_Y = GAME_BOARD_WIDTH / 2
    GAME_OVER_COLOR = pygame.Color('navy')
    GAME_OVER_FONT = pygame.font.SysFont("arial", 120)
    GAME_OVER_TEXT = "Game Over"

    ######################
    # Graphics and Audio #
    ######################

    # Image to display as the head
    HEAD_IMAGE = "trainer.png"
    # Sound to play when eating
    EAT_SOUND = "meow.wav"
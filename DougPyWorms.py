import math
import os
import platform
import random
import sys
import tkinter
from tkinter import messagebox
from tkinter.colorchooser import askcolor

import pygame
from screeninfo import get_monitors

# Initiate pygame and give permission
# to use pygame's functionality
pygame.init()


class worms:
    # Create a display surface object
    # of specific dimension
    # screenWidth, screenHeight = screen.get_size()
    # screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
    screen = pygame.display.set_mode((600, 600), pygame.RESIZABLE)
    # Creating a new clock object to
    # track the amount of time
    clock = pygame.time.Clock()

    # Creating a new rect for first object
    player_rect = pygame.Rect(200, 500, 50, 10)
    # Creating a new rect for second object
    player_rect2 = pygame.Rect(200, 0, 10, 10)

    # Creating variable for gravity
    gravity = 4

    # Creating a boolean variable that
    # we will use to run the while loop
    run = True

    # Creating an infinite loop
    # to run our game
    while run:

        # Setting the framerate to 60fps
        clock.tick(60)

        # Adding gravity in player_rect2
        player_rect2.bottom += gravity

        # Checking if player is colliding
        # with platform or not using the
        # colliderect() method.
        # It will return a boolean value
        collide = pygame.Rect.colliderect(player_rect, player_rect2)

        # If the objects are colliding
        # then changing the y coordinate
        if collide:
            player_rect2.bottom = player_rect.top

        # Drawing player rect
        pygame.draw.rect(screen, (0, 255, 0),
                        player_rect)
        # Drawing player rect2
        pygame.draw.rect(screen, (0, 0, 255),
                        player_rect2)

        # Updating the display surface
        pygame.display.update()

        # Filling the window with white color
        # window.fill((255, 255, 255))

if __name__ == "__main__":
    worms.main()

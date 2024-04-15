import pygame
from enums import GameState
from display import printMe



# Load the background image
background_image = pygame.image.load("graphics/title.tga")


def title_screen(screen):
    width, height = screen.get_size()
    # Draw the background image

    # draw welcome text
    printMe(screen, "Select a game slot to play from!", 40, 160)
    printMe(screen, "(Right-click a slot to erase it)", 40, 170)
    printMe(screen, "Press ESC to stop being entertained", 40, 320)
    printMe(screen, "Credits: Everything by Mike Hommel", 20, 460)
    printMe(screen, "Copyright 2003, by Hamumu Software", 20, 500)


    return GameState.TITLE

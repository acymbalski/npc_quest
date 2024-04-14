import pygame
from enums import GameState



# Load the background image
background_image = pygame.image.load("graphics/title.tga")


def title_screen(screen):
    width, height = screen.get_size()
    # Draw the background image
    screen.blit(background_image, (int(width * 0.025), int(height * 0.05)))

    return GameState.TITLE

import pygame


def printMe(screen, text, x, y, color=pygame.Color("WHITE")):
    font = pygame.font.Font("font/prstartk.ttf", 8)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))

import pygame
from enum import Enum
import title
from enums import GameState


def main():
    # Initialize Pygame
    pygame.init()

    # Set up the window dimensions
    width = 800
    height = 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("NPC Quest R")
    # Set the window icon
    icon_image = pygame.image.load("graphics/fatbird.tga")
    pygame.display.set_icon(icon_image)

    # Set the user's mouse cursor
    cursor_image = pygame.image.load(
        "graphics/cursor.tga"
    ).convert_alpha()  # Convert the cursor image to a surface

    def set_custom_cursor(cursor_surface, hotspot_x, hotspot_y):
        pygame.mouse.set_visible(False)
        cursor_size = cursor_surface.get_size()
        cursor_surface.set_colorkey((255, 0, 255))  # key out pink for transparancy
        cursor_string = pygame.cursors.compile(pygame.surfarray.array2d(cursor_surface))
        cursor_tuple = (
            (cursor_size[0], cursor_size[1]),
            (hotspot_x, hotspot_y),
            cursor_string[0],
            cursor_string[1],
        )
        pygame.mouse.set_cursor(*cursor_tuple)

    set_custom_cursor(cursor_image, hotspot_x=0, hotspot_y=0)

    # Main game loop
    running = True
    game_state = GameState.TITLE

    while running:
        # fill black
        screen.fill((0, 0, 0))

        if game_state == GameState.QUIT:
            running = False

        if game_state == GameState.TITLE:
            game_state = title.title_screen(screen)

        elif game_state == GameState.SHOP:
            pass

        elif game_state == GameState.GAME:
            pass

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw the cursor
        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.blit(cursor_image, (mouse_x, mouse_y))

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()


if __name__ == "__main__":
    main()

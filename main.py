import pygame
import title
from enums import GameState


class Game:
    """Main game class"""

    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up the window dimensions
        width = 800
        height = 600
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("NPC Quest R")
        # Set the window icon
        icon_image = pygame.image.load("graphics/fatbird.tga")
        pygame.display.set_icon(icon_image)

        self.font_8 = pygame.font.Font("font/prstartk.ttf", 8)

        self.title = title.Title(self)

        # Set the user's mouse cursor
        self.cursor_image = pygame.image.load(
            "graphics/cursor.tga"
        ).convert_alpha()  # Convert the cursor image to a surface

        self.set_custom_cursor(self.cursor_image, hotspot_x=0, hotspot_y=0)

        self.game_state = GameState.TITLE

        self.player = None

    def set_custom_cursor(self, cursor_surface, hotspot_x, hotspot_y):
        """Set a custom cursor"""
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

    def run(self):
        """Run the game loop"""

        # Main game loop
        running = True

        while running:
            # fill black
            self.screen.fill((0, 0, 0))

            if self.game_state == GameState.QUIT:
                running = False

            if self.game_state == GameState.TITLE:
                self.title.update()

            elif self.game_state == GameState.SHOP:
                pass

            elif self.game_state == GameState.GAME:
                pass

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Draw the cursor
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.screen.blit(self.cursor_image, (mouse_x, mouse_y))

            # Update the display
            pygame.display.flip()

        # Quit Pygame
        pygame.quit()


def main():
    """Main function"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()

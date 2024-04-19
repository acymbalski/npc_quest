import pygame
import title
from constants import EXIT_CODE, GameState, NOTICE, SFX, STAT, XRES, YRES
from hiscore import load_scores
from map import Map
from monster import monsters
from notice import Notice
from shop import Shop
from sound import makeSound


class Game:
    """Main game class"""

    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up the window dimensions
        width = XRES
        height = YRES
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("NPC Quest R")
        # Set the window icon
        icon_image = pygame.image.load("graphics/fatbird.png")
        pygame.display.set_icon(icon_image)

        self.font_8 = pygame.font.Font("font/prstartk.ttf", 8)

        self.title = title.Title(self)
        self.shop = None
        self.level = None
        self.map = None
        self.notice = None

        self.monster = monsters

        # Set the user's mouse cursor
        self.cursor_image = pygame.image.load(
            "graphics/cursor.tga"
        ).convert_alpha()  # Convert the cursor image to a surface

        self.set_custom_cursor(self.cursor_image, hotspot_x=0, hotspot_y=0)

        self.game_state = GameState.TITLE

        self.exitCode = EXIT_CODE.NONE
        self.noticeType = NOTICE.NONE

        self.hiscores = []
        self.player = None

        # load high scores
        load_scores(self)

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
                if not self.title:
                    self.title = title.Title(self)
                self.title.update()

            elif self.game_state == GameState.SHOP:
                if not self.shop:
                    # creating a shop populates the items
                    self.shop = Shop(self)
                self.shop.update()

            elif self.game_state == GameState.GAME:
                if not self.map:
                    self.map = Map(self)
                self.map.update()

            elif self.game_state == GameState.NOTICE:
                if not self.notice:
                    self.notice = Notice(self)
                self.notice.update()

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

    def levelUp(self):
        while self.player.xp >= self.player.needXP:
            makeSound(SFX.LEVELUP)
            self.player.needXP += self.player.needXP
            self.player.level += 1
            self.noticeType = NOTICE.LEVELUP
            self.game_state = GameState.NOTICE
            topStat = 0
            topSpend = self.player.ptSpend[0]

            for i in range(len(STAT)):
                if self.player.ptSpend[i] > topSpend:
                    topStat = i
                    topSpend = self.player.ptSpend[i]
            self.player.chrClass = topStat + 1


def main():
    """Main function"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()

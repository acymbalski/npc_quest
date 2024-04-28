import configparser
import os
import sys
import time

import pygame
from constants import EXIT_CODE, GameState, NOTICE, SFX, XRES, YRES
from hiscore import load_scores, retrieve_scores
from map import Map
from monster import monsters
from notice import Notice
from shop import Shop
from sound import makeSound
from title import Title
from utilities import makeUpName, resource_path

if getattr(sys, "frozen", False):
    os.chdir(sys._MEIPASS)


class Game:
    """
    Main game class!

    All update logic is found in run(), also all the draw logic even though
    there should be a separate draw() function.

    The state of the game is found in game_state, an enum defined
    in constants.py
    The run() function will call the appropriate sub-update function based
    on the game_state.

    This game object turned out to be super critical. It ends up being passed
    to just about every object in the game that needs to do anything. Global
    variables, game state info, etc. is passed along this way. Is there a better
    way to handle this? Maybe!
    """

    def __init__(self):
        """
        Initialize the game and all appropriate variables.
        It will attempt to read from a config.ini file if one exists, and create
        it if it does not. Window dimensions are defined here but sadly
        not adjustable at this time.
        Leaderboard is defined at a fixed URL, this can be overridden in the
        config.ini file for future-proofing although there are no plans
        for another leaderboard.
        """
        # Initialize Pygame
        pygame.init()

        # Version number. The leaderboard uses this to display appropriate
        # scores. If a significant change is made to the game, this should be
        # incremented. Significant changes include things like new levels,
        # new items, new monsters, or major algorithm changes. Bug fixes
        # don't count. There should probably be a minor version number that
        # does always increment so we can see if there is a new version
        # available for download.
        self.version = "1.0"

        # Load the configuration file, if it exists. Create it if it doesn't
        self.config = configparser.ConfigParser()
        self.score_url = "http://npcquest.hamburger.house:8077"
        # for the leaderboard, give this game a unique name. Users can change
        # this via the config.ini file if they want to use a different name.
        # Leaderboard will auto-highlight scores from this name.
        self.player_name = makeUpName()
        self.upload_scores = True
        self.retrieve_scores = True
        if os.path.exists("config.ini"):
            self.config.read("config.ini")
            score_url = self.config.get("Game", "SCORE_URL", fallback=None)
            if score_url:
                self.score_url = score_url
            self.player_name = self.config.get("Game", "PLAYER_NAME")
            self.upload_scores = (
                self.config.get("Game", "UPLOAD_SCORES", fallback="True").lower()
                == "true"
            )
            self.retrieve_scores = (
                self.config.get("Game", "RETRIEVE_SCORES", fallback="True").lower()
                == "true"
            )
            print(
                f"Loaded config.ini: {self.score_url}, {self.player_name}, {self.upload_scores}, {self.retrieve_scores}"
            )
        else:
            self.config["Game"] = {
                "PLAYER_NAME": self.player_name,
                "UPLOAD_SCORES": "True",
                "RETRIEVE_SCORES": "True",
            }
            with open("config.ini", "w") as configfile:
                self.config.write(configfile)
            print("Created config.ini")

        # Set up the window dimensions
        # This is set via values in constants.py but there's probably no reason
        # for that anymore
        width = XRES
        height = YRES
        self.screen = pygame.display.set_mode((width, height))

        # set window title
        pygame.display.set_caption("NPC Quest R")
        # Set the window icon
        icon_image = pygame.image.load(resource_path("graphics/fatbird.png"))
        pygame.display.set_icon(icon_image)

        # Load the fonts
        self.font_8 = pygame.font.Font(resource_path("font/prstartk.ttf"), 8)

        # These are the game states. Start at the Title
        self.title = Title(self)
        self.shop = None
        self.level = None
        self.map = None
        self.notice = None

        self.monster = monsters

        # Set the user's mouse cursor
        self.cursor_image = pygame.image.load(
            resource_path("graphics/cursor.tga")
        ).convert_alpha()  # Convert the cursor image to a surface

        self.set_custom_cursor(self.cursor_image, hotspot_x=0, hotspot_y=0)

        self.game_state = GameState.TITLE

        self.exitCode = EXIT_CODE.NONE
        self.noticeType = NOTICE.NONE

        # local high scores
        self.hiscores = []
        # global high scores
        self.global_hiscores = []

        # main player
        self.player = None

        # initialize floating text messages. These are used to display small
        # values like damage taken, health gained, etc.
        self.toasts = []

        # load high scores
        load_scores(self)
        self.reload_global_scores()

    def reload_global_scores(self):
        """
        Reload the global high scores. This is called when the game starts and
        when the player uploads a score.
        """
        retrieved_scores = retrieve_scores(self)
        if retrieved_scores:
            # got new scores
            self.global_hiscores = retrieved_scores

    def set_custom_cursor(self, cursor_surface, hotspot_x, hotspot_y):
        """
        Set a custom cursor.
        """
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
        """
        Run the game loop and any sub-update function, as defined by the
        game_state.
        """

        # Main game loop
        running = True

        while running:
            # fill black
            self.screen.fill((0, 0, 0))

            if self.game_state == GameState.QUIT:
                running = False

            if self.game_state == GameState.TITLE:
                if not self.title:
                    self.title = Title(self)
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

            # draw any floating text messages
            for toast in self.toasts:
                toast.update()

            # Update the display
            pygame.display.flip()

        # Quit Pygame
        pygame.quit()

    def levelUp(self):
        """
        Level up the player. This is called when the player has enough XP to
        level up. It will increase the player's level, reset their XP, and
        give them 8 points to spend on attributes.
        Also, shouldn't be in main.py. I think it's here because of some import
        loop that just needed fixing.
        """
        while self.player.xp >= self.player.needXP:
            self.map.get_player_guy().image = None  # trigger image reload
            makeSound(SFX.LEVELUP)
            self.player.needXP += int(self.player.needXP)
            self.player.level += 1
            self.noticeType = NOTICE.LEVELUP
            self.player.ptsLeft = 8
            self.game_state = GameState.NOTICE


def main():
    """
    Main function
    """
    game = Game()
    game.run()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    finally:
        time.sleep(3)

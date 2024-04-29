import pygame
from basics import TextButton
from character import Character
from constants import GameState
from display import printMe
from hiscore import drawHiScores
from utilities import loadGame, resource_path, savegame

# this should be in constants
NUM_SAVES = 10


def findSaveGames(game):
    """
    Find all save games and return them in a list.
    """
    characters = []

    for i in range(NUM_SAVES):
        characters.append(loadGame(i, game))

    return characters


# Load the background image
background_image = pygame.image.load(resource_path("graphics/title.tga"))


class Title:
    """
    Title! The main menu of the game. Basically a list of save games,
    local, and global high scores. Not that much funny business here.
    """

    def __init__(self, game):
        self.game = game
        self.buttons = []

        # load all save games
        characters = findSaveGames(self.game)

        for i in range(NUM_SAVES):
            character = characters[i]
            if character:
                s = f"{i+1: >2}. {character.name}, Lvl {character.level}, Score: {int(character.xp)}"
            else:
                s = f"{i+1: >2}. Unused"

            # is character online eligible?
            color = pygame.Color("WHITE")
            if character and not character.online_eligible:
                color = pygame.Color("GRAY")

            # pop the character in as a button
            self.buttons.append(
                TextButton(
                    self.game,
                    None,
                    40,
                    190 + i * 10,
                    s,
                    color=color,
                )
            )
        # add Exit to Windows button
        self.buttons.append(
            TextButton(
                self.game,
                "Quit",
                40,
                290,
                "Exit To Windows!",
            )
        )
        # inflate button bounding rects to full width
        for button in self.buttons:
            button.setBoundingRectSize(width=268)

    def update(self):
        """
        Update Title. Draw everything.
        """

        screen = self.game.screen

        # Draw the background image
        screen.blit(
            background_image, (10, 40)
        )  # currently matching the original game's offset

        # draw high scores
        drawHiScores(self.game)

        # draw welcome text
        printMe(self.game, "Select a game slot to play from!", 40, 160)
        printMe(self.game, "(Right-click a slot to erase it)", 40, 170)
        printMe(self.game, "Press ESC to stop being entertained", 40, 320)

        printMe(self.game, "Credits: Everything by Mike Hommel", 20, 460)
        printMe(self.game, "Copyright 2003, by Hamumu Software", 20, 500)

        # if we have upload_scores from the config.ini, show the player name
        # discretely in the bottom left
        if self.game.upload_scores:
            printMe(
                self.game,
                f"Your name is: {self.game.player_name}",
                20,
                590,
                color=pygame.Color("GRAY"),
            )

        for button in self.buttons:
            button.draw()

        for event in pygame.event.get():
            # check for escape key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.game_state = GameState.QUIT

            # check for left mouse click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                cursor_pos = pygame.mouse.get_pos()
                for i, button in enumerate(self.buttons):
                    if button.bounding_rect.collidepoint(cursor_pos):
                        # trying to quit?
                        if button.command == "Quit":
                            self.game.game_state = GameState.QUIT
                        else:
                            # otherwise we're loading a game (because there's
                            # no other buttons)

                            # reading this now... Oof. Using this 'i' value
                            # means the order that we added our buttons is
                            # really particular. This will need to be updated.
                            # You can tell Title was the first screen made.
                            character = findSaveGames(self.game)[i]

                            # do we have a character in this slot? Load it
                            if character:
                                active_character = character
                            else:
                                # otherwise make a new character
                                active_character = Character(self.game)
                                active_character.slot = i
                                savegame(active_character)

                            # noice, character loaded. let's head to the shop
                            self.game.game_state = GameState.SHOP
                            self.game.title = None
                            self.game.player = active_character


if __name__ == "__main__":
    import main

    main.main()

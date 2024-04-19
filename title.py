import pygame
from basics import TextButton
from character import Character
from constants import GameState
from display import printMe
from hiscore import drawHiScores
from utilities import loadGame, savegame

NUM_SAVES = 10


def findSaveGames(game):
    characters = []

    for i in range(NUM_SAVES):
        characters.append(loadGame(i, game))

    return characters


# Load the background image
background_image = pygame.image.load("graphics/title.tga")


class Title:

    def __init__(self, game):
        self.game = game
        self.buttons = []

        characters = findSaveGames(self.game)
        # active_character = None
        for i in range(NUM_SAVES):
            character = characters[i]
            if character:
                s = f"{i+1: >2}. {character.name}, Lvl {character.level}, Score: {character.score}"
            else:
                s = f"{i+1: >2}. Unused"

            self.buttons.append(
                TextButton(
                    self.game,
                    None,
                    40,
                    190 + i * 10,
                    s,
                )
            )
        # inflate button bounding rects to full width
        for button in self.buttons:
            button.setBoundingRectSize(width=268)

    def update(self):

        screen = self.game.screen

        # width, height = screen.get_size()
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
        printMe(
            self.game,
            "Exit To Windows!",
            40,
            290,
            draw_bounding_box=True,
            bounding_box_width=268,
        )  # TODO: Click this to quit
        printMe(self.game, "Credits: Everything by Mike Hommel", 20, 460)
        printMe(self.game, "Copyright 2003, by Hamumu Software", 20, 500)

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
                        character = findSaveGames(self.game)[i]
                        if character:
                            active_character = character
                        else:
                            active_character = Character(self.game)
                            active_character.slot = i
                            savegame(active_character)
                        self.game.game_state = GameState.SHOP
                        self.game.title = None
                        self.game.player = active_character


if __name__ == "__main__":
    import main

    main.main()

import pygame
from display import printMe, printMeIsClicked
from character import loadGame
from enums import GameState
from character import Character

NUM_SAVES = 10


def findSaveGames():
    characters = []

    for i in range(NUM_SAVES):
        characters.append(loadGame(i))

    return characters


# Load the background image
background_image = pygame.image.load("graphics/title.tga")


class Title:

    def __init__(self, game):
        self.game = game

    def update(self):

        screen = self.game.screen

        # width, height = screen.get_size()
        # Draw the background image
        screen.blit(
            background_image, (10, 40)
        )  # currently matching the original game's offset

        # draw welcome text
        printMe(screen, "Select a game slot to play from!", 40, 160)
        printMe(screen, "(Right-click a slot to erase it)", 40, 170)
        printMe(screen, "Press ESC to stop being entertained", 40, 320)
        printMe(
            screen,
            "Exit To Windows!",
            40,
            290,
            draw_bounding_box=True,
            bounding_box_width=268,
        )
        printMe(screen, "Credits: Everything by Mike Hommel", 20, 460)
        printMe(screen, "Copyright 2003, by Hamumu Software", 20, 500)

        characters = findSaveGames()
        active_character = None

        for i in range(NUM_SAVES):
            # if cursor == i:
            # pygame.draw.rect(screen, (255, 255, 0), (38, 188 + i * 10, 310, 188 + 10 + i * 10))
            character = characters[i]
            if character:
                s = f"{i+1: >2}. {character.name}, Lvl {character.level}, Score: {character.score}"

            else:
                s = f"{i+1: >2}. Unused"

            # draw bounding box if mouseover
            if printMeIsClicked(
                screen,
                s,
                40,
                190 + i * 10,
                draw_bounding_box=True,
                bounding_box_width=268,
            ):
                if character:
                    active_character = character
                else:
                    active_character = Character()
                self.game.game_state = GameState.GAME
                self.game.player = active_character


if __name__ == "__main__":
    import main

    main.main()

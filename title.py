import pygame
from enums import GameState
from display import printMe
from character import loadGame

NUM_SAVES = 10


def findSaveGames():
    characters = []

    for i in range(NUM_SAVES):
        characters.append(loadGame(i))

    return characters


# Load the background image
background_image = pygame.image.load("graphics/title.tga")


def title_screen(screen):
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

    for i in range(NUM_SAVES):
        # if cursor == i:
        # pygame.draw.rect(screen, (255, 255, 0), (38, 188 + i * 10, 310, 188 + 10 + i * 10))
        character = characters[i]
        if character:
            s = f"{i+1: >2}. {character.name}, Lvl {character.level}, Score: {character.score}"

        else:
            s = f"{i+1: >2}. Unused"

        # draw bounding box if mouseover
        printMe(
            screen, s, 40, 190 + i * 10, draw_bounding_box=True, bounding_box_width=268
        )

    return GameState.TITLE


if __name__ == "__main__":
    import main

    main.main()

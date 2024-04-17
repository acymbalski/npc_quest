import pygame
from enums import GameState, GUYS, STAT, EXIT_CODE
import random
from critter import addGuy
from basics import FIXAMT


class Action:

    def __init__(self, game):
        self.game = game
        self.buttons = []
        self.shouldExit = False
        self.level = self.game.level

        # add guys
        addGuy(GUYS.PLAYER, 0)
        if self.level >= 3:
            j = random.randint(0, self.level + 1)
            if self.level > 4:
                j += self.level * 2
            if self.level == 9:
                j += 10

            for _ in range(j):
                if random.randint(0, 5) == 0:
                    addGuy(GUYS.DOLPHIN, self.level)
                else:
                    addGuy(GUYS.HOTDOG, self.level)
        if self.level >= 2:
            j = random.randint(0, self.level * 2 + 1)
            for i in range(j):
                if random.randint(0, 5) == 0:
                    addGuy(GUYS.REINDEER, self.level)
                else:
                    addGuy(GUYS.BLUEY, self.level)
        else:
            j = 0

        j = 10 - j
        if j < 1:
            j = 1
        j += self.level * 2
        if self.level == 9:
            j *= 5
        for _ in range(j):
            if random.randint(0, 7) == 0 or self.level == 0:
                addGuy(GUYS.GNOME, self.level)
            else:
                addGuy(GUYS.FATBIRD, self.level)

    def update(self):

        screen = self.game.screen

        speed = self.game.player.stat[STAT.SPD]
        if speed < 1:
            speed = 1

        amount = 120 * FIXAMT / speed
        if amount > 120 * FIXAMT:
            amount = 120 * FIXAMT

        amount /= 30
        if amount < 1:
            amount = 1

        while (
            ticksLeft()
        ):  # we can probably ignore this, it is trying to just do a game loop at 60fps
            # updateMap()
            # if lmb is held...
            # updateCombatNums()
            # updateGuys(amount * 8, 8)
            # else:
            # updateCombatNums()
            # updateGuys(amount, 1)
            # if rmb is held...
            self.game.player.shouldExit = True

        # Draw the background image
        # screen.blit(background_image, (0, 0))

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
                for _, button in enumerate(self.buttons):
                    if button.bounding_rect.collidepoint(cursor_pos):
                        pass


def gotKilled(game, how):
    game.player.life = 0
    game.exitCode = EXIT_CODE.DIED + how.value  # TODO: cause of death needs rework
    # TODO: rankEarned = AddHiScore()


if __name__ == "__main__":
    import main

    main.main()

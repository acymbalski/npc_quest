import random

import pygame
from constants import EXIT_CODE, FIXAMT, GameState, GUYS, STAT
from critter import addGuy, updateGuys


class Action:

    def __init__(self, game):
        self.game = game
        self.buttons = []
        self.shouldExit = False
        self.level = self.game.level

        # have to init late due to a wacko circular reference I think
        self.is_initialized = False

    def finishInit(self):
        self.is_initialized = True

        # add guys
        addGuy(self.game, GUYS.PLAYER, 0)
        if self.level.value >= 3:
            j = random.randint(0, self.level.value + 1)
            if self.level.value > 4:
                j += self.level.value * 2
            if self.level.value == 9:
                j += 10

            for _ in range(j):
                if random.randint(0, 5) == 0:
                    addGuy(self.game, GUYS.DOLPHIN, self.level.value)
                else:
                    addGuy(self.game, GUYS.HOTDOG, self.level.value)
        if self.level.value >= 2:
            j = random.randint(0, self.level.value * 2 + 1)
            for i in range(j):
                if random.randint(0, 5) == 0:
                    addGuy(self.game, GUYS.REINDEER, self.level.value)
                else:
                    addGuy(self.game, GUYS.BLUEY, self.level.value)
        else:
            j = 0

        j = 10 - j
        if j < 1:
            j = 1
        j += self.level.value * 2
        if self.level.value == 9:
            j *= 5
        for _ in range(j):
            if random.randint(0, 7) == 0 or self.level.value == 0:
                addGuy(self.game, GUYS.GNOME, self.level.value)
            else:
                addGuy(self.game, GUYS.FATBIRD, self.level.value)

    def update(self):

        if not self.is_initialized:
            self.finishInit()

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

        # while (
        #     ticksLeft()
        # ):  # we can probably ignore this, it is trying to just do a game loop at 60fps
        # self.game.map.updateMap()
        # if lmb is held...
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
            # updateCombatNums()
            updateGuys(self.game, amount * 8, 8)
        # else:
        else:
            # updateCombatNums()
            updateGuys(self.game, amount, 1)
        # if rmb is held...
        # self.game.player.shouldExit = True

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    cursor_pos = pygame.mouse.get_pos()
                    for _, button in enumerate(self.buttons):
                        if button.bounding_rect.collidepoint(cursor_pos):
                            pass
                if event.button == 3:
                    self.game.player.shouldExit = True


if __name__ == "__main__":
    import main

    main.main()

import random

import pygame
from constants import FIXAMT, GameState, GUYS, MAX_GUYS, STAT
from critter import addGuy, updateGuys


class Action:

    def __init__(self, game):
        self.game = game
        self.level = self.game.level

        # have to init late due to a wacko circular reference I think
        self.is_initialized = False

        self.game.player.shouldExit = False

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

        speed = self.game.player.stat[STAT.SPD]
        if speed < 1:
            speed = 1

        amount = 120 * FIXAMT / speed
        if amount > 120 * FIXAMT:
            amount = 120 * FIXAMT

        amount /= 30
        if amount < 1:
            amount = 1

        # remove dead guys
        for i in range(MAX_GUYS):
            guy = self.game.map.guys[i]
            if guy:
                if guy.type == GUYS.NONE:
                    self.game.map.guys[i] = None
            else:
                continue

        # if lmb is held...
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
            # run at 8x speed
            updateGuys(self.game, amount * 8, 8)
        else:
            # otherwise actually run at 1/4x speed because 1x speed is
            # way too fast in this engine
            updateGuys(self.game, amount / 4, 1)


if __name__ == "__main__":
    import main

    main.main()

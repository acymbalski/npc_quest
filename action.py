import random

import pygame
from constants import FIXAMT, GUYS, MAX_GUYS, STAT
from critter import addGuy, updateGuys


class Action:
    """
    Action is not responsible for a whole lot anymore. It needs to be absorbed
    elsewhere, probably into Map, which is the only place it gets used.
    Action adds bad guys to the map and handles the logic that tells them to
    update. It doesn't do the updating, just handles the game speed.
    """

    def __init__(self, game):
        """
        Initialize the Action object with a reference to the game object.
        """
        self.game = game
        self.level = self.game.level

        # have to init late due to a wacko circular reference I think
        self.is_initialized = False

        self.game.player.shouldExit = False

    def finishInit(self):
        """
        Finish initializing the Action object. This is called after the game
        object has been fully initialized, because the Action object needs to
        reference the game object to add bad guys to the map.
        """
        self.is_initialized = True

        # add guys

        # add the player
        addGuy(self.game, GUYS.PLAYER, 0)

        # add number of bad guys based on level
        if self.level.value >= 3:
            j = random.randint(0, self.level.value + 1)
            if self.level.value > 4:
                j += self.level.value * 2
            if self.level.value == 9:
                j += 10

            for _ in range(j):
                # 20% dolphins, 80% hotdogs
                if random.randint(0, 5) == 0:
                    addGuy(self.game, GUYS.DOLPHIN, self.level.value)
                else:
                    addGuy(self.game, GUYS.HOTDOG, self.level.value)
        if self.level.value >= 2:
            j = random.randint(0, self.level.value * 2 + 1)
            for _ in range(j):
                if random.randint(0, 5) == 0:
                    # 20% reindeer, 80% blueys
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
            # always add some fatbirds and gnomes
            if random.randint(0, 7) == 0 or self.level.value == 0:
                addGuy(self.game, GUYS.GNOME, self.level.value)
            else:
                addGuy(self.game, GUYS.FATBIRD, self.level.value)

    def update(self):
        """
        Update the Action object. This is called every frame by the Map object.
        It updates the bad guys on the map.
        """

        if not self.is_initialized:
            self.finishInit()

        # When the character's speed is high, monsters update less frequently
        speed = self.game.player.stat[STAT.SPD]
        if speed < 1:
            speed = 1

        amount = 120 * FIXAMT / speed
        if amount > 120 * FIXAMT:
            amount = 120 * FIXAMT

        amount /= 30
        # But bad guys never freeze solid!
        if amount < 1:
            amount = 1

        # remove dead guys
        # this is a quirk of how the original code was written and
        # then re-written. I think guys are simply "marked" as dead when killed
        # and need to be explicitly removed here. I think it was an issue with
        # targeting a guy that was already dead or something.
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

import random

import pygame
from action import Action
from character import renderCharacterData
from constants import (
    EXIT_CODE,
    GameState,
    GUYS,
    LEVEL,
    MAP_HEIGHT,
    MAP_WIDTH,
    MAP_X,
    MAX_GUYS,
    NOTICE,
    offX,
    offY,
    TILE_HEIGHT,
    TILE_TYPE,
    TILE_WIDTH,
    XRES,
    YRES,
)
from utilities import resource_path, savegame


def getTileImage(tile):
    """
    Get the image for a tile based on its type and level.
    Not a fan of this, but it's not the worst thing in the world.

    Tile images are on a spritesheet. This function gets the right part of the
    spritesheet based on the tile's type and level.
    """
    tiles = pygame.image.load(resource_path("graphics/tiles.tga"))

    l = tile.level.value
    if l > 9:
        l = 10

    tile_rect = pygame.Rect(
        tile.type.value * TILE_WIDTH, l * 16, TILE_WIDTH, TILE_HEIGHT
    )
    tile_surface = pygame.Surface((16, 16))
    tile_surface.blit(tiles, (0, 0), tile_rect)
    tile_surface.set_colorkey((255, 0, 255))  # key out pink for transparancy
    return tile_surface


class Tile:
    """
    A Tile. The map is made of them!
    Tiles have a couple special properties besides their icon,
    which pathfinding depends on.
    """

    def __init__(
        self,
        level=LEVEL.GNOMEY_PLAINS,
        tile_type=TILE_TYPE.FLOOR,
        critter=0,
        monsNum=0,
        code=0,
    ):
        # tile type - floor, wall, door
        self._type = tile_type

        # critter... I don't think this is actually used
        self.critter = critter

        # monsNum is used for pathfinding. Basically a tile with a monster on it
        # gets its monsNum set to a high value (200). Tiles around it are set to
        # slowly decrementing values. So as your monsNum gets higher, you are in
        # closer proximity to a monster
        self.monsNum = monsNum

        # code is like monsNum except for Doors
        # and it gets set to 2000 instead of 200
        # higher code = closer to a door
        # it also gets used for the map generator to determine if the map is
        # "done" before we start adding doors
        self.code = code

        # level is used to determine the tile's image
        self.level = level
        self.image = getTileImage(self)

    @property
    def type(self):
        """
        Get the tile's type.
        Overridden because I overrode the setter.
        """
        return self._type

    @type.setter
    def type(self, tile_type):
        """
        Set the tile's type. I did this to update the image as appropriate,
        since the map generator sets types directly.
        It would be smarter to load the images later, once the map is generated,
        but I didn't do that.
        """
        if tile_type in TILE_TYPE:
            self._type = tile_type
            self.image = getTileImage(self)
        else:
            raise ValueError("Invalid tile type")


# Load the background image
# shouldn't be here :/
background_image = pygame.image.load(resource_path("graphics/charsheet.tga"))


class Map:
    """
    The Map!
    The map is made of tiles. The map is responsible for generating itself,
    drawing itself, and updating itself.
    """

    def __init__(self, game):
        """
        Initialize the map.
        """
        self.game = game

        # I had this big idea for buttons and screens and how they would get
        # inherited and used but I didn't really get all the way with that
        # so this is just a list of buttons. I don't think we ever use it here.
        self.buttons = []

        # the map is a 1D array!
        self.map = []  # size MAP_WIDTH * MAP_HEIGHT
        for _ in range(int(MAP_WIDTH * MAP_HEIGHT)):
            self.map.append(Tile())

        # all Guys on the map
        self.guys = [None] * MAX_GUYS  # list 128 long, yikes

        # reset player's berserk status
        self.game.player.goneBerserk = False
        # yikes
        self.game.player.haveSaidFood = False
        self.game.exitCode = EXIT_CODE.NONE

        self.victory = False
        self.action = Action(self.game)

        # now, generate the map
        self.genMap()

    def genMap(self):
        """
        Generate the map!

        First, fill the map with walls.
        Then add a few rooms - between 2 and 8.
        Then make tunnels until the map is "done."
        Then add doors.

        The original code drew the map while it generated. I tried that here
        (you can see the draw_map() commands)
        but it doesn't really work. But it's "so fast" that it doesn't matter.
        """

        for i in range(int(MAP_WIDTH * MAP_HEIGHT)):
            self.map[i] = Tile(level=self.game.level, tile_type=TILE_TYPE.WALL)
            self.map[i].code = i

        j = 2 + random.randint(0, 6)
        for i in range(j):
            self.draw_map()
            self.addRoom()

        while not self.mapIsDone():
            self.draw_map()
            self.makeTunnel()

        self.placeDoors()

    def levelEmpty(self):
        """
        Is the level empty of enemies?
        """
        for i in range(MAX_GUYS):
            if self.guys[i] is not None:
                if self.guys[i].type != GUYS.PLAYER:
                    return False

        return True

    def addRoom(self):
        """
        Add a room (of floor tiles).
        Width/height are random between 2 and 16.
        """
        x = random.randint(0, MAP_WIDTH - 2) + 1
        y = random.randint(0, MAP_HEIGHT - 2) + 1
        w = random.randint(0, 14) + 2
        h = random.randint(0, 14) + 2

        for i in range(w):
            for j in range(h):
                # if it fits, I sits
                if (
                    x + i > 0
                    and x + i < MAP_WIDTH - 1
                    and y + j > 0
                    and y + j < MAP_HEIGHT - 1
                ):
                    self.map[x + i + (y + j) * MAP_WIDTH].type = TILE_TYPE.FLOOR
                    self.map[x + i + (y + j) * MAP_WIDTH].code = self.map[
                        x + y * MAP_WIDTH
                    ].code  # make the whole room one code (???)

    def mapIsDone(self):
        """
        Is the map done?
        This is a direct translation of the original.
        If all the floor tiles have the same code, the map is done.
        Code gets updated after this in placeDoor()
        """
        fCode = -1
        for i in range(MAP_WIDTH * MAP_HEIGHT):
            if self.map[i].type == TILE_TYPE.FLOOR:
                if fCode == -1:
                    fCode = self.map[i].code
                elif fCode != self.map[i].code:
                    return False
        return True

    def makeTunnel(self):
        """
        Make a tunnel from here to there.
        Find a room, then dig a tunnel to another room.
        """
        x = random.randint(0, MAP_WIDTH - 2) + 1
        y = random.randint(0, MAP_HEIGHT - 2) + 1
        while self.map[x + y * MAP_WIDTH].type != TILE_TYPE.FLOOR:
            x = random.randint(0, MAP_WIDTH - 2) + 1
            y = random.randint(0, MAP_HEIGHT - 2) + 1

        # now we have a floor
        a = random.randint(0, 3)
        startA = a
        while True:
            # if we hit the edge of the map or...?, wander differently
            if (
                x + offX[a] < 1
                or y + offY[a] < 1
                or x + offX[a] >= MAP_WIDTH - 1
                or y + offY[a] >= MAP_HEIGHT - 1
                or self.map[(x + offX[a]) + (y + offY[a]) * MAP_WIDTH].code
                == self.map[x + y * MAP_WIDTH].code
            ):
                a = (a + 1) % 4
                if a == startA:
                    break
                continue
            # dig!
            self.digTunnel(
                x + offX[a], y + offY[a], self.map[x + y * MAP_WIDTH].code, a
            )
            return

    def digTunnel(self, x, y, code, a):
        """
        Actually dig the tunnel.

        This is a direct translation of the original.
        This function is recursive. In the original code it was sort of
        left unchecked. I don't think it could have literally gone "forever,"
        there's only so many tiles to wander to, but Python really didn't like
        it. After four or so levels of recursion it would throw an error
        and crash. Sneakily, it wouldn't happen every time.
        """
        a = random.randint(0, 3)
        if self.map[x + y * MAP_WIDTH].type != TILE_TYPE.FLOOR:
            self.map[x + y * MAP_WIDTH].type = TILE_TYPE.FLOOR
            self.map[x + y * MAP_WIDTH].code = code

            startA = a
            tries = 0
            while True:
                if (
                    x + offX[a] < 1
                    or y + offY[a] < 1
                    or x + offX[a] >= MAP_WIDTH - 1
                    or y + offY[a] >= MAP_HEIGHT - 1
                    or self.map[(x + offX[a]) + (y + offY[a]) * MAP_WIDTH].code == code
                ):
                    a = random.randint(0, 3)
                    if tries + 1 == 10:
                        return  # got stuck
                    tries += 1
                    continue
                self.digTunnel(x + offX[a], y + offY[a], code, a)
                return
        else:
            if self.map[x + y * MAP_WIDTH].code != code:
                try:
                    self.floodFillCode(x, y, code)
                except Exception:  # can fail on some dumb recursion thing
                    return
                return
            else:
                return  # hit your own code, give up

    def floodFillCode(self, x, y, code):
        """
        Flood fill a code.
        """
        self.map[x + y * MAP_WIDTH].code = code

        for a in range(4):
            if (
                self.map[x + offX[a] + (y + offY[a]) * MAP_WIDTH].type
                == TILE_TYPE.FLOOR
                and self.map[x + offX[a] + (y + offY[a]) * MAP_WIDTH].code != code
            ):
                self.floodFillCode(x + offX[a], y + offY[a], code)

    def placeDoors(self):
        """
        Place 1-4 doors and set the tile's code appropriately.
        """
        a = random.randint(0, 3) + 1

        while a > 0:
            x = random.randint(0, MAP_WIDTH - 2) + 1
            y = random.randint(0, MAP_HEIGHT - 2) + 1

            while self.map[x + y * MAP_WIDTH].type != TILE_TYPE.FLOOR:
                x = random.randint(0, MAP_WIDTH - 2) + 1
                y = random.randint(0, MAP_HEIGHT - 2) + 1

            self.map[x + y * MAP_WIDTH].type = TILE_TYPE.DOOR
            a -= 1

        for i in range(MAP_WIDTH * MAP_HEIGHT):
            if self.map[i].type == TILE_TYPE.DOOR:
                self.map[i].code = 2000  # what?
            else:
                self.map[i].code = 0

    def spreadToNeighbors(self, x, y, code):
        """
        Spread the code value to neighbors for door pathfinding.
        """
        for a in range(4):
            if (
                x + offX[a] < 1
                or y + offY[a] < 1
                or x + offX[a] >= MAP_WIDTH - 1
                or y + offY[a] >= MAP_HEIGHT - 1
                or self.map[(x + offX[a]) + (y + offY[a]) * MAP_WIDTH].type
                != TILE_TYPE.FLOOR
            ):
                continue
            if self.map[(x + offX[a]) + (y + offY[a]) * MAP_WIDTH].code < code - 1:
                self.map[(x + offX[a]) + (y + offY[a]) * MAP_WIDTH].code = code - 1

    def spreadToNeighbors2(self, x, y, code):
        """
        Spread the monsNum value to neighbors for monster pathfinding.
        """
        for a in range(4):
            if (
                x + offX[a] < 1
                or y + offY[a] < 1
                or x + offX[a] >= MAP_WIDTH - 1
                or y + offY[a] >= MAP_HEIGHT - 1
                or (
                    self.map[(x + offX[a]) + (y + offY[a]) * MAP_WIDTH].type
                    != TILE_TYPE.FLOOR
                    and self.map[(x + offX[a]) + (y + offY[a]) * MAP_WIDTH].type
                    != TILE_TYPE.DOOR
                )
            ):
                continue
            if self.map[(x + offX[a]) + (y + offY[a]) * MAP_WIDTH].monsNum < code - 1:
                self.map[(x + offX[a]) + (y + offY[a]) * MAP_WIDTH].monsNum = code - 1

    def stinkUpTheMap(self):
        """
        Stink it up.
        i.e. Set the monsNum value of any Tile with a monster on it to 200.
        For pathfinding!
        """
        for i in range(MAX_GUYS):
            if self.guys:
                if self.guys[i] is not None:
                    if self.guys[i].type != GUYS.PLAYER:
                        self.map[
                            self.guys[i].x + self.guys[i].y * MAP_WIDTH
                        ].monsNum = 200

    def updateMap(self):  # yep this one is different!
        """
        Update the map's monsNum and code values for pathfinding.
        """
        self.stinkUpTheMap()

        for i in range(MAP_WIDTH * MAP_HEIGHT):
            if self.map[i].code > 0:
                self.spreadToNeighbors(
                    i % MAP_WIDTH, int(i / MAP_WIDTH), self.map[i].code
                )
            if self.map[i].monsNum > 0:
                self.map[i].monsNum -= 1
                self.spreadToNeighbors2(
                    i % MAP_WIDTH, int(i / MAP_WIDTH), self.map[i].monsNum
                )

    def draw_map(self):
        """
        Draw the map.
        """
        screen = self.game.screen

        # Draw the background image
        screen.blit(background_image, (0, 0))
        # draw the character data
        renderCharacterData(self.game)

        # update code/monsNum values for pathfinding
        # we do this a lot!
        self.updateMap()

        # draw all tiles
        x = MAP_X
        y = 0
        for j in range(MAP_HEIGHT):
            for i in range(MAP_WIDTH):
                screen.blit(self.map[i + j * MAP_WIDTH].image, (x, y))
                x += TILE_WIDTH
            x = MAP_X
            y += TILE_HEIGHT

        pygame.draw.rect(
            screen, (0, 0, 0), (MAP_X, TILE_HEIGHT * MAP_HEIGHT, XRES - 1, YRES - 1)
        )

        # draw all the Guys
        self.drawGuys()

        # draw the buttons, which we don't have
        for button in self.buttons:
            button.draw()

    def update(self):
        """
        The main update loop. Not like that other one, updateMap
        """

        # don't draw if we're in a level-up screen
        if self.game.game_state == GameState.NOTICE:
            return

        # update Action
        self.action.update()
        self.draw_map()

        for event in pygame.event.get():
            # check for escape key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.game_state = GameState.QUIT

            # check for right mouse click
            # if the player clicks the right mouse button, tell the player
            # to exit the map
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    self.game.player.shouldExit = True

        # if player died or exited the map, go back to shop
        if self.game.exitCode == EXIT_CODE.ESCAPED:
            # we made it out, save game
            savegame(self.game.player)
            self.game.game_state = GameState.SHOP
            self.game.map = None
        elif self.game.exitCode == EXIT_CODE.DIED:
            # oop, we died
            self.game.noticeType = NOTICE.MURDERED
            self.game.game_state = GameState.NOTICE
            self.game.map = None
        elif self.game.exitCode == EXIT_CODE.STARVED:
            # oop, we starved
            self.game.noticeType = NOTICE.STARVED
            self.game.game_state = GameState.NOTICE
            self.game.map = None

    def drawGuys(self):
        """
        Draw all the Guys.
        """
        for i in range(MAX_GUYS):
            if self.guys[i] is not None:
                # draw guy
                self.guys[i].draw()

    def get_player_guy(self):
        """
        Get the Guy of the player.
        """
        for i in range(MAX_GUYS):
            if self.guys[i] is not None:
                if self.guys[i].type == GUYS.PLAYER:
                    return self.guys[i]
        return None


if __name__ == "__main__":
    import main

    main.main()

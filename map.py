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
    def __init__(
        self,
        level=LEVEL.GNOMEY_PLAINS,
        tile_type=TILE_TYPE.FLOOR,
        critter=0,
        monsNum=0,
        code=0,
    ):
        self._type = tile_type
        self.critter = critter
        self.monsNum = monsNum
        self.code = code
        self.level = level
        self.image = getTileImage(self)

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, tile_type):
        if tile_type in TILE_TYPE:
            self._type = tile_type
            self.image = getTileImage(self)
        else:
            raise ValueError("Invalid tile type")


background_image = pygame.image.load(resource_path("graphics/charsheet.tga"))


class Map:

    def __init__(self, game):
        self.game = game
        self.buttons = []

        self.map = []  # size MAP_WIDTH * MAP_HEIGHT
        for i in range(int(MAP_WIDTH * MAP_HEIGHT)):
            self.map.append(Tile())
        self.genMap()

        self.guys = [None] * MAX_GUYS  # list 128 long, yikes

        # reset player's berserk status
        self.game.player.goneBerserk = False
        # yikes
        self.game.player.haveSaidFood = False
        self.game.exitCode = EXIT_CODE.NONE

        self.action = Action(self.game)

    def genMap(self):

        for i in range(int(MAP_WIDTH * MAP_HEIGHT)):
            self.map[i] = Tile(level=self.game.level, tile_type=TILE_TYPE.WALL)
            self.map[i].code = i

        j = 2 + random.randint(0, 6)
        for i in range(j):
            # RenderMap(level)
            # SwapPages()
            self.addRoom()

        while not self.mapIsDone():
            # RenderMap(level)
            # SwapPages()
            self.makeTunnel()

        self.placeDoors()

    def levelEmpty(self):
        for i in range(MAX_GUYS):
            if self.guys[i] is not None:
                if self.guys[i].type != GUYS.PLAYER:
                    return False

        return True

    def addRoom(self):
        x = random.randint(0, MAP_WIDTH - 2) + 1
        y = random.randint(0, MAP_HEIGHT - 2) + 1
        w = random.randint(0, 14) + 2
        h = random.randint(0, 14) + 2

        for i in range(w):
            for j in range(h):
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
        fCode = -1
        for i in range(MAP_WIDTH * MAP_HEIGHT):
            if self.map[i].type == TILE_TYPE.FLOOR:
                if fCode == -1:
                    fCode = self.map[i].code
                elif fCode != self.map[i].code:
                    return False
        return True

    def makeTunnel(self):
        x = random.randint(0, MAP_WIDTH - 2) + 1
        y = random.randint(0, MAP_HEIGHT - 2) + 1
        while self.map[x + y * MAP_WIDTH].type != TILE_TYPE.FLOOR:
            x = random.randint(0, MAP_WIDTH - 2) + 1
            y = random.randint(0, MAP_HEIGHT - 2) + 1

        # now we have a floor
        a = random.randint(0, 3)
        startA = a
        while True:
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
            self.digTunnel(
                x + offX[a], y + offY[a], self.map[x + y * MAP_WIDTH].code, a
            )
            return

    def digTunnel(self, x, y, code, a):
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
                self.floodFillCode(x, y, code)
                return
            else:
                return  # hit your own code, give up

    def floodFillCode(self, x, y, code):
        self.map[x + y * MAP_WIDTH].code = code

        for a in range(4):
            if (
                self.map[x + offX[a] + (y + offY[a]) * MAP_WIDTH].type
                == TILE_TYPE.FLOOR
                and self.map[x + offX[a] + (y + offY[a]) * MAP_WIDTH].code != code
            ):
                self.floodFillCode(x + offX[a], y + offY[a], code)

    def placeDoors(self):
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
        for i in range(MAX_GUYS):
            if self.guys[i] is not None:
                if self.guys[i].type != GUYS.PLAYER:
                    self.map[self.guys[i].x + self.guys[i].y * MAP_WIDTH].monsNum = 200

    def updateMap(self):  # yep this one is different!
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

    def update(self):

        # don't draw if we're in a level-up screen
        if self.game.game_state == GameState.NOTICE:
            return
        screen = self.game.screen

        # Draw the background image
        screen.blit(background_image, (0, 0))
        renderCharacterData(self.game)
        self.updateMap()

        self.action.update()
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

        self.drawGuys()

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

        # if player died or exited the map, go back to shop
        if self.game.exitCode == EXIT_CODE.ESCAPED:
            # we made it out, save game
            savegame(self.game.player)
            self.game.game_state = GameState.SHOP
            print("MAP = NONE")
            self.game.map = None
        elif self.game.exitCode == EXIT_CODE.DIED:
            self.game.noticeType = NOTICE.MURDERED
            self.game.game_state = GameState.NOTICE
            print("MAP = NONE")
            self.game.map = None
        elif self.game.exitCode == EXIT_CODE.STARVED:
            self.game.noticeType = NOTICE.STARVED
            self.game.game_state = GameState.NOTICE
            print("MAP = NONE")
            self.game.map = None

    def drawGuys(self):
        for i in range(MAX_GUYS):
            if self.guys[i] is not None:
                # draw guy
                self.guys[i].draw()

    def get_player_guy(self):
        for i in range(MAX_GUYS):
            if self.guys[i] is not None:
                if self.guys[i].type == GUYS.PLAYER:
                    return self.guys[i]
        return None


if __name__ == "__main__":
    import main

    main.main()

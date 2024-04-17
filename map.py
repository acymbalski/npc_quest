from enums import LEVEL, GameState, TILE_TYPE
import pygame
import random

LEVELS = {
    LEVEL.GNOMEY_PLAINS: "Gnomey Plains",
    LEVEL.FLOOFY_WOODS: "Floofy Woods",
    LEVEL.THE_ISLE_OF_TERROR: "The Isle Of Terror",
    LEVEL.ROCKY_DIRTVILLE: "Rocky Dirtville",
    LEVEL.LAVALAVA_HOT_SPRINGS: "Lavalava Hot Springs",
    LEVEL.THE_TEMPLE_OF_SPOON: "The Temple Of Spoon",
    LEVEL.FROSTY_HILL: "Frosty Hill",
    LEVEL.DEADLY_DUNGEON: "Deadly Dungeon",
    LEVEL.A_WEIRD_PLACE: "A Weird Place",
    LEVEL.THE_EVILNESS_PIT: "The Evilness Pit",
    LEVEL.SHIFT_Q: "Shift Q",
}


class Tile:
    def __init__(self, tile_type=0, critter=0, monsNum=0, code=0):
        self.type = tile_type
        self.critter = critter
        self.monsNum = monsNum
        self.code = code

    def draw(self):
        pass


TILE_WIDTH = 16
TILE_HEIGHT = 16

MAP_X = 800 - 576  # 800 is technically supposed to be the screen width
MAP_WIDTH = 576 / TILE_WIDTH
MAP_HEIGHT = 600 / TILE_HEIGHT  # 600 is technically supposed to be the screen height

offX = [1, 0, -1, 0]
offY = [0, 1, 0, -1]


class Map:

    def __init__(self, game):
        self.game = game
        self.buttons = []

        self.map = []  # size MAP_WIDTH * MAP_HEIGHT
        for i in range(MAP_WIDTH * MAP_HEIGHT):
            self.map.append(Tile())
        self.genMap()

    def genMap(self):

        for i in range(MAP_WIDTH * MAP_HEIGHT):
            self.map[i] = Tile(tile_type=TILE_TYPE.WALL)
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
        a = random.randint(0, 4)
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
        a = random.randint(0, 4)
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
                    a = random.randint(0, 4)
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
        a = random.randint(0, 4) + 1

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

    def update(self):

        screen = self.game.screen

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

from enums import GUYS, PLAN, SFX, TILE_TYPE, STAT
from character import CLASS, eatFood
from sound import makeSound
import random
from map import MAP_WIDTH, MAP_HEIGHT
from basics import FIXAMT


def initGuys():
    pass


MAX_GUYS = 128


class Guy:
    def __init__(
        self,
        type=None,
        x=0,
        y=0,
        life=1,
        guy_reload=0,
        plan=PLAN.WANDER,
        planTime=2,
        moves=0,
        foodClock=0,
        level=0,
    ):
        self.type = type
        self.x = x
        self.y = y
        self.life = life
        self.reload = guy_reload
        self.plan = plan
        self.planTime = planTime
        self.moves = moves
        self.foodClock = foodClock
        self.level = level


def addGuy(game, guy_type):
    for i in range(MAX_GUYS):
        if game.map.guys[i] is None:
            guy = Guy()
            guy.type = guy_type
            guy.x, guy.y = findReallyEmptySpot(game)
            guy.life = game.monster[guy_type.value].maxLife * (1 + game.level * 3)
            guy.level = (game.level * 5) + 1
            if guy_type == GUYS.PLAYER:
                makeSound(SFX.HUZZAH)

            game.map.guys[i] = guy
            return


def findReallyEmptySpot(game):
    x = random.randint(0, MAP_WIDTH - 2) + 1
    y = random.randint(0, MAP_HEIGHT - 2) + 1

    while game.map.map[x + y * MAP_WIDTH].type != TILE_TYPE.FLOOR:
        x = random.randint(0, MAP_WIDTH - 2) + 1
        y = random.randint(0, MAP_HEIGHT - 2) + 1

        if game.map.map[x + y * MAP_WIDTH].type == TILE_TYPE.FLOOR:
            for i in range(MAX_GUYS):
                if game.map.guys[i] is not None:
                    if game.map.guys[i].x == x and game.map.guys[i].y == y:
                        continue
    return x, y


def updateGuys(game, timePassed, food):
    for i in range(MAX_GUYS):
        guy = game.map.guys[i]
        if guy:
            if guy.type == GUYS.PLAYER:
                guy.foodClock += food
                if guy.foodClock > 120:
                    guy.foodClock -= 120
                    eatFood()
                amount = game.player.stat[STAT.SPD]
                if amount < 1:
                    amount = 1
                guy.moves += amount * timePassed
            else:
                guy.moves += (
                    game.monsters[guy.type.value].speed * guy.level * timePassed
                )

            if (
                guy.type == GUYS.PLAYER
                and game.player.chrClass == CLASS.WARRIOR
                and game.player.life <= (game.player.stat[STAT.LIF] / 4)
            ):
                guy.moves += amount * timePassed  # double speed when berserk!

            while guy.moves >= 120 * FIXAMT:
                if guy.type == GUYS.PLAYER:
                    updatePlayer(game)
                else:
                    updateGuy(guy)
                guy.moves -= 120 * FIXAMT
                if game.player.life == 0:
                    break
        if game.player.life == 0:
            break


def updatePlayer(game):
    pass


def updateGuy(guy):
    pass

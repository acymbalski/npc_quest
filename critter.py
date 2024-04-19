import random

import pygame

from character import CLASS, eatFood
from combat import gotKilled, monsterAttack, moveMe, playerAttack
from constants import (
    berserkerGfx,
    DEATH_CAUSE,
    EXIT_CODE,
    FIXAMT,
    get_map_xy,
    GUYS,
    MAP_HEIGHT,
    MAP_WIDTH,
    MAP_X,
    MAX_GUYS,
    MONSTER_GFX,
    offX,
    offY,
    PLAN,
    PLAYER_GFX,
    SFX,
    STAT,
    TILE_HEIGHT,
    TILE_TYPE,
    TILE_WIDTH,
)
from display import printMe
from sound import makeSound
from toast import Toast


def initGuys():
    pass


class Guy:
    def __init__(
        self,
        game,
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
        self.game = game
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
        self.image = None

        self.sprite_offset_x = 0
        self.sprite_offset_y = 0

        # hate this
        self.berserkImage = None

    def __str__(self):
        return f"Guy-> type: {self.type}, x: {self.x}, y: {self.y}, life: {self.life}, reload: {self.reload}, plan: {self.plan}, planTime: {self.planTime}, moves: {self.moves}, foodClock: {self.foodClock}, level: {self.level}"

    def load_image(self):
        if self.type == GUYS.PLAYER:
            self.image = pygame.image.load(
                PLAYER_GFX[self.game.player.chrClass]
            ).convert_alpha()
            self.sprite_offset_x = -9
            self.sprite_offset_y = -22
            self.berserkImage = pygame.image.load(berserkerGfx).convert_alpha()
            self.berserkImage.set_colorkey((255, 0, 255))
        else:
            self.image = pygame.image.load(MONSTER_GFX[self.type]).convert_alpha()

            # aaaaahhhhh!
            if self.type in [GUYS.GNOME, GUYS.FATBIRD, GUYS.REINDEER, GUYS.BLUEY]:
                self.sprite_offset_x = -9
                self.sprite_offset_y = -22
            elif self.type in [GUYS.DOLPHIN, GUYS.HOTDOG]:
                self.sprite_offset_x = -10
                self.sprite_offset_y = -28

        # handle pink transparancy
        self.image.set_colorkey((255, 0, 255))

    def draw(self):
        if not self.image:
            self.load_image()
        if self.type == GUYS.PLAYER:
            player = self.game.player
            if player.chrClass != CLASS.WARRIOR or player.life > (
                player.stat[STAT.LIF] / 4
            ):
                # AddToDispList(playerGfx[player.chrClass],MAP_X+me->x*TILE_WIDTH+TILE_WIDTH/2,me->y*TILE_HEIGHT+TILE_HEIGHT*3/4,-9,-22);

                # draw the sprite at the x/y tile in the map, adjusted for the
                # sprite size to the tile, plus the map offset, plus
                # (or minus, really) some completely arbitrary offset from the
                # original code
                self.game.screen.blit(
                    self.image,
                    (
                        self.x * TILE_WIDTH
                        + TILE_WIDTH / 2
                        + MAP_X
                        + self.sprite_offset_x,
                        self.y * TILE_HEIGHT
                        + TILE_HEIGHT * 3 / 4
                        + self.sprite_offset_y,
                    ),
                )
            else:
                self.game.screen.blit(
                    self.berserkImage,
                    (
                        self.x * TILE_WIDTH
                        + TILE_WIDTH / 2
                        + MAP_X
                        + self.sprite_offset_x,
                        self.y * TILE_HEIGHT
                        + TILE_HEIGHT * 3 / 4
                        + self.sprite_offset_y,
                    ),
                )

            if self.plan == PLAN.HUNT:
                printMe(self.game, "Hunting...", 8, 570)
            elif self.plan == PLAN.WANDER:
                printMe(self.game, "Wandering...", 8, 570)
            elif self.plan == PLAN.EXIT:
                printMe(self.game, "Finding a way out!", 8, 570)
        else:
            self.game.screen.blit(
                self.image,
                (
                    self.x * TILE_WIDTH + TILE_WIDTH / 2 + MAP_X + self.sprite_offset_x,
                    self.y * TILE_HEIGHT + TILE_HEIGHT * 3 / 4 + self.sprite_offset_y,
                ),
            )


def addGuy(game, guy_type, level):
    for i in range(MAX_GUYS):
        if game.map.guys[i] is None:
            guy = Guy(game)
            guy.type = guy_type
            guy.x, guy.y = findReallyEmptySpot(game)
            guy.level = (level * 5) + 1
            if guy_type == GUYS.PLAYER:
                makeSound(SFX.HUZZAH)
                guy.life = 1  # I think this does nothing
            else:
                guy.life = game.monster[guy_type.value].maxLife * (1 + level * 3)

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
        if guy and guy.type != GUYS.NONE:
            if guy.type == GUYS.PLAYER:
                guy.foodClock += food
                if guy.foodClock > 120:
                    guy.foodClock -= 120
                    eatFood(game)
                amount = game.player.stat[STAT.SPD]
                if amount < 1:
                    amount = 1
                guy.moves += amount * timePassed
            else:
                guy.moves += game.monster[guy.type.value].speed * guy.level * timePassed

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
                    updateGuy(game, guy)
                guy.moves -= 120 * FIXAMT
                if game.player.life == 0:
                    break
        if game.player.life == 0:
            break


def isEnemy(me, you):
    if me.type == GUYS.PLAYER and you.type != GUYS.PLAYER:
        return True
    if you.type == GUYS.PLAYER and me.type != GUYS.PLAYER:
        return True
    return False


def getNeighbors(game, x, y):
    neighbors = []
    # get guy at x, y
    guy = None
    # find yourself
    for i in range(MAX_GUYS):

        # got a None on the map here. So the map was removed but we are still fighting?
        if game.map.guys[i] is not None:
            if game.map.guys[i].x == x and game.map.guys[i].y == y:
                guy = game.map.guys[i]
                break
    for a in range(4):
        x = guy.x + offX[a]
        y = guy.y + offY[a]
        if x < 0 or x >= MAP_WIDTH or y < 0 or y >= MAP_HEIGHT:
            continue
        for i in range(MAX_GUYS):
            if game.map.guys[i] is not None:
                if (
                    game.map.guys[i].x == x
                    and game.map.guys[i].y == y
                    and isEnemy(guy, game.map.guys[i])
                ):
                    neighbors.append(game.map.guys[i])

    # sort neighbors by life. Lowest first
    neighbors.sort(key=lambda z: z.life)

    return neighbors


def moreBadGuysLive(game):
    if game.map.levelEmpty():
        return
    x = 0
    y = 0

    for i in range(MAX_GUYS):
        if game.map.guys[i] is not None:
            if game.map.guys[i].type != GUYS.PLAYER:
                return False
            if game.map.guys[i].type == GUYS.PLAYER:
                x = game.map.guys[i].x
                y = game.map.guys[i].y

    makeSound(SFX.VICTORY)
    gold_earned = (game.level.value + 1) * 10
    game.player.gold += gold_earned
    game.toasts.append(
        Toast(
            game,
            str(gold_earned),
            x * TILE_WIDTH + MAP_X + TILE_WIDTH / 2,
            y * TILE_HEIGHT + TILE_HEIGHT / 2,
            color=pygame.Color(255, 255, 0),
        )
    )


def updatePlayer(game):
    player = game.player
    # get player's Guy
    player_guy = game.map.get_player_guy()

    if (
        player.chrClass == CLASS.WARRIOR
        and player.life <= (player.stat[STAT.LIF] / 4)
        and not player.goneBerserk
    ):
        makeSound(SFX.BERSERK)
        player.goneBerserk = True

    # updateMap()
    moreBadGuysLive(game)
    player.drinkPotion()

    if player.food == 0:
        player.deathCause = DEATH_CAUSE.HUNGER
        gotKilled(game, player.deathCause)

    # get adjacent monsters
    neighbors = getNeighbors(game, player_guy.x, player_guy.y)
    a = None
    if len(neighbors) > 0:
        a = neighbors[0]
    # attack nearby monster
    if a is not None and a.type != GUYS.NONE:
        playerAttack(game, player, a)
        if player.chrClass == CLASS.THIEF:  # pickpocket
            gotIt = False
            for guy in neighbors:
                if random.randint(0, 10) == 0:
                    gotIt = True
                    player.gold += game.level.value + 1
                    x, y = get_map_xy(guy.x, guy.y)
                    game.toasts.append(
                        Toast(
                            game,
                            str(game.level.value + 1),
                            x,
                            y,
                            color=pygame.Color(255, 255, 0),
                        )
                    )

            if gotIt:
                makeSound(SFX.CHACHING)
        elif player.chrClass == CLASS.GUARD:  # circular strike
            strength = player.stat[STAT.STR]
            player.stat[STAT.STR] /= 2  # why?
            acc = player.stat[STAT.ACC]
            player.stat[STAT.ACC] /= 2  # dumb
            hit_second_enemy = False
            for neighbor in neighbors:
                if neighbor.type != GUYS.NONE:
                    playerAttack(game, player, neighbor)
                    hit_second_enemy = True
            if hit_second_enemy:
                makeSound(SFX.CIRCLE)
            player.stat[STAT.STR] = strength
            player.stat[STAT.ACC] = acc
    else:
        # no foe adjacent
        player_guy.planTime -= 1
        if player_guy.planTime == 0:
            player_guy.planTime = 3
            if (
                player.foodLeft()
                and not game.map.levelEmpty()
                and not player.shouldExit
            ):
                player_guy.plan = PLAN.HUNT
            else:
                if not player.foodLeft() and not player.haveSaidFood:
                    player.haveSaidFood = True
                    makeSound(SFX.NEEDFOOD)
                player_guy.plan = PLAN.EXIT
        if player_guy.plan == PLAN.WANDER:
            a = random.randint(0, 3)
            moveMe(game, player_guy, offX[a], offY[a])
        elif player_guy.plan == PLAN.HUNT:
            if not followNose2(game, player_guy):
                player_guy.plan = PLAN.WANDER
                player_guy.planTime = 3
        elif player_guy.plan == PLAN.EXIT:
            followNose(game, player_guy)
            if (
                game.map.map[player_guy.x + player_guy.y * MAP_WIDTH].type
                == TILE_TYPE.DOOR
            ):
                game.exitCode = EXIT_CODE.ESCAPED


def getTarget(game, guy):
    x = 0
    y = 0

    bestdist = -1
    for i in range(MAX_GUYS):
        other_guy = game.map.guys[i]
        if other_guy is not None:
            if (other_guy.type == GUYS.PLAYER and guy.type != GUYS.PLAYER) or (
                other_guy.type != GUYS.PLAYER and guy.type == GUYS.PLAYER
            ):
                if bestdist == -1:
                    dist = (other_guy.x - guy.x) * (other_guy.x - guy.x) + (
                        other_guy.y - guy.y
                    ) * (other_guy.y - guy.y)
                    x = other_guy.x
                    y = other_guy.y
                    bestdist = dist
                else:
                    dist = (other_guy.x - guy.x) * (other_guy.x - guy.x) + (
                        other_guy.y - guy.y
                    ) * (other_guy.y - guy.y)
                    if dist < bestdist:
                        x = other_guy.x
                        y = other_guy.y
                        bestdist = dist

    return x, y


def updateGuy(game, guy):

    # updateMap()
    neighbors = getNeighbors(game, guy.x, guy.y)
    a = None
    if len(neighbors) > 0:
        a = neighbors[0]
    if a:
        monsterAttack(game, guy, a)
    else:
        guy.planTime -= 1
        if guy.planTime == 0:
            guy.planTime = 25
            guy.plan = PLAN.HUNT

        if guy.plan == PLAN.WANDER:
            a = random.randint(0, 3)
            moveMe(game, guy, offX[a], offY[a])
        elif guy.plan == PLAN.HUNT:
            tx, ty = getTarget(game, guy)
            if abs(tx - guy.x) > abs(ty - guy.y):
                if tx < guy.x:
                    a = 2
                else:
                    a = 0
            else:
                if ty < guy.y:
                    a = 3
                else:
                    a = 1
            if not moveMe(game, guy, offX[a], offY[a]):
                guy.plan = PLAN.WANDER
                guy.planTime = random.randint(0, 4)


def followNose(game, guy):
    best = 0

    for a in range(1, 4):
        if (
            game.map.map[guy.x + offX[a] + (guy.y + offY[a]) * MAP_WIDTH].code
            > game.map.map[guy.x + offX[best] + (guy.y + offY[best]) * MAP_WIDTH].code
        ):
            best = a
    return moveMe(game, guy, offX[best], offY[best])


def followNose2(game, guy):
    best = 0
    for a in range(1, 4):
        if (
            game.map.map[guy.x + offX[a] + (guy.y + offY[a]) * MAP_WIDTH].monsNum
            > game.map.map[
                guy.x + offX[best] + (guy.y + offY[best]) * MAP_WIDTH
            ].monsNum
        ):
            best = a
    return moveMe(game, guy, offX[best], offY[best])


if __name__ == "__main__":
    import main

    main.main()

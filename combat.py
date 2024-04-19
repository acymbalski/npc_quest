import random

from constants import (
    CLASS,
    DEATH_CAUSE,
    EXIT_CODE,
    GameState,
    GUYS,
    MAP_HEIGHT,
    MAP_WIDTH,
    MAX_GUYS,
    NOTICE,
    PLAN,
    SFX,
    STAT,
    TILE_TYPE,
)
from hiscore import addHiScore

from sound import makeSound

from utilities import delGame


def gotKilled(game, how):
    print(f"Player died via {how}")
    game.player.life = 0
    game.player.deathHow = how.value
    game.player.deathCause = how
    game.exitCode = EXIT_CODE.DIED
    if how == DEATH_CAUSE.HUNGER:
        game.noticeType = NOTICE.STARVED
    else:
        game.noticeType = NOTICE.MURDERED
    game.game_state = GameState.NOTICE
    game.map = None
    delGame(game.player.slot)
    addHiScore(game)


def getKicked(game, me, kicker):
    dx = 0
    dy = 0
    if kicker.x > me.x:
        dx = -1
        dy = 0
    elif kicker.x < me.x:
        dx = 1
        dy = 0
    else:
        if kicker.y < me.y:
            dx = 0
            dy = 1
        else:
            dx = 0
            dy = -1
    moveMe(game, me, dx, dy)
    moveMe(game, me, dx, dy)


def playerAttack(game, me, you):

    hitChance = game.player.stat[STAT.ACC] * 20 - you.level * 10
    if hitChance < 5:
        hitChance = 5

    if random.randint(1, 100) <= hitChance:
        makeSound(SFX.HITBADGUY)
        damage = (
            game.player.stat[STAT.STR]
            - game.monster[you.type.value].defense
            + you.level
            - 1
        )
        if damage < 1:
            damage = 1
        if (
            game.player.chrClass == CLASS.DOCTOR
            and random.randint(1, 100) < game.player.level
        ):
            makeSound(SFX.CRITICAL)
            if damage < 9999:
                damage = 9999
        # TODO: AddNum
        if you.life > damage:
            you.life -= damage
            if game.player.chrClass == CLASS.MULE:
                getKicked(game, you, me)
        else:
            you.life = 0
            badGuyDie(game, you)
            if (
                game.player.chrClass == CLASS.CHEF
                and random.randint(1, 100) < game.player.level * 2
            ):
                makeSound(SFX.CHOMP)
                if game.player.life < game.player.stat[STAT.LIF]:
                    game.player.life += 1
                    # TODO: healPlayerNum
    else:
        makeSound(SFX.WHIFF)


def monsterAttack(game, me, you):
    hitChance = (
        game.monster[me.type.value].accuracy + me.level
    ) * 20 - game.player.level * 10
    if hitChance < 5:
        hitChance = 5

    if random.randint(1, 100) < hitChance:
        makeSound(SFX.HITPLAYER)
        damage = (game.monster[me.type.value].strength + me.level) - (
            game.player.stat[STAT.DEF] + game.player.level - 1
        )
        if damage < 1:
            damage = 1
            # TODO: AddNum
        if game.player.life > damage:
            game.player.life -= damage
        else:
            game.player.deathCause = me.type
            gotKilled(game, me.type)
            makeSound(SFX.PLAYERDIE)
    else:
        makeSound(SFX.WHIFF)


def badGuyDie(game, me):
    amount = game.monster[me.type.value].xp * me.level * game.player.stat[STAT.INT] / 20
    if amount < 1:
        amount = 1

    game.player.xp += amount
    game.player.gold += game.monster[me.type.value].gold + me.level
    me.type = GUYS.NONE
    makeSound(SFX.DEADGUY)
    game.levelUp()


def moveMe(game, guy, dx, dy):
    if (
        guy.x + dx < 0
        or guy.y + dy < 0
        or guy.x + dx >= MAP_WIDTH
        or guy.y + dy >= MAP_HEIGHT
        or (game.map.map[guy.x + dx + (guy.y + dy) * MAP_WIDTH].type != TILE_TYPE.FLOOR)
        and game.map.map[guy.x + dx + (guy.y + dy) * MAP_WIDTH].type != TILE_TYPE.DOOR
    ):
        return False
    for i in range(MAX_GUYS):
        if game.map.guys[i] is not None:
            if game.map.guys[i].x == guy.x + dx and game.map.guys[i].y == guy.y + dy:
                return False
    guy.x += dx
    guy.y += dy
    return True


def zapBadGuys(game):
    makeSound(SFX.ZAP)
    for i in range(MAX_GUYS):
        guy = game.map.guys[i]
        if guy and guy.type != GUYS.PLAYER and guy.type != GUYS.NONE and guy.life > 0:
            guy.life -= 1
            if guy.life == 0:
                badGuyDie(game, guy)

            # addNum


def chickenOut(game):
    for i in range(MAX_GUYS):
        guy = game.map.guys[i]
        if guy and guy.type == GUYS.PLAYER:
            if guy.plan == PLAN.EXIT:
                makeSound(SFX.CHICKEN)
                game.exitCode = EXIT_CODE.ESCAPED
                return

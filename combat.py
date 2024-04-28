import random

import pygame

from constants import (
    CLASS,
    DEATH_CAUSE,
    DEATH_NAMES,
    EXIT_CODE,
    GameState,
    get_map_xy,
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
from toast import Toast

from utilities import delGame


def gotKilled(game, how):
    """
    Called when the player dies.
    Not a big fan of this, in fact it's really confusing now with all this
    mumbo-jumbo I had to add.
    Please fix this.
    """

    print(f"Player died via {how}")
    game.player.life = 0
    game.player.deathHow = how.value
    game.player.deathCause = DEATH_NAMES[how]
    game.exitCode = EXIT_CODE.DIED
    if how == DEATH_CAUSE.HUNGER:
        game.noticeType = NOTICE.STARVED
    else:
        game.noticeType = NOTICE.MURDERED
    game.game_state = GameState.NOTICE
    game.map = None

    # remove player save
    delGame(game.player.slot)

    # add to high score list
    addHiScore(game)

    # reload global high scores
    game.reload_global_scores()


def getKicked(game, me, kicker):
    """
    Used when the Pack Mule kicks an enemy. Calculates where the enemy gets
    pushed to.
    """
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
    """
    Player attacks a bad guy.
    """

    hitChance = game.player.stat[STAT.ACC] * 20 - you.level * 10
    if hitChance < 5:
        hitChance = 5

    if random.randint(1, 100) <= hitChance:
        makeSound(SFX.HITBADGUY)

        # how much damage should we do?
        damage = (
            game.player.stat[STAT.STR]
            - game.monster[you.type.value].defense
            + you.level
            - 1
        )
        if damage < 1:
            damage = 1

        # Doctor can do a pre-emptive autopsy
        if (
            game.player.chrClass == CLASS.DOCTOR
            and random.randint(1, 100) < game.player.level
        ):
            makeSound(SFX.CRITICAL)
            if damage < 9999:
                damage = 9999

        # draw damage text
        x, y = get_map_xy(you.x, you.y)
        game.toasts.append(
            Toast(
                game,
                str(-damage),
                x,
                y,
                color=pygame.Color(255, 0, 0),
            )
        )

        # if player is a Pack Mule and the bad guy won't die from this attack,
        # kick them
        if you.life > damage:
            you.life -= damage
            if game.player.chrClass == CLASS.MULE:
                getKicked(game, you, me)
        else:
            # otherwise, they're dead
            you.life = 0
            badGuyDie(game, you)

            # Chef may be able to eat!
            if (
                game.player.chrClass == CLASS.CHEF
                and random.randint(1, 100) < game.player.level * 2
            ):
                makeSound(SFX.CHOMP)
                if game.player.life < game.player.stat[STAT.LIF]:
                    game.player.life += 1
                    player_guy = game.map.get_player_guy()
                    x, y = get_map_xy(player_guy.x, player_guy.y)
                    game.toasts.append(
                        Toast(
                            game,
                            "1",
                            x,
                            y,
                            color=pygame.Color(0, 255, 0),
                        )
                    )
    else:
        # Whiff!
        makeSound(SFX.WHIFF)


def monsterAttack(game, me, you):
    """
    Bad guy attacks the player.
    """

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

        # draw damage text
        x, y = get_map_xy(you.x, you.y)
        game.toasts.append(
            Toast(
                game,
                str(-damage),
                x,
                y,
                color=pygame.Color(255, 0, 0),
            )
        )

        if game.player.life > damage:
            game.player.life -= damage
        else:
            # killed player!
            game.player.deathCause = DEATH_NAMES[me.type]
            gotKilled(game, me.type)
            makeSound(SFX.PLAYERDIE)
    else:
        # Whiff!
        makeSound(SFX.WHIFF)


def badGuyDie(game, me):
    """
    Bad guy dies. Increment gold, XP, and check for a level up. Don't like this!
    """
    amount = game.monster[me.type.value].xp * me.level * game.player.stat[STAT.INT] / 20
    if amount < 1:
        amount = 1

    game.player.xp += int(amount)
    game.player.gold += game.monster[me.type.value].gold + me.level

    # mark this guy as dead. The cleanup is handled elsewhere for some reason.
    me.type = GUYS.NONE
    makeSound(SFX.DEADGUY)
    game.levelUp()


def moveMe(game, guy, dx, dy):
    """
    Move a Guy in a direction. Check for walls, doors, and other Guys.
    """
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
    """
    Zap all bad guys on the map!
    """
    makeSound(SFX.ZAP)
    for i in range(MAX_GUYS):
        guy = game.map.guys[i]
        if guy and guy.type != GUYS.PLAYER and guy.type != GUYS.NONE and guy.life > 0:
            guy.life -= 1
            if guy.life == 0:
                badGuyDie(game, guy)

            # draw damage text
            x, y = get_map_xy(guy.x, guy.y)
            game.toasts.append(
                Toast(
                    game,
                    "-1",
                    x,
                    y,
                    color=pygame.Color(255, 0, 0),
                )
            )


def chickenOut(game):
    """
    Exit the map!
    """
    for i in range(MAX_GUYS):
        guy = game.map.guys[i]
        if guy and guy.type == GUYS.PLAYER:
            if guy.plan == PLAN.EXIT:
                makeSound(SFX.CHICKEN)
                game.exitCode = EXIT_CODE.ESCAPED
                return

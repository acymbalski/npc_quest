from constants import STAT, SFX, GUYS, DEATH_CAUSE
from character import CLASS
from sound import makeSound
import random
from critter import getKicked
from action import gotKilled


def playerAttack(game, me, you):
    hitChance = game.player.stat[STAT.ACC] * 20 - you.level * 10
    if hitChance < 5:
        hitChance = 5

    if random.randint(1, 100) <= hitChance:
        makeSound(SFX.HITBADGUY)
        damage = (
            game.player.stat[STAT.STR] - game.monster[you.type].defense + you.level - 1
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


def badGuyAttack(game, me, you):
    hitChance = (
        game.monster[me.type].accuracy + me.level
    ) * 20 - game.player.level * 10
    if hitChance < 5:
        hitChance = 5

    if random.randint(1, 100) < hitChance:
        makeSound(SFX.HITPLAYER)
        damage = (game.monster[me.type].strength + me.level) - (
            game.player.stat[STAT.DEF] + game.player.level - 1
        )
        if damage < 1:
            damage = 1
            # TODO: AddNum
        if game.player.life > damage:
            game.player.life -= damage
        else:
            game.player.deathCause = me.type
            gotKilled(game, DEATH_CAUSE.MONSTER)
            makeSound(SFX.PLAYERDIE)
    else:
        makeSound(SFX.WHIFF)


def badGuyDie(game, me):
    amount = game.monster[me.type].xp * me.level * game.player.stat[STAT.INT] / 20
    if amount < 1:
        amount = 1

    game.player.xp += amount
    game.player.gold += game.monster[me.type].gold + me.level
    me.type = GUYS.NONE
    makeSound(SFX.DEADGUY)
    game.levelUp()

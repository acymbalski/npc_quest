import os
import pickle
import random
from enum import Enum

from combat import chickenOut, zapBadGuys

from constants import (
    CLASS,
    classBonus,
    className,
    DEATH_CAUSE,
    ITEM_EFFECT,
    ITEM_TYPE,
    NUM_STATS,
    SFX,
    STAT,
)
from display import printMe
from item import getIcon, Item, netWeightEffect, sortItems, statChangeFromItem
from sound import makeSound


class Character:

    def __init__(self):
        self.stat = {
            STAT.STR: 1,
            STAT.SPD: 1,
            STAT.ACC: 1,
            STAT.INT: 1,
            STAT.DEF: 1,
            STAT.STO: 1,
            STAT.CHA: 1,
            STAT.LIF: 10,
            STAT.CAR: 20,
        }

        self.xp = 0
        self.needXP = 10
        self.level = 1
        self.life = 10
        self.gold = 20
        self.totalWeight = 0
        self.itemCount = 0
        self.food = 50

        self.inventory = [
            None,
        ] * 20  # player has 20 inventory slots; value '255' means empty. We have replaced it with None
        self.ptSpend = [0] * NUM_STATS
        self.chrClass = CLASS.PEASANT
        self.shouldExit = 0
        self.name = makeUpName()
        self.deathCause = DEATH_CAUSE.NONE
        self.deathHow = 0
        self.slot = 0
        self.score = 0

        self.goneBerserk = False
        self.haveSaidFood = False

    def __str__(self):
        return f"Character-> xp: {self.xp}, level: {self.level}, life: {self.life}, gold: {self.gold}, totalWeight: {self.totalWeight}, itemCount: {self.itemCount}, food: {self.food}, inventory: {self.inventory}, ptSpend: {self.ptSpend}, chrClass: {self.chrClass}, shouldExit: {self.shouldExit}, name: {self.name}, deathCause: {self.deathCause}, slot: {self.slot}, score: {self.score}, goneBerserk: {self.goneBerserk}"

    def drinkPotion(self):
        # iterate through inventory
        for i in range(len(self.inventory)):
            item = self.inventory[i]
            # if item is not None
            if item:
                # if item is a potion
                if item.type == ITEM_TYPE.POTION:
                    if self.life < self.stat[STAT.LIF] - item.value or self.life < (
                        self.stat[STAT.LIF] / 3
                    ):
                        amount = self.stat[STAT.LIF] - self.life
                        # TODO: healPlayerNum(amount)
                        self.life += amount
                        statChangeFromItem(self, item, -1)
                        self.inventory[i] = None
                        makeSound(SFX.DRINK)
                        # sort inventory
                        self.inventory = sortItems(self.inventory)
                        return

    def foodLeft(self):
        for item in self.inventory:
            if item:
                if item.type == ITEM_TYPE.FOOD:
                    return True
        return False

    def getStatChanges(self, item, to_equip=True):
        strength = 0
        speed = 0
        accuracy = 0
        intellect = 0
        defense = 0
        stomach = 0
        charisma = 0
        life = 0
        weight = 0

        mult = 1
        if not to_equip:
            mult = -1

        # if this item is replacing single-carry items,
        # get the stat changes from un-equiping that item and then apply the new changes
        unequip_stat_changes = {
            STAT.STR: 0,
            STAT.SPD: 0,
            STAT.ACC: 0,
            STAT.INT: 0,
            STAT.DEF: 0,
            STAT.STO: 0,
            STAT.CHA: 0,
            STAT.LIF: 0,
            STAT.CAR: 0,
        }
        if (
            item.type
            not in [
                ITEM_TYPE.POTION,
                ITEM_TYPE.RING,
                ITEM_TYPE.FOOD,
            ]
            and to_equip
        ):  # multi-carry items
            for held_item in self.inventory:
                if held_item:
                    if held_item.type == item.type:
                        unequip_stat_changes = self.getStatChanges(
                            held_item, to_equip=False
                        )

        if item.type in [ITEM_TYPE.ARMOR, ITEM_TYPE.HELMET, ITEM_TYPE.SHIELD]:
            defense += mult * item.value
        elif item.type == ITEM_TYPE.WEAPON:
            strength += mult * item.value
        elif item.type == ITEM_TYPE.GAUNTLET:
            accuracy += mult * item.value
        elif item.type == ITEM_TYPE.BOOTS:
            speed += mult * item.value

        for eff, val in [
            (item.effect, item.effValue),
            (item.effect2, item.eff2Value),
        ]:
            if eff == ITEM_EFFECT.ALL:
                strength += mult * val
                speed += mult * val
                accuracy += mult * val
                intellect += mult * val
                defense += mult * val
                stomach += mult * val
                charisma += mult * val
                life += mult * val
                weight += mult * val
            elif eff == ITEM_EFFECT.STRENGTH:
                strength += mult * val
            elif eff == ITEM_EFFECT.DEFENSE:
                defense += mult * val
            elif eff == ITEM_EFFECT.STOMACH:
                stomach += mult * val
            elif eff == ITEM_EFFECT.SPEED:
                speed += mult * val
            elif eff == ITEM_EFFECT.ACCURACY:
                accuracy += mult * val
            elif eff == ITEM_EFFECT.CHARISMA:
                charisma += mult * val
            elif eff == ITEM_EFFECT.LIFE:
                life += mult * val
            elif eff == ITEM_EFFECT.CARRY:
                weight += mult * val
            elif eff == ITEM_EFFECT.IQ:
                intellect += mult * val

        return {
            STAT.STR: strength + unequip_stat_changes[STAT.STR],
            STAT.SPD: speed + unequip_stat_changes[STAT.SPD],
            STAT.ACC: accuracy + unequip_stat_changes[STAT.ACC],
            STAT.INT: intellect + unequip_stat_changes[STAT.INT],
            STAT.DEF: defense + unequip_stat_changes[STAT.DEF],
            STAT.STO: stomach + unequip_stat_changes[STAT.STO],
            STAT.CHA: charisma + unequip_stat_changes[STAT.CHA],
            STAT.LIF: life + unequip_stat_changes[STAT.LIF],
            STAT.CAR: weight + unequip_stat_changes[STAT.CAR],
        }

    def roomToEquip(self, item: Item) -> bool:
        # return True or False if the player has room to equip an item
        weight = item.weight
        if item.type not in [ITEM_TYPE.POTION, ITEM_TYPE.RING, ITEM_TYPE.FOOD]:
            # iterate over inventory. If we are buying this item by now, it's replacing something we already have
            # so don't double-count the weights
            for held_item in self.inventory:
                if held_item:
                    if held_item.type == item.type:
                        weight -= netWeightEffect(held_item)

        if weight + self.totalWeight > self.stat[STAT.CAR]:
            makeSound(SFX.HEAVY)
            return False
        # if we have a full 20 items...
        if len([item for item in self.inventory if item]) == 20:
            makeSound(SFX.HEAVY)
            return False
        return True


def renderCharacterData(game, shop=False):
    """
    Render character data - stats, name, inventory, etc - to the screen.
    if shop is True, don't render the inventory
    """
    character = game.player
    printMe(game, character.name, 8, 8)
    printMe(
        game,
        f"Level {character.level} {className(game.player.chrClass)}",
        8,
        18,
    )
    printMe(game, "{:<10} {}".format("Strength:", character.stat[STAT.STR]), 8, 28)
    printMe(game, "{:<10} {}".format("Speed:", character.stat[STAT.SPD]), 8, 38)
    printMe(game, "{:<10} {}".format("Accuracy:", character.stat[STAT.ACC]), 8, 48)
    printMe(game, "{:<10} {}".format("Intellect:", character.stat[STAT.INT]), 8, 58)
    printMe(game, "{:<10} {}".format("Defense:", character.stat[STAT.DEF]), 8, 68)
    printMe(game, "{:<10} {}".format("Stomach:", character.stat[STAT.STO]), 8, 78)
    printMe(game, "{:<10} {}".format("Charisma:", character.stat[STAT.CHA]), 8, 88)

    printMe(
        game, "{:<10} {}".format("XP needed:", character.needXP - character.xp), 8, 108
    )
    printMe(game, "{:<10} {}".format("Life:", character.stat[STAT.LIF]), 8, 118)

    printMe(game, "{:<10} {}".format("Weight:", character.stat[STAT.CAR]), 8, 128)
    printMe(game, "{:<10} ${}".format("Gold:", character.gold), 8, 138)

    printMe(game, "Inventory", 8, 158)
    if not shop:
        for i in range(20):
            if character.inventory[i]:
                game.screen.blit(getIcon(character.inventory[i]), (8, 178 + i * 10))
                printMe(game, character.inventory[i].name, 19, 178 + i * 10)
            else:
                printMe(game, "......", 19, 178 + i * 10)

    if character.chrClass != CLASS.PEASANT:
        printMe(game, "Special Ability:", 8, 400)
        printMe(game, classBonus[character.chrClass], 20, 410)

    printMe(game, f"Food In Tummy: {int(character.food)}", 8, 580)


def renderLevelUpLine(c: int, name: str, stat: int):
    pass


def renderLevelUpData(c: int):
    pass


def printItemEffect(amt: int, y: int):
    pass


def printItemEffectReverse(amt: int, y: int):
    pass


def renderItemEffects():
    pass


def calcItemEffects(itm: int):
    # calculate the effects of an item without actually equipping it
    # there is a better way to do this once some logic is ironed out
    pass


def calcSellEffects(itm: int):
    pass


def eatFood(game):
    player = game.player

    if player.chrClass == CLASS.WIZARD:
        if random.randint(1, 100) < player.level:
            zapBadGuys(game)
    if player.chrClass == CLASS.SALESMAN:
        if random.randint(1, 100) < player.level:
            chickenOut(game)

    amount = 0

    for i in range(7):
        amount += player.stat[STAT(i)]

    amount = (amount - player.stat[STAT.STO]) / 8 - player.stat[STAT.STO]

    if amount < 1:
        amount = 1

    if player.food > amount:
        player.food -= amount
        if player.food > 0:
            return  # don't need any!
    else:
        player.food = 0

    for i in range(20):
        if player.inventory[i]:
            item = player.inventory[i]
            # eat!
            if item.type == ITEM_TYPE.FOOD:
                statChangeFromItem(player, item, -1)
                player.food += item.value * 100
                player.inventory[i] = None
                makeSound(SFX.EAT)
                player.inventory = sortItems(player.inventory)
                return


MAX_NAMETYPES = 10


def makeUpName() -> str:
    name_format = [
        "Cvcvvc",
        "Cvvcv Cvccv",
        "Cvv C'Cvcc",
        "Cvcvcv",
        "Cvvcvv",
        "Vcvvcv",
        "Vvcv",
        "Vccvcvv",
        "Vcvcvv",
        "Vccvv Cvcv",
    ]
    vowel = "aeiouy"
    consonant = "bcdfghjklmnpqrstvwxz"

    name = random.choice(name_format)

    for character in name:
        if character == "C":
            name = name.replace("C", random.choice(consonant).upper(), 1)
        elif character == "c":
            name = name.replace("c", random.choice(consonant), 1)
        elif character == "V":
            name = name.replace("V", random.choice(vowel).upper(), 1)
        elif character == "v":
            name = name.replace("v", random.choice(vowel), 1)
        elif character == " ":
            name = name.replace(" ", " ", 1)
        elif character == "'":
            name = name.replace("'", "'", 1)

    return name

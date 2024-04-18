import os
import pickle
import random
from enum import Enum

from combat import chickenOut, zapBadGuys

from constants import CLASS, classBonus, DEATH_CAUSE, NUM_STATS, SFX, STAT
from display import printMe
from item import getIcon, Item, ITEM_TYPE, sortItems, statChangeFromItem
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
        for item in self.inventory:
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
                        self.inventory[item] = None
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


def roomToEquip(weight: int, type: Item) -> bool:
    # return True or False if the player has room to equip an item
    # TODO: think about this one
    if type.type not in [ITEM_TYPE.POTION, ITEM_TYPE.RING, ITEM_TYPE.FOOD]:
        # iterate over inventory, calculate net weights?
        for item in player.inventory:
            if item:
                if item.type == type.type:
                    weight -= netWeightEffect(item)

    if weight + player.totalWeight > player.stat[STAT.CAR]:
        # TODO: MakeSound(SND_HEAVY)
        return False
    if player.itemCount == 20:
        # TODO: MakeSound(SND_HEAVY)
        return False
    return True


def renderCharacterData(game):
    character = game.player
    printMe(game, character.name, 8, 8)
    printMe(game, f"Level: {character.level}", 8, 18)
    printMe(game, f"Strength: {character.stat[STAT.STR]}", 8, 28)
    printMe(game, f"Speed: {character.stat[STAT.SPD]}", 8, 38)
    printMe(game, f"Accuracy: {character.stat[STAT.ACC]}", 8, 48)
    printMe(game, f"Intellect: {character.stat[STAT.INT]}", 8, 58)
    printMe(game, f"Defense: {character.stat[STAT.DEF]}", 8, 68)
    printMe(game, f"Stomach: {character.stat[STAT.STO]}", 8, 78)
    printMe(game, f"Charisma: {character.stat[STAT.CHA]}", 8, 88)

    printMe(game, f"XP needed: {character.needXP-character.xp}", 8, 108)
    printMe(game, f"Life: {character.stat[STAT.LIF]}", 8, 118)

    printMe(game, f"Weight: {character.stat[STAT.CAR]}", 8, 128)
    printMe(game, f"Gold: {character.gold}", 8, 138)

    printMe(game, "Inventory", 8, 158)
    for i in range(20):
        if character.inventory[i]:
            game.screen.blit(getIcon(character.inventory[i]), (8, 178 + i * 10))
            printMe(game, character.inventory[i].name, 19, 178 + i * 10)
        else:
            printMe(game, "......", 19, 178 + i * 10)

    if character.chrClass != CLASS.PEASANT:
        printMe(game, "Special Ability:", 8, 400)
        printMe(game, classBonus[character.chrClass], 20, 410)

    printMe(game, f"Food In Tummy: {character.food}", 8, 580)


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


def foodLeft():
    pass


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

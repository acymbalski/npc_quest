import random
from item import Item, getIcon
from enum import Enum
import pickle
import os
from display import printMe
from enums import STAT


class CLASS(Enum):
    PEASANT = 0
    WARRIOR = 1
    THIEF = 2
    RANGER = 3
    WIZARD = 4
    GUARD = 5
    CHEF = 6
    SALESMAN = 7
    DOCTOR = 8
    MULE = 9


NUM_STATS = 9


classBonus = [
    "",  # peasant
    "Berserk Rage",  # warrior
    "Pickpocket",  # thief
    "Bow Attack",  # ranger
    "Infernal Blast",  # wizard
    "Spinning Strike",  # guard
    "Snack Attack",  # chef
    "Chicken Out",  # salesman
    "Preemptive Autopsy",  # doctor
    "Mule Kick",  # pack mule
]


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
        self.deathCause = 0
        self.slot = 0
        self.score = 0


def roomToEquip(weight: int, type: Item) -> bool:
    # return True or False if the player has room to equip an item
    # TODO: think about this one
    if type.type not in [ITM_POTION, ITM_RING, ITM_FOOD]:
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


def className(i: int) -> str:

    if i == CLASS.PEASANT:
        return "Peasant"
    if i == CLASS.WARRIOR:
        return "Warrior"
    if i == CLASS.THIEF:
        return "Thief"
    if i == CLASS.RANGER:
        return "Ranger"
    if i == CLASS.WIZARD:
        return "Wizard"
    if i == CLASS.GUARD:
        return "Guard"
    if i == CLASS.CHEF:
        return "Chef"
    if i == CLASS.SALESMAN:
        return "Used Car Salesman"
    if i == CLASS.DOCTOR:
        return "Doctor"
    if i == CLASS.MULE:
        return "Pack Mule"
    return "Unknown"


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


def eatFood():
    pass


def foodLeft():
    pass


def levelUp():
    pass


def drinkPotion():
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


def loadGame(w: int) -> Character:
    # load game from save/save00X.sav
    filename = f"save/save00{w}.sav"
    try:
        with open(filename, "rb") as file:
            character = pickle.load(file)
        return character
    except Exception:
        return None


def delGame(w: int) -> bool:
    # delete game from save/save00X.sav
    filename = f"save/save00{w}.sav"
    try:
        os.remove(filename)
        return True
    except Exception:
        return False


def savegame(character: Character) -> bool:
    # save game to save/save00X.sav
    saveDir = "save"
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)
    filename = f"{saveDir}/save00{character.slot}.sav"
    try:
        with open(filename, "wb") as file:
            pickle.dump(character, file)
        return True
    except Exception as e:
        print(f"Error saving game: {e}")
        return False

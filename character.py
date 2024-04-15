import random
from item import Item
from enum import Enum
import pickle
import os


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


class STAT(Enum):
    STR = 0
    SPD = 1
    ACC = 2
    INT = 3
    DEF = 4
    STO = 5
    CHA = 6
    LIF = 7
    CAR = 8


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


def sortInventory():
    # sort inventory by item type, then by cost
    inventory = player.inventory  # a list of Item objects, or None
    inventory.sort(
        key=lambda item: (
            (item.type, item.cost) if item else (float("inf"), float("inf"))
        )
    )


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


def renderCharacterData():
    pass


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
    filename = f"save/save00{character.slot}.sav"
    try:
        with open(filename, "wb") as file:
            pickle.dump(character, file)
        return True
    except Exception:
        return False

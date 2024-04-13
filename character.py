import random

CLASS_PEASANT = 0
CLASS_WARRIOR = 1
CLASS_THIEF = 2
CLASS_RANGER = 3
CLASS_WIZARD = 4
CLASS_GUARD = 5
CLASS_CHEF = 6
CLASS_SALESMAN = 7
CLASS_DOCTOR = 8
CLASS_MULE = 9

STAT_STR = 0
STAT_SPD = 1
STAT_ACC = 2
STAT_INT = 3
STAT_DEF = 4
STAT_STO = 5
STAT_CHA = 6
STAT_LIF = 7
STAT_CAR = 8
NUM_STATS = 9


class Character:

    def __init__(self):
        self.stat = [1, 1, 1, 1, 1, 1, 1, 10, 20]
        self.xp = 0
        self.needXP = 10
        self.level = 1
        self.life = 10
        self.gold = 20
        self.totalWeight = 0
        self.itemCount = 0
        self.food = 50

        self.inventory = [
            255
        ] * 20  # player has 20 inventory slots; value '255' means empty
        self.ptSpend = [0] * NUM_STATS
        self.chrClass = CLASS_PEASANT
        self.shouldExit = 0
        self.name = makeUpName()
        self.deathCause = 0
        self.slot = 0


def sortInventory():
    pass


def roomToEquip(weight: int, type: int) -> int:
    pass


def renderCharacterData():
    pass


def renderLevelUpLine(c: int, name: str, stat: int):
    pass


def className(i: int) -> str:

    if i == CLASS_PEASANT:
        return "Peasant"
    if i == CLASS_WARRIOR:
        return "Warrior"
    if i == CLASS_THIEF:
        return "Thief"
    if i == CLASS_RANGER:
        return "Ranger"
    if i == CLASS_WIZARD:
        return "Wizard"
    if i == CLASS_GUARD:
        return "Guard"
    if i == CLASS_CHEF:
        return "Chef"
    if i == CLASS_SALESMAN:
        return "Used Car Salesman"
    if i == CLASS_DOCTOR:
        return "Doctor"
    if i == CLASS_MULE:
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

    t = random.randint(0, MAX_NAMETYPES - 1)
    for i in range(len(name_format[t])):
        if name_format[t][i] == "C":
            player.name[i] = consonant[random.randint(0, 21)].upper()
        elif name_format[t][i] == "c":
            player.name[i] = consonant[random.randint(0, 21)]
        elif name_format[t][i] == "V":
            player.name[i] = vowel[random.randint(0, 6)].upper()
        elif name_format[t][i] == "v":
            player.name[i] = vowel[random.randint(0, 6)]
        elif name_format[t][i] == " ":
            player.name[i] = " "
        elif name_format[t][i] == "'":
            player.name[i] = "'"


def loadGame(w: int) -> int:
    pass


def delGame(w: int):
    pass


def savegame(w: int):
    pass

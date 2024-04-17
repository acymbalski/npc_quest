from enum import Enum

FIXAMT = 256

NUM_STATS = 9

MAX_NUMS = 16

MAX_GUYS = 128

TILE_WIDTH = 16
TILE_HEIGHT = 16

XRES = 800
YRES = 600

MAP_X = 800 - 576  # 800 is technically supposed to be the screen width
MAP_WIDTH = int(576 / TILE_WIDTH)
MAP_HEIGHT = int(
    600 / TILE_HEIGHT
)  # 600 is technically supposed to be the screen height

offX = [1, 0, -1, 0]
offY = [0, 1, 0, -1]

SHOP_AMT = 40


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


class ITEM_TYPE(Enum):
    FOOD = 1
    POTION = 2
    WEAPON = 3
    ARMOR = 4
    SHIELD = 5
    HELMET = 6
    BOOTS = 7
    GAUNTLET = 8
    RING = 9
    AMULET = 10


class ITEM_EFFECT(Enum):
    NONE = 0
    ALL = 1  # boost all stats
    STRENGTH = 2
    SPEED = 3
    ACCURACY = 4
    CHARISMA = 5
    CARRY = 6
    DEFENSE = 7
    STOMACH = 8
    LIFE = 9
    IQ = 10


class GameState(Enum):
    QUIT = -1
    TITLE = 0
    SHOP = 1
    GAME = 2


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


class SFX(Enum):
    HUZZAH = 0
    WHIFF = 1
    HITBADGUY = 2
    HITPLAYER = 3
    DEADGUY = 4
    NEEDFOOD = 5
    PLAYERDIE = 6
    EAT = 7
    LEVELUP = 8
    VICTORY = 9
    CHACHING = 10
    HEAVY = 11
    PRICEY = 12
    DRINK = 13
    CIRCLE = 14
    ARROW = 15
    ZAP = 16
    CHOMP = 17
    CHICKEN = 18
    CRITICAL = 19
    BERSERK = 20


class LEVEL(Enum):
    GNOMEY_PLAINS = 0
    FLOOFY_WOODS = 1
    THE_ISLE_OF_TERROR = 2
    ROCKY_DIRTVILLE = 3
    LAVALAVA_HOT_SPRINGS = 4
    THE_TEMPLE_OF_SPOON = 5
    FROSTY_HILL = 6
    DEADLY_DUNGEON = 7
    A_WEIRD_PLACE = 8
    THE_EVILNESS_PIT = 9
    SHIFT_Q = 10


LEVELS = {
    LEVEL.GNOMEY_PLAINS: "Gnomey Plains",
    LEVEL.FLOOFY_WOODS: "Floofy Woods",
    LEVEL.THE_ISLE_OF_TERROR: "The Isle Of Terror",
    LEVEL.ROCKY_DIRTVILLE: "Rocky Dirtville",
    LEVEL.LAVALAVA_HOT_SPRINGS: "Lavalava Hot Springs",
    LEVEL.THE_TEMPLE_OF_SPOON: "The Temple Of Spoon",
    LEVEL.FROSTY_HILL: "Frosty Hill",
    LEVEL.DEADLY_DUNGEON: "Deadly Dungeon",
    LEVEL.A_WEIRD_PLACE: "A Weird Place",
    LEVEL.THE_EVILNESS_PIT: "The Evilness Pit",
    LEVEL.SHIFT_Q: "Shift Q",
}


class TILE_TYPE(Enum):
    FLOOR = 0
    WALL = 1
    DOOR = 2


class EXIT_CODE(Enum):
    NONE = 0
    ESCAPED = 2
    DIED = 3


class GUYS(Enum):
    NONE = 0
    PLAYER = 1
    GNOME = 2
    FATBIRD = 3
    DOLPHIN = 4
    HOTDOG = 5
    REINDEER = 6
    BLUEY = 7


class MONSTER(Enum):
    NONE = 0
    NONEEITHER = 1
    GNOME = 2
    FATBIRD = 3
    DOLPHIN = 4
    HOTDOG = 5
    REINDEER = 6
    BLUEY = 7


class PLAN(Enum):
    WANDER = 0
    HUNT = 1
    EXIT = 2


class DEATH_CAUSE(Enum):
    HUNGER = 0
    MONSTER = 1

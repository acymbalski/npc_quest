from enum import Enum


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


class TILE_TYPE(Enum):
    FLOOR = 0
    WALL = 1
    DOOR = 2


class EXIT_CODE(Enum):
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

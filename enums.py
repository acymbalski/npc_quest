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

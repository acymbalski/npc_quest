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

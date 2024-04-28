from enum import Enum


# What a gnarly file.
# There is no real equivalent in the original game. There are a fair few enum-like
# structures in the original code, I went ahead and updated... most of them...
# to Enums. Not that it's really any better.
# Tons of stuff is defined here, like window size and some things that control
# the sizes of some of the fixed arrays.


# used in a couple places as fixed number for some math calculations.
# Could likely be done away with.
FIXAMT = 256

# Number of stats a player has. Defines a fixed array.
NUM_STATS = 9

# Max number of guys on a map
MAX_GUYS = 128

# Max number of high scores to display. If the global leaderboard is displayed,
# we may display less than this to fit the leaderboard.
MAX_SCORES = 10

# size of tiles in a map. If you are trying to resize the window, this needs
# to be evaluated.
TILE_WIDTH = 16
TILE_HEIGHT = 16

# Window dimensions
XRES = 800
YRES = 600

# The window may be one size, but the actual map is smaller!
MAP_X = 800 - 576  # 800 is technically supposed to be the screen width
MAP_WIDTH = int(576 / TILE_WIDTH)
MAP_HEIGHT = int(
    600 / TILE_HEIGHT
)  # 600 is technically supposed to be the screen height

# These are used in a ton of places to do the whole 1D-to-2D array thing.
# You should not touch these unless you are doing a major overhaul of some kind.
offX = [1, 0, -1, 0]
offY = [0, 1, 0, -1]

# Amount of items in the shop. This is a fixed array size.
SHOP_AMT = 40


# Character class
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


# Monster type
class MONSTER(Enum):
    NONE = 0
    NONEEITHER = 1
    GNOME = 2
    FATBIRD = 3
    DOLPHIN = 4
    HOTDOG = 5
    REINDEER = 6
    BLUEY = 7


# Guy type. Hate that this is not the same as Monster type. A future coder
# should please do away with Monster type
class GUYS(Enum):
    NONE = 0
    PLAYER = 1
    GNOME = 2
    FATBIRD = 3
    DOLPHIN = 4
    HOTDOG = 5
    REINDEER = 6
    BLUEY = 7


# Not crazy about this, eventually just gave up. Defines the location of the
# image assets
PLAYER_GFX = {
    CLASS.PEASANT: "graphics/peasant.tga",
    CLASS.WARRIOR: "graphics/knight.tga",
    CLASS.THIEF: "graphics/thief.tga",
    CLASS.RANGER: "graphics/ranger.tga",
    CLASS.WIZARD: "graphics/wizard.tga",
    CLASS.GUARD: "graphics/guard.tga",
    CLASS.CHEF: "graphics/chef.tga",
    CLASS.SALESMAN: "graphics/salesman.tga",
    CLASS.DOCTOR: "graphics/doctor.tga",
    CLASS.MULE: "graphics/mule.tga",
}
berserkerGfx = "graphics/knight2.tga"
MONSTER_GFX = {
    GUYS.GNOME: "graphics/gnome.tga",
    GUYS.DOLPHIN: "graphics/dolphin.tga",
    GUYS.REINDEER: "graphics/reindeer.tga",
    GUYS.FATBIRD: "graphics/fatbird.tga",
    GUYS.HOTDOG: "graphics/hotdog.tga",
    GUYS.BLUEY: "graphics/bluey.tga",
}


# Wish this was an enum:string dict like some other items in this file.
# Defines the string name of the class bonus for each class.
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


# Item types!
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


# Item effect. basically "what stat does this effect manipulate?"
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


# First enum made, that's why the case doesn't match elsewhere. Just never
# fixed it.
# Defines what screen to load/logic to use in main loop
class GameState(Enum):
    QUIT = -1
    TITLE = 0
    SHOP = 1
    GAME = 2
    NOTICE = 3


# character stats
# Uses original names. Wish I changed them to be more descriptive.
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


# The sound effects!
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


# Levels
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


# Level names. I like how dicts like this work but for some stupid reason
# they don't all work this way
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
    LEVEL.SHIFT_Q: "A Very Bad Place",
}


# Tile types, used for map generation/movement
class TILE_TYPE(Enum):
    FLOOR = 0
    WALL = 1
    DOOR = 2


# How did we exit the level?
class EXIT_CODE(Enum):
    NONE = 0
    ESCAPED = 2
    DIED = 3
    STARVED = 4


# AI plans, used for both character and monster AI
class PLAN(Enum):
    WANDER = 0
    HUNT = 1
    EXIT = 2


# Don't like this
# Cause of death
class DEATH_CAUSE(Enum):
    NONE = 0
    HUNGER = 1
    MONSTER = 2


# A Notice is a full-screen popup basically. There are three - two for death,
# one for level-up.
# The two death notices can be consolidated
class NOTICE(Enum):
    NONE = 0
    STARVED = 1
    MURDERED = 2
    LEVELUP = 3


# Class names
CLASS_NAME = {
    CLASS.PEASANT: "Peasant",
    CLASS.WARRIOR: "Warrior",
    CLASS.THIEF: "Thief",
    CLASS.RANGER: "Ranger",
    CLASS.WIZARD: "Wizard",
    CLASS.GUARD: "Guard",
    CLASS.CHEF: "Chef",
    CLASS.SALESMAN: "Used Car Salesman",
    CLASS.DOCTOR: "Doctor",
    CLASS.MULE: "Pack Mule",
}

# Death names. Dont like that the key can be two different enum types
DEATH_NAMES = {
    DEATH_CAUSE.HUNGER: "Starvation",
    DEATH_CAUSE.NONE: "DC_NONE",
    GUYS.NONE: "G_NONE",
    GUYS.GNOME: "a Gnome",
    GUYS.FATBIRD: "a Fatbird",
    GUYS.DOLPHIN: "a Dolphin",
    GUYS.HOTDOG: "a Hotdog",
    GUYS.REINDEER: "a Reindeer",
    GUYS.BLUEY: "a Bluey",
}


# Used hither and thither to get the X/Y pixels for a given map location.
# Are you resizing the window? You should look at this
# Also it's here because I had some import loop issues
def get_map_xy(x, y):
    return (
        x * TILE_WIDTH + MAP_X + TILE_WIDTH / 2,
        y * TILE_HEIGHT + TILE_HEIGHT / 2,
    )


# String names of each stat
STAT_NAMES = {
    STAT.STR: "Strength",
    STAT.SPD: "Speed",
    STAT.ACC: "Accuracy",
    STAT.INT: "Intellect",
    STAT.DEF: "Defense",
    STAT.STO: "Stomach",
    STAT.CHA: "Charisma",
    STAT.LIF: "Life",
    STAT.CAR: "Weight",
}

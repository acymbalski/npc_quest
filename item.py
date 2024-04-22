import pygame
from constants import ITEM_EFFECT, ITEM_TYPE, STAT
from utilities import resource_path


class Item:
    def __init__(
        self,
        name: str,
        cost: int,
        weight: int,
        item_type: int,
        value: int,
        effect: int,
        effValue: int,
        effect2: int,
        eff2Value: int,
    ) -> None:
        self.name = name
        self.cost = cost
        self.weight = weight
        self.type = item_type
        self.value = value
        self.effect = effect
        self.effValue = effValue
        self.effect2 = effect2
        self.eff2Value = eff2Value

    def __str__(self) -> str:
        return self.name


# armor
# {"Origami Gi",1,1,ITEM_TYPE.ARMOR,1,ITEM_EFFECT.NONE,0,ITEM_EFFECT.NONE,0},


all_items = [
    # armor
    Item(
        "Origami Gi", 1, 1, ITEM_TYPE.ARMOR, 1, ITEM_EFFECT.NONE, 0, ITEM_EFFECT.NONE, 0
    ),
    Item(
        "Santa Claus Costume",  # name
        4,  # cost
        3,  # weight
        ITEM_TYPE.ARMOR,  # type
        2,  # value
        ITEM_EFFECT.NONE,  # effect
        0,  # effValue
        ITEM_EFFECT.NONE,  # effect2
        0,  # eff2Value
    ),
    Item(
        "Leatherwear",
        12,
        5,
        ITEM_TYPE.ARMOR,
        4,
        ITEM_EFFECT.NONE,
        0,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Heavy Metal T-Shirt",
        30,
        6,
        ITEM_TYPE.ARMOR,
        8,
        ITEM_EFFECT.STOMACH,
        4,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Fuschia Housecoat",
        100,
        4,
        ITEM_TYPE.ARMOR,
        12,
        ITEM_EFFECT.CHARISMA,
        -3,
        ITEM_EFFECT.CARRY,
        10,
    ),
    Item(
        "Technicolor Dreamcoat",
        777,
        15,
        ITEM_TYPE.ARMOR,
        20,
        ITEM_EFFECT.ALL,
        1,
        ITEM_EFFECT.LIFE,
        10,
    ),
    Item(
        "Diving Bell",
        2800,
        20,
        ITEM_TYPE.ARMOR,
        70,
        ITEM_EFFECT.SPEED,
        -3,
        ITEM_EFFECT.LIFE,
        20,
    ),
    Item(
        "Armor Of All",
        4950,
        20,
        ITEM_TYPE.ARMOR,
        80,
        ITEM_EFFECT.ALL,
        2,
        ITEM_EFFECT.LIFE,
        15,
    ),
    # helmets
    Item(
        "Paper Bag", 1, 1, ITEM_TYPE.HELMET, 1, ITEM_EFFECT.NONE, 0, ITEM_EFFECT.NONE, 0
    ),
    Item(
        "Baseball Cap",
        4,
        2,
        ITEM_TYPE.HELMET,
        3,
        ITEM_EFFECT.NONE,
        0,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Gimp Mask",
        8,
        3,
        ITEM_TYPE.HELMET,
        5,
        ITEM_EFFECT.STOMACH,
        3,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Cool Shades",
        16,
        3,
        ITEM_TYPE.HELMET,
        7,
        ITEM_EFFECT.CHARISMA,
        2,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Thinking Cap",
        192,
        3,
        ITEM_TYPE.HELMET,
        13,
        ITEM_EFFECT.IQ,
        6,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Safety Helmet",
        58,
        4,
        ITEM_TYPE.HELMET,
        10,
        ITEM_EFFECT.LIFE,
        2,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Hardhat",
        130,
        4,
        ITEM_TYPE.HELMET,
        20,
        ITEM_EFFECT.LIFE,
        8,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Iron Mask",
        280,
        7,
        ITEM_TYPE.HELMET,
        45,
        ITEM_EFFECT.CHARISMA,
        -1,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Enchanted Helm Of Glip",
        400,
        7,
        ITEM_TYPE.HELMET,
        30,
        ITEM_EFFECT.LIFE,
        10,
        ITEM_EFFECT.STOMACH,
        10,
    ),
    Item(
        "Sun Mask Of Solee",
        3400,
        8,
        ITEM_TYPE.HELMET,
        35,
        ITEM_EFFECT.ALL,
        3,
        ITEM_EFFECT.CHARISMA,
        17,
    ),
    # shields
    Item(
        "Week-Old Pizza",
        1,
        1,
        ITEM_TYPE.SHIELD,
        1,
        ITEM_EFFECT.STOMACH,
        1,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Trash Can Lid",
        2,
        3,
        ITEM_TYPE.SHIELD,
        2,
        ITEM_EFFECT.NONE,
        0,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Wooden Shield",
        4,
        4,
        ITEM_TYPE.SHIELD,
        3,
        ITEM_EFFECT.NONE,
        0,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Iron Shield",
        14,
        6,
        ITEM_TYPE.SHIELD,
        7,
        ITEM_EFFECT.NONE,
        0,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Diamond Shield",
        250,
        8,
        ITEM_TYPE.SHIELD,
        14,
        ITEM_EFFECT.STRENGTH,
        5,
        ITEM_EFFECT.IQ,
        5,
    ),
    Item(
        "Unobtainium Shield",
        999,
        10,
        ITEM_TYPE.SHIELD,
        29,
        ITEM_EFFECT.STRENGTH,
        8,
        ITEM_EFFECT.LIFE,
        10,
    ),
    Item(
        "Supreme Shield W/Cheese",
        4950,
        12,
        ITEM_TYPE.SHIELD,
        35,
        ITEM_EFFECT.ALL,
        2,
        ITEM_EFFECT.LIFE,
        5,
    ),
    # weapons
    Item(
        "Glittering Axe Of Eternity",
        3800,
        10,
        ITEM_TYPE.WEAPON,
        50,
        ITEM_EFFECT.ALL,
        5,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Pointy Stick",
        1,
        1,
        ITEM_TYPE.WEAPON,
        1,
        ITEM_EFFECT.NONE,
        0,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Spatula", 5, 2, ITEM_TYPE.WEAPON, 2, ITEM_EFFECT.NONE, 0, ITEM_EFFECT.NONE, 0
    ),
    Item(
        "Safety Scissors",
        45,
        3,
        ITEM_TYPE.WEAPON,
        4,
        ITEM_EFFECT.NONE,
        0,
        ITEM_EFFECT.LIFE,
        2,
    ),
    Item(
        "Wind Spatula +3",
        70,
        4,
        ITEM_TYPE.WEAPON,
        10,
        ITEM_EFFECT.SPEED,
        3,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Razor Sharp Wit",
        220,
        5,
        ITEM_TYPE.WEAPON,
        20,
        ITEM_EFFECT.ACCURACY,
        5,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Very Large Celery Stalk",
        400,
        7,
        ITEM_TYPE.WEAPON,
        30,
        ITEM_EFFECT.SPEED,
        -2,
        ITEM_EFFECT.STOMACH,
        20,
    ),
    Item(
        "Miracle Whip",
        100,
        4,
        ITEM_TYPE.WEAPON,
        9,
        ITEM_EFFECT.SPEED,
        5,
        ITEM_EFFECT.LIFE,
        3,
    ),
    Item(
        "WoMD",
        9544,
        15,
        ITEM_TYPE.WEAPON,
        100,
        ITEM_EFFECT.ALL,
        50,
        ITEM_EFFECT.CHARISMA,
        -400,
    ),
    # gauntlets
    Item(
        "Polka-Dot Garden Gloves",
        1,
        1,
        ITEM_TYPE.GAUNTLET,
        1,
        ITEM_EFFECT.NONE,
        0,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Latex Gloves",
        5,
        2,
        ITEM_TYPE.GAUNTLET,
        2,
        ITEM_EFFECT.NONE,
        0,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Batting Gloves",
        30,
        3,
        ITEM_TYPE.GAUNTLET,
        4,
        ITEM_EFFECT.LIFE,
        2,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Racing Gloves",
        150,
        3,
        ITEM_TYPE.GAUNTLET,
        8,
        ITEM_EFFECT.SPEED,
        4,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Gauntlets Of Pain",
        300,
        5,
        ITEM_TYPE.GAUNTLET,
        10,
        ITEM_EFFECT.STRENGTH,
        6,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Nifty Gauntlets",
        1900,
        8,
        ITEM_TYPE.GAUNTLET,
        30,
        ITEM_EFFECT.STRENGTH,
        2,
        ITEM_EFFECT.SPEED,
        3,
    ),
    Item(
        "Oven Mitts Of Asbestos",
        5700,
        9,
        ITEM_TYPE.GAUNTLET,
        35,
        ITEM_EFFECT.ALL,
        2,
        ITEM_EFFECT.IQ,
        10,
    ),
    # food
    Item(
        "Ramen Noodles",
        5,
        1,
        ITEM_TYPE.FOOD,
        1,
        ITEM_EFFECT.NONE,
        0,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "McNuggets", 4, 1, ITEM_TYPE.FOOD, 1, ITEM_EFFECT.NONE, 0, ITEM_EFFECT.NONE, 0
    ),
    Item(
        "Soylent Blue",
        8,
        2,
        ITEM_TYPE.FOOD,
        2,
        ITEM_EFFECT.NONE,
        0,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Mac & Cheese",
        10,
        2,
        ITEM_TYPE.FOOD,
        3,
        ITEM_EFFECT.NONE,
        0,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Filet Mignon",
        50,
        3,
        ITEM_TYPE.FOOD,
        10,
        ITEM_EFFECT.NONE,
        0,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Chef's Special",
        200,
        4,
        ITEM_TYPE.FOOD,
        20,
        ITEM_EFFECT.NONE,
        0,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Hungry Man Dinner",
        500,
        5,
        ITEM_TYPE.FOOD,
        70,
        ITEM_EFFECT.NONE,
        0,
        ITEM_EFFECT.NONE,
        0,
    ),
    # potion
    Item(
        "Potion Of Health",
        10,
        1,
        ITEM_TYPE.POTION,
        5,
        ITEM_EFFECT.NONE,
        0,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Potion Of Ginseng",
        40,
        1,
        ITEM_TYPE.POTION,
        10,
        ITEM_EFFECT.NONE,
        0,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Ocean Lotion Potion",
        150,
        1,
        ITEM_TYPE.POTION,
        30,
        ITEM_EFFECT.NONE,
        0,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Emotion Potion",
        200,
        1,
        ITEM_TYPE.POTION,
        50,
        ITEM_EFFECT.NONE,
        0,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Love Potion #9",
        500,
        1,
        ITEM_TYPE.POTION,
        100,
        ITEM_EFFECT.NONE,
        0,
        ITEM_EFFECT.NONE,
        0,
    ),
    # ring
    Item(
        "Ring Of Strength (+1)",
        20,
        1,
        ITEM_TYPE.RING,
        0,
        ITEM_EFFECT.STRENGTH,
        1,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Ring Of Speed (+2)",
        37,
        1,
        ITEM_TYPE.RING,
        0,
        ITEM_EFFECT.SPEED,
        2,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Ring Of Aim (+5)",
        60,
        1,
        ITEM_TYPE.RING,
        0,
        ITEM_EFFECT.ACCURACY,
        5,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Rainbow Ring Of Joy",
        850,
        1,
        ITEM_TYPE.RING,
        0,
        ITEM_EFFECT.ALL,
        2,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Ring Of Uppityness",
        150,
        1,
        ITEM_TYPE.RING,
        0,
        ITEM_EFFECT.CARRY,
        10,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Ring Of Saturn (+4)",
        326,
        1,
        ITEM_TYPE.RING,
        0,
        ITEM_EFFECT.ACCURACY,
        4,
        ITEM_EFFECT.SPEED,
        4,
    ),
    Item(
        "Toilet Bowl Ring (-1)",
        1,
        1,
        ITEM_TYPE.RING,
        0,
        ITEM_EFFECT.ALL,
        -1,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Ring Around The Collar",
        110,
        1,
        ITEM_TYPE.RING,
        0,
        ITEM_EFFECT.CHARISMA,
        -2,
        ITEM_EFFECT.STRENGTH,
        7,
    ),
    Item(
        "Fruit Loop",
        200,
        1,
        ITEM_TYPE.RING,
        0,
        ITEM_EFFECT.STOMACH,
        30,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Ring Of Tummy Power (+8)",
        20,
        1,
        ITEM_TYPE.RING,
        0,
        ITEM_EFFECT.STOMACH,
        8,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Ring Of Life (+4)",
        50,
        1,
        ITEM_TYPE.RING,
        0,
        ITEM_EFFECT.LIFE,
        4,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Ring Of Wisdom (+10)",
        230,
        1,
        ITEM_TYPE.RING,
        0,
        ITEM_EFFECT.IQ,
        10,
        ITEM_EFFECT.NONE,
        0,
    ),
    # amulet
    Item(
        "Amulet Of Speed (+10)",
        250,
        1,
        ITEM_TYPE.AMULET,
        0,
        ITEM_EFFECT.SPEED,
        10,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Amulet Of Strength (+10)",
        250,
        1,
        ITEM_TYPE.AMULET,
        0,
        ITEM_EFFECT.STRENGTH,
        10,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Amulet Of Accuracy (+10)",
        250,
        1,
        ITEM_TYPE.AMULET,
        0,
        ITEM_EFFECT.ACCURACY,
        10,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Amulet Of Omelet (+10)",
        9000,
        1,
        ITEM_TYPE.AMULET,
        0,
        ITEM_EFFECT.ALL,
        10,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Amulet Of Hamlet (+3)",
        3000,
        1,
        ITEM_TYPE.AMULET,
        0,
        ITEM_EFFECT.ALL,
        3,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Amulet Of Health (+10)",
        400,
        1,
        ITEM_TYPE.AMULET,
        0,
        ITEM_EFFECT.LIFE,
        10,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Amulet Of Wisdom (+30)",
        800,
        1,
        ITEM_TYPE.AMULET,
        0,
        ITEM_EFFECT.IQ,
        30,
        ITEM_EFFECT.NONE,
        0,
    ),
    # boots
    Item(
        "Orthopedic Sandals",
        2,
        1,
        ITEM_TYPE.BOOTS,
        1,
        ITEM_EFFECT.NONE,
        0,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Scruffy Boots",
        7,
        2,
        ITEM_TYPE.BOOTS,
        2,
        ITEM_EFFECT.NONE,
        0,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Air Lancelots",
        75,
        3,
        ITEM_TYPE.BOOTS,
        6,
        ITEM_EFFECT.STRENGTH,
        2,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Winged Loafers",
        153,
        4,
        ITEM_TYPE.BOOTS,
        15,
        ITEM_EFFECT.STOMACH,
        10,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "Birkenstockus Maximus",
        420,
        4,
        ITEM_TYPE.BOOTS,
        20,
        ITEM_EFFECT.CHARISMA,
        5,
        ITEM_EFFECT.IQ,
        3,
    ),
    Item(
        "Enchanted Mocassins",
        1840,
        5,
        ITEM_TYPE.BOOTS,
        35,
        ITEM_EFFECT.NONE,
        0,
        ITEM_EFFECT.NONE,
        0,
    ),
    Item(
        "The Shadow Boots Of Elmo",
        3780,
        7,
        ITEM_TYPE.BOOTS,
        40,
        ITEM_EFFECT.ACCURACY,
        3,
        ITEM_EFFECT.LIFE,
        15,
    ),
    Item(
        "Bunny Slippers",
        9400,
        5,
        ITEM_TYPE.BOOTS,
        45,
        ITEM_EFFECT.ALL,
        5,
        ITEM_EFFECT.CHARISMA,
        50,
    ),
]


def calcCost(player, item: Item) -> int:
    cost = item.cost
    cost -= (cost * player.stat[STAT.CHA]) / 500

    if cost < 1:
        cost = 1
    return round(cost)


def calcSell(player, item: Item) -> int:
    cost = item.cost / 2

    cost = (item.cost * player.stat[STAT.CHA]) / 100
    if cost > item.cost:
        cost = item.cost
    if cost < 1:
        cost = 1
    return round(cost)


def calcSwapCost(player, item):
    """
    Calculate the cost of this item... minus any gold to be earned by
    equipping it, depending on the type
    """
    cost_of_new_item = calcCost(player, item)
    cost_of_old_item = 0

    if item.type not in [ITEM_TYPE.POTION, ITEM_TYPE.FOOD, ITEM_TYPE.RING]:
        # can only have one of each type unless it's a potion, food, or ring

        for i in range(20):
            # if we already have one, sell it and equip the new one

            if (
                player.inventory[i] is not None
                and item is not None
                and player.inventory[i].type == item.type
            ):
                cost_of_old_item = calcSell(player, player.inventory[i])
                break
    return cost_of_new_item - cost_of_old_item


def specialEffect(player, effect, amt: int, mult: str):
    if effect == ITEM_EFFECT.ALL:
        for stat in STAT:
            player.stat[stat] += mult * amt
    elif effect == ITEM_EFFECT.STRENGTH:
        player.stat[STAT.STR] += mult * amt
    elif effect == ITEM_EFFECT.DEFENSE:
        player.stat[STAT.DEF] += mult * amt
    elif effect == ITEM_EFFECT.STOMACH:
        player.stat[STAT.STO] += mult * amt
    elif effect == ITEM_EFFECT.SPEED:
        player.stat[STAT.SPD] += mult * amt
    elif effect == ITEM_EFFECT.ACCURACY:
        player.stat[STAT.ACC] += mult * amt
    elif effect == ITEM_EFFECT.CHARISMA:
        player.stat[STAT.CHA] += mult * amt
    elif effect == ITEM_EFFECT.LIFE:
        player.stat[STAT.LIF] += mult * amt
        if player.life > player.stat[STAT.LIF]:
            player.life = player.stat[STAT.LIF]
    elif effect == ITEM_EFFECT.CARRY:
        player.stat[STAT.CAR] += mult * amt
    elif effect == ITEM_EFFECT.IQ:
        player.stat[STAT.INT] += mult * amt


def statChangeFromItem(player, item: Item, mult: str):
    player.totalWeight += mult * item.weight

    if item.type in [ITEM_TYPE.ARMOR, ITEM_TYPE.HELMET, ITEM_TYPE.SHIELD]:
        player.stat[STAT.DEF] += mult * item.value
    elif item.type == ITEM_TYPE.WEAPON:
        player.stat[STAT.STR] += mult * item.value
    elif item.type == ITEM_TYPE.GAUNTLET:
        player.stat[STAT.ACC] += mult * item.value
    elif item.type == ITEM_TYPE.BOOTS:
        player.stat[STAT.SPD] += mult * item.value
    specialEffect(player, item.effect, item.effValue, mult)
    specialEffect(player, item.effect2, item.eff2Value, mult)


def equipItem(player, item: Item):
    if item.type not in [ITEM_TYPE.POTION, ITEM_TYPE.FOOD, ITEM_TYPE.RING]:
        # can only have one of each type unless it's a potion, food, or ring

        for i in range(20):
            # if we already have one, sell it and equip the new one

            if (
                player.inventory[i] is not None
                and item is not None
                and player.inventory[i].type == item.type
            ):
                player.gold += calcSell(player, player.inventory[i])
                statChangeFromItem(player, player.inventory[i], -1)  # unequip item
                player.inventory[i] = item
                statChangeFromItem(player, item, 1)  # equip the new one, and done!
                return
    # otherwise equip it in the first empty slot

    for i in range(20):
        if player.inventory[i] is None:
            statChangeFromItem(player, item, 1)
            player.inventory[i] = item
            return


# fake item equip, for effect calculation


def fakeEquipItem(player, item: Item):
    if item.type in [ITEM_TYPE.POTION, ITEM_TYPE.FOOD, ITEM_TYPE.RING]:
        return  # can have multiples
    else:  # can only have one
        for i in range(20):
            if (
                player.inventory[i] != 255
                and player.inventory[i].item_type == item.item_type
            ):
                player.gold += calcSell(player, player.inventory[i])
                statChangeFromItem(player, player.inventory[i], -1)  # unequip item
                statChangeFromItem(player, item, 1)  # equip the new one, and done!
                return
    for i in range(20):
        if player.inventory[i] == 255:
            statChangeFromItem(player, item, 1)


def netWeightEffect(item: Item) -> int:
    result = item.weight

    if item.effect == ITEM_EFFECT.CARRY:
        result -= item.effValue
    if item.effect2 == ITEM_EFFECT.CARRY:
        result -= item.eff2Value
    return result


def get_item(name: str) -> Item:
    """
    Get the item with the specified name.

    Args:
        name: The name of the item.

    Returns:
        The item with the specified name, or None if not found.
    """
    for i, item in enumerate(all_items):
        if item.name == name:
            return item
    raise Exception(f"Cannot find item '{name}'")


def sortItems(items: list) -> list:
    # sort inventory by item type, then by cost

    items.sort(
        key=lambda item: (
            (item.type.value, item.cost) if item else (float("inf"), float("inf"))
        )
    )
    return items


def getIcon(item):
    # masked_blit(icons,screen2,(item[itm].type-1)*10,0,x,y,10,10);

    icons = pygame.image.load(resource_path("graphics/icons.tga"))

    icon_rect = pygame.Rect((item.type.value - 1) * 10, 0, 10, 10)
    icon_surface = pygame.Surface((10, 10))
    icon_surface.blit(icons, (0, 0), icon_rect)
    icon_surface.set_colorkey((255, 0, 255))  # key out pink for transparancy
    return icon_surface


if __name__ == "__main__":
    import main

    main.main()

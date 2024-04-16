import pygame
from enums import STAT

ITM_FOOD = 1
ITM_POTION = 2
ITM_WEAPON = 3
ITM_ARMOR = 4
ITM_SHIELD = 5
ITM_HELMET = 6
ITM_BOOTS = 7
ITM_GAUNTLET = 8
ITM_RING = 9
ITM_AMULET = 10

EFF_NONE = 0
EFF_ALL = 1  # boost all stats
EFF_STRENGTH = 2
EFF_SPEED = 3
EFF_ACCURACY = 4
EFF_CHARISMA = 5
EFF_CARRY = 6
EFF_DEFENSE = 7
EFF_STOMACH = 8
EFF_LIFE = 9
EFF_IQ = 10


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
# {"Origami Gi",1,1,ITM_ARMOR,1,EFF_NONE,0,EFF_NONE,0},
all_items = [
    # armor
    Item("Origami Gi", 1, 1, ITM_ARMOR, 1, EFF_NONE, 0, EFF_NONE, 0),
    Item("Santa Claus Costume", 4, 3, ITM_ARMOR, 2, EFF_NONE, 0, EFF_NONE, 0),
    Item("Leatherwear", 12, 5, ITM_ARMOR, 4, EFF_NONE, 0, EFF_NONE, 0),
    Item("Heavy Metal T-Shirt", 30, 6, ITM_ARMOR, 8, EFF_STOMACH, 4, EFF_NONE, 0),
    Item("Fuschia Housecoat", 100, 4, ITM_ARMOR, 12, EFF_CHARISMA, -3, EFF_CARRY, 10),
    Item("Technicolor Dreamcoat", 777, 15, ITM_ARMOR, 20, EFF_ALL, 1, EFF_LIFE, 10),
    Item("Diving Bell", 2800, 20, ITM_ARMOR, 70, EFF_SPEED, -3, EFF_LIFE, 20),
    Item("Armor Of All", 4950, 20, ITM_ARMOR, 80, EFF_ALL, 2, EFF_LIFE, 15),
    # helmets
    Item("Paper Bag", 1, 1, ITM_HELMET, 1, EFF_NONE, 0, EFF_NONE, 0),
    Item("Baseball Cap", 4, 2, ITM_HELMET, 3, EFF_NONE, 0, EFF_NONE, 0),
    Item("Gimp Mask", 8, 3, ITM_HELMET, 5, EFF_STOMACH, 3, EFF_NONE, 0),
    Item("Cool Shades", 16, 3, ITM_HELMET, 7, EFF_CHARISMA, 2, EFF_NONE, 0),
    Item("Thinking Cap", 192, 3, ITM_HELMET, 13, EFF_IQ, 6, EFF_NONE, 0),
    Item("Safety Helmet", 58, 4, ITM_HELMET, 10, EFF_LIFE, 2, EFF_NONE, 0),
    Item("Hardhat", 130, 4, ITM_HELMET, 20, EFF_LIFE, 8, EFF_NONE, 0),
    Item("Iron Mask", 280, 7, ITM_HELMET, 45, EFF_CHARISMA, -1, EFF_NONE, 0),
    Item(
        "Enchanted Helm Of Glip", 400, 7, ITM_HELMET, 30, EFF_LIFE, 10, EFF_STOMACH, 10
    ),
    Item("Sun Mask Of Solee", 3400, 8, ITM_HELMET, 35, EFF_ALL, 3, EFF_CHARISMA, 17),
    # shields
    Item("Week-Old Pizza", 1, 1, ITM_SHIELD, 1, EFF_STOMACH, 1, EFF_NONE, 0),
    Item("Trash Can Lid", 2, 3, ITM_SHIELD, 2, EFF_NONE, 0, EFF_NONE, 0),
    Item("Wooden Shield", 4, 4, ITM_SHIELD, 3, EFF_NONE, 0, EFF_NONE, 0),
    Item("Iron Shield", 14, 6, ITM_SHIELD, 7, EFF_NONE, 0, EFF_NONE, 0),
    Item("Diamond Shield", 250, 8, ITM_SHIELD, 14, EFF_STRENGTH, 5, EFF_IQ, 5),
    Item("Unobtainium Shield", 999, 10, ITM_SHIELD, 29, EFF_STRENGTH, 8, EFF_LIFE, 10),
    Item("Supreme Shield W/Cheese", 4950, 12, ITM_SHIELD, 35, EFF_ALL, 2, EFF_LIFE, 5),
    # weapons
    Item(
        "Glittering Axe Of Eternity", 3800, 10, ITM_WEAPON, 50, EFF_ALL, 5, EFF_NONE, 0
    ),
    Item("Pointy Stick", 1, 1, ITM_WEAPON, 1, EFF_NONE, 0, EFF_NONE, 0),
    Item("Spatula", 5, 2, ITM_WEAPON, 2, EFF_NONE, 0, EFF_NONE, 0),
    Item("Safety Scissors", 45, 3, ITM_WEAPON, 4, EFF_NONE, 0, EFF_LIFE, 2),
    Item("Wind Spatula +3", 70, 4, ITM_WEAPON, 10, EFF_SPEED, 3, EFF_NONE, 0),
    Item("Razor Sharp Wit", 220, 5, ITM_WEAPON, 20, EFF_ACCURACY, 5, EFF_NONE, 0),
    Item(
        "Very Large Celery Stalk",
        400,
        7,
        ITM_WEAPON,
        30,
        EFF_SPEED,
        -2,
        EFF_STOMACH,
        20,
    ),
    Item("Miracle Whip", 100, 4, ITM_WEAPON, 9, EFF_SPEED, 5, EFF_LIFE, 3),
    Item("WoMD", 9544, 15, ITM_WEAPON, 100, EFF_ALL, 50, EFF_CHARISMA, -400),
    # gauntlets
    Item("Polka-Dot Garden Gloves", 1, 1, ITM_GAUNTLET, 1, EFF_NONE, 0, EFF_NONE, 0),
    Item("Latex Gloves", 5, 2, ITM_GAUNTLET, 2, EFF_NONE, 0, EFF_NONE, 0),
    Item("Batting Gloves", 30, 3, ITM_GAUNTLET, 4, EFF_LIFE, 2, EFF_NONE, 0),
    Item("Racing Gloves", 150, 3, ITM_GAUNTLET, 8, EFF_SPEED, 4, EFF_NONE, 0),
    Item("Gauntlets Of Pain", 300, 5, ITM_GAUNTLET, 10, EFF_STRENGTH, 6, EFF_NONE, 0),
    Item("Nifty Gauntlets", 1900, 8, ITM_GAUNTLET, 30, EFF_STRENGTH, 2, EFF_SPEED, 3),
    Item("Oven Mitts Of Asbestos", 5700, 9, ITM_GAUNTLET, 35, EFF_ALL, 2, EFF_IQ, 10),
    # food
    Item("Ramen Noodles", 5, 1, ITM_FOOD, 1, EFF_NONE, 0, EFF_NONE, 0),
    Item("McNuggets", 4, 1, ITM_FOOD, 1, EFF_NONE, 0, EFF_NONE, 0),
    Item("Soylent Blue", 8, 2, ITM_FOOD, 2, EFF_NONE, 0, EFF_NONE, 0),
    Item("Mac & Cheese", 10, 2, ITM_FOOD, 3, EFF_NONE, 0, EFF_NONE, 0),
    Item("Filet Mignon", 50, 3, ITM_FOOD, 10, EFF_NONE, 0, EFF_NONE, 0),
    Item("Chef's Special", 200, 4, ITM_FOOD, 20, EFF_NONE, 0, EFF_NONE, 0),
    Item("Hungry Man Dinner", 500, 5, ITM_FOOD, 70, EFF_NONE, 0, EFF_NONE, 0),
    # potion
    Item("Potion Of Health", 10, 1, ITM_POTION, 5, EFF_NONE, 0, EFF_NONE, 0),
    Item("Potion Of Ginseng", 40, 1, ITM_POTION, 10, EFF_NONE, 0, EFF_NONE, 0),
    Item("Ocean Lotion Potion", 150, 1, ITM_POTION, 30, EFF_NONE, 0, EFF_NONE, 0),
    Item("Emotion Potion", 200, 1, ITM_POTION, 50, EFF_NONE, 0, EFF_NONE, 0),
    Item("Love Potion #9", 500, 1, ITM_POTION, 100, EFF_NONE, 0, EFF_NONE, 0),
    # ring
    Item("Ring Of Strength (+1)", 20, 1, ITM_RING, 0, EFF_STRENGTH, 1, EFF_NONE, 0),
    Item("Ring Of Speed (+2)", 37, 1, ITM_RING, 0, EFF_SPEED, 2, EFF_NONE, 0),
    Item("Ring Of Aim (+5)", 60, 1, ITM_RING, 0, EFF_ACCURACY, 5, EFF_NONE, 0),
    Item("Rainbow Ring Of Joy", 850, 1, ITM_RING, 0, EFF_ALL, 2, EFF_NONE, 0),
    Item("Ring Of Uppityness", 150, 1, ITM_RING, 0, EFF_CARRY, 10, EFF_NONE, 0),
    Item("Ring Of Saturn (+4)", 326, 1, ITM_RING, 0, EFF_ACCURACY, 4, EFF_SPEED, 4),
    Item("Toilet Bowl Ring (-1)", 1, 1, ITM_RING, 0, EFF_ALL, -1, EFF_NONE, 0),
    Item(
        "Ring Around The Collar", 110, 1, ITM_RING, 0, EFF_CHARISMA, -2, EFF_STRENGTH, 7
    ),
    Item("Fruit Loop", 200, 1, ITM_RING, 0, EFF_STOMACH, 30, EFF_NONE, 0),
    Item("Ring Of Tummy Power (+8)", 20, 1, ITM_RING, 0, EFF_STOMACH, 8, EFF_NONE, 0),
    Item("Ring Of Life (+4)", 50, 1, ITM_RING, 0, EFF_LIFE, 4, EFF_NONE, 0),
    Item("Ring Of Wisdom (+10)", 230, 1, ITM_RING, 0, EFF_IQ, 10, EFF_NONE, 0),
    # amulet
    Item("Amulet Of Speed (+10)", 250, 1, ITM_AMULET, 0, EFF_SPEED, 10, EFF_NONE, 0),
    Item(
        "Amulet Of Strength (+10)", 250, 1, ITM_AMULET, 0, EFF_STRENGTH, 10, EFF_NONE, 0
    ),
    Item(
        "Amulet Of Accuracy (+10)", 250, 1, ITM_AMULET, 0, EFF_ACCURACY, 10, EFF_NONE, 0
    ),
    Item("Amulet Of Omelet (+10)", 9000, 1, ITM_AMULET, 0, EFF_ALL, 10, EFF_NONE, 0),
    Item("Amulet Of Hamlet (+3)", 3000, 1, ITM_AMULET, 0, EFF_ALL, 3, EFF_NONE, 0),
    Item("Amulet Of Health (+10)", 400, 1, ITM_AMULET, 0, EFF_LIFE, 10, EFF_NONE, 0),
    Item("Amulet Of Wisdom (+30)", 800, 1, ITM_AMULET, 0, EFF_IQ, 30, EFF_NONE, 0),
    # boots
    Item("Orthopedic Sandals", 2, 1, ITM_BOOTS, 1, EFF_NONE, 0, EFF_NONE, 0),
    Item("Scruffy Boots", 7, 2, ITM_BOOTS, 2, EFF_NONE, 0, EFF_NONE, 0),
    Item("Air Lancelots", 75, 3, ITM_BOOTS, 6, EFF_STRENGTH, 2, EFF_NONE, 0),
    Item("Winged Loafers", 153, 4, ITM_BOOTS, 15, EFF_STOMACH, 10, EFF_NONE, 0),
    Item("Birkenstockus Maximus", 420, 4, ITM_BOOTS, 20, EFF_CHARISMA, 5, EFF_IQ, 3),
    Item("Enchanted Mocassins", 1840, 5, ITM_BOOTS, 35, EFF_NONE, 0, EFF_NONE, 0),
    Item(
        "The Shadow Boots Of Elmo",
        3780,
        7,
        ITM_BOOTS,
        40,
        EFF_ACCURACY,
        3,
        EFF_LIFE,
        15,
    ),
    Item("Bunny Slippers", 9400, 5, ITM_BOOTS, 45, EFF_ALL, 5, EFF_CHARISMA, 50),
]


def calcCost(player, item: Item) -> int:
    cost = item.cost
    cost -= (cost * player.stat[STAT.CHA]) / 500

    if cost < 1:
        cost = 1

    return cost


def calcSell(player, item: Item) -> int:
    cost = item.cost / 2

    cost = (item.cost * player.stat[STAT.CHA]) / 100
    if cost > item.cost:
        cost = item.cost

    if cost < 1:
        cost = 1

    return cost


def specialEffect(player, item: Item, amt: int, mult: str):
    if item.type == EFF_ALL:
        for i in range(8):
            player.stat[i] += mult * amt
    elif item.type == EFF_STRENGTH:
        player.stat[STAT.STR] += mult * amt
    elif item.type == EFF_DEFENSE:
        player.stat[STAT.DEF] += mult * amt
    elif item.type == EFF_STOMACH:
        player.stat[STAT.STO] += mult * amt
    elif item.type == EFF_SPEED:
        player.stat[STAT.SPD] += mult * amt
    elif item.type == EFF_ACCURACY:
        player.stat[STAT.ACC] += mult * amt
    elif item.type == EFF_CHARISMA:
        player.stat[STAT.CHA] += mult * amt
    elif item.type == EFF_LIFE:
        player.stat[STAT.LIF] += mult * amt
        if player.life > player.stat[STAT.LIF]:
            player.life = player.stat[STAT.LIF]
    elif item.type == EFF_CARRY:
        player.stat[STAT.CAR] += mult * amt
    elif item.type == EFF_IQ:
        player.stat[STAT.INT] += mult * amt


def statChangeFromItem(player, item: Item, mult: str):
    player.totalWeight += mult * item.weight

    if item.type in [ITM_ARMOR, ITM_HELMET, ITM_SHIELD]:
        player.stat[STAT.DEF] += mult * item.value
    elif item.type == ITM_WEAPON:
        player.stat[STAT.STR] += mult * item.value
    elif item.type == ITM_GAUNTLET:
        player.stat[STAT.ACC] += mult * item.value
    elif item.type == ITM_BOOTS:
        player.stat[STAT.SPD] += mult * item.value

    specialEffect(player, item, item.effValue, mult)
    specialEffect(player, item, item.eff2Value, mult)


def equipItem(player, item: Item):
    if item.type in [ITM_POTION, ITM_FOOD, ITM_RING]:
        return  # can have multiples
    else:  # can only have one
        for i in range(20):
            # if we already have one, sell it and equip the new one
            if (
                player.inventory[i] is not None
                and item is not None
                and player.inventory[i].type == item.type
            ):
                # TODO: implement calcSell
                player.gold += calcSell(player, player.inventory[i])
                statChangeFromItem(player, player.inventory[i], -1)  # unequip item
                player.inventory[i] = item
                statChangeFromItem(player, item, 1)  # equip the new one, and done!
                return

    for i in range(20):
        if player.inventory[i] is None:
            statChangeFromItem(player, item, 1)
            player.inventory[i] = item
            return


# fake item equip, for effect calculation
def fakeEquipItem(player, item: Item):
    if item.type in [ITM_POTION, ITM_FOOD, ITM_RING]:
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

    if item.effect == EFF_CARRY:
        result -= item.effValue
    if item.effects2 == EFF_CARRY:
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
            (item.type, item.cost) if item else (float("inf"), float("inf"))
        )
    )
    return items


def getIcon(item):
    # masked_blit(icons,screen2,(item[itm].type-1)*10,0,x,y,10,10);
    icons = pygame.image.load("graphics/icons.tga")

    icon_rect = pygame.Rect((item.type - 1) * 10, 0, 10, 10)
    icon_surface = pygame.Surface((10, 10))
    icon_surface.blit(icons, (0, 0), icon_rect)
    icon_surface.set_colorkey((255, 0, 255))  # key out pink for transparancy
    return icon_surface


if __name__ == "__main__":
    import main

    main.main()

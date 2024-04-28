import random

import pygame
from combat import chickenOut, zapBadGuys

from constants import (
    CLASS,
    CLASS_NAME,
    classBonus,
    DEATH_CAUSE,
    DEATH_NAMES,
    get_map_xy,
    ITEM_EFFECT,
    ITEM_TYPE,
    NUM_STATS,
    SFX,
    STAT,
)
from display import printMe
from item import getIcon, Item, netWeightEffect, sortItems, statChangeFromItem
from sound import makeSound
from toast import Toast
from utilities import makeUpName


class Character:
    """
    Character class. This class is responsible for storing all the data about
    the player character. This includes stats, inventory, level, etc.

    The character class is also responsible for rendering the character data to
    the screen. That part is rough.

    Because game saves are per-character, a fair bit of "extra" info is stored
    here. Also some other stuff like cause of death, etc. even though the save
    gets wiped on death. Just another write-rewrite quirk.
    """

    def __init__(self, game):
        """
        Initialize the character with default values.
        """

        # default stats
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
        self.game = game

        # total XP so far
        self.xp = 0

        # XP needed to level up
        self.needXP = 10

        # character level
        self.level = 1

        # life points
        self.life = 10

        # gold
        self.gold = 20

        # total weight of items in inventory. This has been reworked a little
        # to be a function (getTotalWeight) instead of a variable. I'm not sure
        # that this value is used anymore.
        self.totalWeight = 0

        # number of items in inventory. Also not used anymore
        self.itemCount = 0

        # food in tummy
        self.food = 50

        # inventory. This is a list of 20 items. If an item is None, that slot
        # is empty. In the original code, empty items hold a value of 255.
        # It would be nice to rework this as a dynamic list but a fair bit
        # of logic was directly translated and depends on this structure.
        self.inventory = [
            None,
        ] * 20

        # points spend on each stat when leveling up. Used to define class.
        # also could use a rework
        self.ptSpend = [0] * NUM_STATS

        # points left to spend in a level up
        self.ptsLeft = 0

        # character class
        self.chrClass = CLASS.PEASANT

        # should we exit the current level? (this shouldn't be here)
        self.shouldExit = False

        # give the character a name! Would be nice to allow this to be updated
        self.name = makeUpName()

        # cause of death. Yikes
        self.deathCause = DEATH_NAMES[DEATH_CAUSE.NONE]

        # not used anymore.
        self.deathHow = 0

        # which save slot is this character in? Used on the title screen and
        # in the save file name
        self.slot = 0

        # score. This is possibly not used? I think the actual score used in
        # the high-score list is based on XP
        self.score = 0

        # don't like this. The knight can go berserk once per level. For some
        # reason I put this here.
        self.goneBerserk = False

        # don't like this either. Once per level, when the character needs food
        # but doesn't have it, they can activate the sound effect for hunger
        self.haveSaidFood = False

        # if the player uses debug commands, we can't upload their score!
        self.online_eligible = True

    def __str__(self):
        """
        For debugging. Render character data to a string.
        """
        return f"Character-> xp: {self.xp}, level: {self.level}, life: {self.life}, gold: {self.gold}, totalWeight: {self.totalWeight}, itemCount: {self.itemCount}, food: {self.food}, inventory: {self.inventory}, ptSpend: {self.ptSpend}, chrClass: {self.chrClass}, shouldExit: {self.shouldExit}, name: {self.name}, deathCause: {self.deathCause}, slot: {self.slot}, score: {self.score}, goneBerserk: {self.goneBerserk}"

    def __getstate__(self):
        """
        Used to exclude some fields from pickling
        """
        state = self.__dict__.copy()

        # Don't pickle game
        del state["game"]
        return state

    def __setstate__(self, state):
        """
        Used to exclude some fields from pickling
        """
        self.__dict__.update(state)
        self.game = None
        # ensure that these fields get re-added upon load!

    def getTotalWeight(self):
        """
        Get the total weight of all items in the player's inventory.
        """
        total = 0
        for item in self.inventory:
            if item:
                total += netWeightEffect(item)
        return total

    def drinkPotion(self):
        """
        Drink a potion. If the player has a potion in their inventory, drink it
        """
        # iterate through inventory
        for i in range(len(self.inventory)):
            item = self.inventory[i]

            # if item is not None
            if item:

                # if item is a potion
                if item.type == ITEM_TYPE.POTION:

                    # Drink potion if:
                    # 1. Drinking the potion would not exceed the player's max life
                    # or 2. The player's life is less than 1/3 of their max life
                    if self.life < self.stat[STAT.LIF] - item.value or self.life < (
                        self.stat[STAT.LIF] / 3
                    ):
                        amount = self.stat[STAT.LIF] - self.life

                        # get player x, y to display toast
                        player_guy = self.game.map.get_player_guy()
                        x, y = get_map_xy(player_guy.x, player_guy.y)
                        self.game.toasts.append(
                            Toast(
                                self.game,
                                str(amount),
                                x,
                                y,
                                color=pygame.Color(0, 255, 0),
                            )
                        )

                        # heal player
                        self.life += amount
                        statChangeFromItem(self, item, -1)
                        self.inventory[i] = None
                        makeSound(SFX.DRINK)

                        # sort inventory
                        self.inventory = sortItems(self.inventory)
                        return

    def foodLeft(self):
        """
        Return True if the player has food in their inventory, False otherwise
        """
        for item in self.inventory:
            if item:
                if item.type == ITEM_TYPE.FOOD:
                    return True
        return False

    def getStatChanges(self, item, to_equip=True):
        """
        Get the stat changes from equipping or un-equipping an item
        """
        strength = 0
        speed = 0
        accuracy = 0
        intellect = 0
        defense = 0
        stomach = 0
        charisma = 0
        life = 0
        weight = 0

        mult = 1
        if not to_equip:
            mult = -1

        # if this item is replacing single-carry items,
        # get the stat changes from un-equiping that item and then apply the new changes
        unequip_stat_changes = {
            STAT.STR: 0,
            STAT.SPD: 0,
            STAT.ACC: 0,
            STAT.INT: 0,
            STAT.DEF: 0,
            STAT.STO: 0,
            STAT.CHA: 0,
            STAT.LIF: 0,
            STAT.CAR: 0,
        }
        if (
            item.type
            not in [
                ITEM_TYPE.POTION,
                ITEM_TYPE.RING,
                ITEM_TYPE.FOOD,
            ]
            and to_equip
        ):  # multi-carry items
            for held_item in self.inventory:
                if held_item:
                    if held_item.type == item.type:
                        unequip_stat_changes = self.getStatChanges(
                            held_item, to_equip=False
                        )
        if item.type in [ITEM_TYPE.ARMOR, ITEM_TYPE.HELMET, ITEM_TYPE.SHIELD]:
            defense += mult * item.value
        elif item.type == ITEM_TYPE.WEAPON:
            strength += mult * item.value
        elif item.type == ITEM_TYPE.GAUNTLET:
            accuracy += mult * item.value
        elif item.type == ITEM_TYPE.BOOTS:
            speed += mult * item.value

        # calculate special effects
        for eff, val in [
            (item.effect, item.effValue),
            (item.effect2, item.eff2Value),
        ]:
            if eff == ITEM_EFFECT.ALL:
                strength += mult * val
                speed += mult * val
                accuracy += mult * val
                intellect += mult * val
                defense += mult * val
                stomach += mult * val
                charisma += mult * val
                life += mult * val
                weight += mult * val
            elif eff == ITEM_EFFECT.STRENGTH:
                strength += mult * val
            elif eff == ITEM_EFFECT.DEFENSE:
                defense += mult * val
            elif eff == ITEM_EFFECT.STOMACH:
                stomach += mult * val
            elif eff == ITEM_EFFECT.SPEED:
                speed += mult * val
            elif eff == ITEM_EFFECT.ACCURACY:
                accuracy += mult * val
            elif eff == ITEM_EFFECT.CHARISMA:
                charisma += mult * val
            elif eff == ITEM_EFFECT.LIFE:
                life += mult * val
            elif eff == ITEM_EFFECT.CARRY:
                weight += mult * val
            elif eff == ITEM_EFFECT.IQ:
                intellect += mult * val
        return {
            STAT.STR: strength + unequip_stat_changes[STAT.STR],
            STAT.SPD: speed + unequip_stat_changes[STAT.SPD],
            STAT.ACC: accuracy + unequip_stat_changes[STAT.ACC],
            STAT.INT: intellect + unequip_stat_changes[STAT.INT],
            STAT.DEF: defense + unequip_stat_changes[STAT.DEF],
            STAT.STO: stomach + unequip_stat_changes[STAT.STO],
            STAT.CHA: charisma + unequip_stat_changes[STAT.CHA],
            STAT.LIF: life + unequip_stat_changes[STAT.LIF],
            STAT.CAR: weight + unequip_stat_changes[STAT.CAR],
        }

    def roomToEquip(self, item: Item) -> bool:
        """
        Return True or False if the player has room to equip an item.
        "Room" means an available slot and enough weight carrying capacity to
        hold it.
        """

        weight = item.weight
        if item.type not in [ITEM_TYPE.POTION, ITEM_TYPE.RING, ITEM_TYPE.FOOD]:

            # iterate over inventory. If we are buying this item by now, it's replacing something we already have
            # so don't double-count the weights
            for held_item in self.inventory:
                if held_item:
                    if held_item.type == item.type:
                        weight -= netWeightEffect(held_item)

        # get weight of all items on player
        if weight + self.getTotalWeight() > self.stat[STAT.CAR]:
            makeSound(SFX.HEAVY)
            return False

        # if we have a full 20 items...
        if len([item for item in self.inventory if item]) == 20:
            makeSound(SFX.HEAVY)
            return False
        return True


def renderCharacterData(game, shop=False, levelUp=False):
    """
    Render character data - stats, name, inventory, etc - to the screen.
    If shop is True, don't render the inventory.
    If levelUp is True, the stats will be rendered as buttons elsewhere. Yikes!
    """
    character = game.player
    printMe(game, character.name, 8, 8)
    printMe(
        game,
        f"Level {character.level} {CLASS_NAME[game.player.chrClass]}",
        8,
        18,
    )
    if not levelUp:

        # levelling up renders these as buttons
        # weirdo formatting trick. Left-align the stat name, pad to 10 characters,
        # then print the stat value. Basically left-aligning the stat name
        # and right-aligning the value
        # my linter is complaining about how I could simply use f-strings
        # but I don't think you actually can for this kind of double-formatting
        printMe(game, "{:<10} {}".format("Strength:", character.stat[STAT.STR]), 8, 28)
        printMe(game, "{:<10} {}".format("Speed:", character.stat[STAT.SPD]), 8, 38)
        printMe(game, "{:<10} {}".format("Accuracy:", character.stat[STAT.ACC]), 8, 48)
        printMe(game, "{:<10} {}".format("Intellect:", character.stat[STAT.INT]), 8, 58)
        printMe(game, "{:<10} {}".format("Defense:", character.stat[STAT.DEF]), 8, 68)
        printMe(game, "{:<10} {}".format("Stomach:", character.stat[STAT.STO]), 8, 78)
        printMe(game, "{:<10} {}".format("Charisma:", character.stat[STAT.CHA]), 8, 88)
    printMe(
        game,
        "{:<10} {}".format("XP needed:", int(character.needXP - character.xp)),
        8,
        108,
    )
    if not levelUp:
        printMe(
            game,
            "{:<10} {}/{}".format("Life:", character.life, character.stat[STAT.LIF]),
            8,
            118,
        )

        printMe(
            game,
            "{:<10} {}/{}".format(
                "Weight:", character.getTotalWeight(), character.stat[STAT.CAR]
            ),
            8,
            128,
        )
    printMe(game, "{:<10} ${}".format("Gold:", character.gold), 8, 138)

    printMe(game, "Inventory", 8, 158)
    if not shop:
        for i in range(20):
            if character.inventory[i]:
                game.screen.blit(getIcon(character.inventory[i]), (8, 178 + i * 10))
                printMe(game, character.inventory[i].name, 18, 178 + i * 10)
            else:
                printMe(game, "......", 8, 178 + i * 10)

    # render special ability, if we have one!
    if character.chrClass != CLASS.PEASANT:
        printMe(game, "Special Ability:", 8, 400)
        printMe(game, classBonus[character.chrClass.value], 20, 410)
    printMe(game, f"Food In Tummy: {int(character.food)}", 8, 580)


def eatFood(game):
    """
    Name is a little misleading. There is a "hunger clock", and when it strikes
    the player takes what I'll call "hunger damage." Basically the food in their
    tummy decreases. But the amount it decreases is based on the their stats.
    If it's decreased enough, we'll need to eat food. That is also handled here.
    """
    player = game.player

    # Wizards may cast Zap! when the hunger clock strikes
    if player.chrClass == CLASS.WIZARD:
        if random.randint(1, 100) < player.level:
            zapBadGuys(game)

    # Used Car Salesmen may Chicken Out
    if player.chrClass == CLASS.SALESMAN:
        if random.randint(1, 100) < player.level:
            chickenOut(game)

    # amount to reduce our food by
    amount = 0

    # sum up all stats except stomach(?)
    for i in range(7):
        amount += player.stat[STAT(i)]
    # subtract Stomach stat, divide by 8, subtract Stomach stat again
    amount = (amount - player.stat[STAT.STO]) / 8 - player.stat[STAT.STO]

    # we always need to eat a little bit
    if amount < 1:
        amount = 1

    # if we have more food in our tummy than is about to be subtracted,
    # we're cool
    if player.food > amount:
        player.food -= amount
        if player.food > 0:
            return  # don't need to eat!
    else:
        # otherwise we've got an empty tum-tum
        player.food = 0

    # eat food
    for i in range(20):
        if player.inventory[i]:
            item = player.inventory[i]

            # eat!
            if item.type == ITEM_TYPE.FOOD:
                statChangeFromItem(player, item, -1)
                player.food += item.value * 100
                player.inventory[i] = None
                makeSound(SFX.EAT)
                player.inventory = sortItems(player.inventory)
                return

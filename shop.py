import random

import pygame
from basics import TextButton
from character import renderCharacterData, statChangeFromItem
from constants import GameState, ITEM_TYPE, LEVEL, LEVELS, SFX, SHOP_AMT, STAT
from display import printMe
from item import (
    all_items,
    calcCost,
    calcSell,
    calcSwapCost,
    equipItem,
    get_item,
    getIcon,
    sortItems,
)
from sound import makeSound
from utilities import resource_path

background_image = pygame.image.load(resource_path("graphics/shop.tga"))


class Shop:
    """
    The Shop!
    Basically a listing of 40 items to the player. Mostly random.
    Prices listed are the "cost" value of the item, but the player will
    actually pay a different amount based on their charisma.
    I don't think the original game showed the listed price as the
    actual, final price, so we won't either.
    """

    def __init__(self, game):
        """
        Initialize the Shop object with a reference to the game object.
        """
        self.game = game
        self.buttons = []
        self.available_items = []

        # fill the shop with items
        self.populateItems()

        max_text_width = 55
        # make buttons for all the items for sale
        for item in self.available_items:
            price_str = f"${item.cost}"
            price_width = max_text_width - len(item.name)
            # format item name to be left alinged with price right aligned
            formatted_item_name = "{: >{}}".format(price_str, price_width)

            item_button = TextButton(
                game,
                item,  # store item as command, this may change someday
                300,
                20 + 10 * len(self.buttons),
                f"{item.name}{formatted_item_name}",
                icon=getIcon(item),
            )

            # items are highlighted red if you can't afford them, green if you
            # can
            item_button.bounding_rect_bg_color = self.getItemHighlightColor(item)
            item_button.bounding_rect_color = None

            self.buttons.append(item_button)

        # add buttons for loading levels
        for i, level in enumerate(LEVEL):
            # don't show Shift Q
            if level == LEVEL.SHIFT_Q:
                continue

            level_button = TextButton(
                game,
                level,
                300,
                20 + 10 * SHOP_AMT + i * 10,
                f"Enter {LEVELS[level]}",
                icon=pygame.Surface((10, 10), pygame.SRCALPHA),  # blank icon
            )
            level_button.setBoundingRectSize(width=450)
            level_button.bounding_rect_bg_color = pygame.Color("GREEN")
            level_button.bounding_rect_color = None
            self.buttons.append(level_button)

        # because players can sell objects, list their inventory as buttons.
        self.setUpInventory()

    def getItemHighlightColor(self, item):
        """
        Return the color to highlight the item with based on the player's gold.
        """
        # if player can afford item, it is highlighted green on mouseover
        if item.cost > self.game.player.gold:
            return pygame.Color("RED")
        return pygame.Color("GREEN")

    def getValidItems(self):
        """
        Return a list of items that can be sold in the shop.
        Items sold in shop:
            - Are not in the players inventory
                - Unless they are Food, Potion, or Rings
            - Are not already listed in the shop
        """
        valid_items = all_items.copy()
        for item in self.game.player.inventory:
            if item in valid_items and item.type not in [
                ITEM_TYPE.POTION,
                ITEM_TYPE.FOOD,
                ITEM_TYPE.RING,
            ]:
                valid_items.remove(item)
        for item in self.available_items:
            if item in valid_items:
                valid_items.remove(item)
        return valid_items

    def populateItems(self):
        """
        Populate the shop with items.
        When you are Level 1, the shop will always include some items:
            - Polka-Dot Garden Gloves
            - Pointy Stick
            - Orthopedic Sandals
        Regardless of your level, the shop wil also always include some items:
            - Potion Of Health
            - Ramen Noodles
        The rest are random based on some validity criteria defined in
        getValidItems.
        """
        # don't like this
        # if we are level 1, we have three pre-populated items
        # this offset lets us fill the shop with the max number of items
        # I can already think of a thousand better ways to do this but I'm tired
        item_count_offset = 2
        # shop at level 1 always includes these
        if self.game.player.level == 1:
            item_count_offset = 5
            self.available_items.append(get_item("Polka-Dot Garden Gloves"))
            self.available_items.append(get_item("Pointy Stick"))
            self.available_items.append(get_item("Orthopedic Sandals"))

        # and we always have these
        self.available_items.append(get_item("Potion Of Health"))
        self.available_items.append(get_item("Ramen Noodles"))

        # populate rest of shop
        for _ in range(SHOP_AMT - item_count_offset):
            # select random valid item
            valid_item = random.choice(self.getValidItems())
            if valid_item:
                self.available_items.append(valid_item)
            # no more valid items? Just give up
            # (note that there are enough items that this should not happen)
            else:
                break

        # sort items
        self.available_items = sortItems(self.available_items)

    def setUpInventory(self):
        """
        Set up the player's inventory as buttons.
        """
        # remove old inventory buttons
        self.buttons = [
            button
            for button in self.buttons
            if button.command.__class__.__name__ != "int"
        ]

        # add buttons for inventory items (to sell)
        for i in range(20):
            item = self.game.player.inventory[i]
            if item:
                item_button = TextButton(
                    self.game,
                    i,  # command
                    8,
                    178 + i * 10,
                    item.name,
                    icon=getIcon(item),
                )
                item_button.bounding_rect = pygame.Rect(
                    item_button.x, item_button.y, 210, 10
                )
                self.buttons.append(item_button)

    def sellItem(self, item_index):
        """
        Sell an item from the player's inventory.
        Remove item from inventory, give gold (based on calcSell), change stats,
        and update the highlights on the items in the shop (because we have
        more gold now).

        This can easily be cleaned up by updating the equipItem function to
        allow unequips.

        """
        # get item from player inventory
        item = self.game.player.inventory[item_index]
        item_cost = calcSell(self.game.player, item)
        # add gold to player
        self.game.player.gold += item_cost
        # unequip item
        # eqiupping is all done in one function but not unequipping.
        # should probably be cleaned up (yikes)
        statChangeFromItem(self.game.player, item, -1)
        # remove item from player inventory
        self.game.player.inventory[item_index] = None

        # gold changed; update button backgrounds and positions
        self.updateItemHighlights()

        # sort player inventory
        self.game.player.inventory = sortItems(self.game.player.inventory)

        self.setUpInventory()
        # play sound effect
        makeSound(SFX.CHACHING)

    def updateItemHighlights(self):
        """
        Update the mouseover highlights on the items in the shop based on the
        player's gold.
        """
        for button in self.buttons:
            # if button.command is an item...
            if button.command.__class__.__name__ == "Item":
                button.bounding_rect_bg_color = self.getItemHighlightColor(
                    button.command
                )
                button.y = 20 + 10 * self.buttons.index(button)
                button.rect.topleft = (button.x, button.y)
                button.bounding_rect.topleft = (button.x, button.y)

    def buyItem(self, button):
        """
        Buy an item from the shop.
        Deduct the cost of the item from the player's gold, add the item to the
        player's inventory, and remove the item from the shop.

        Actually I don't think we remove from the shop. Why is that line there?
        """

        # get item from button
        item = button.command
        # deduct cost of item from gold if affordable
        item_cost = calcCost(self.game.player, item)
        if self.game.player.gold >= item_cost:
            self.game.player.gold -= item_cost
            # add item to player inventory
            # self.game.player.inventory.append(item)
            equipItem(self.game.player, item)
            # remove item from shop
            if item in self.available_items:
                self.available_items.remove(item)

            # gold changed; update button backgrounds and positions
            self.updateItemHighlights()

            # play sound effect
            makeSound(SFX.CHACHING)
            # sort player inventory
            self.game.player.inventory = sortItems(self.game.player.inventory)
            self.setUpInventory()
        else:
            makeSound(SFX.PRICEY)

    def update(self):
        """
        Update the shop screen.
        Draw shop items, character data, handle mouse clicks, etc.
        If the player holds SHIFT and presses Q, load Shift Q.
        If the player holds SHIFT and presses A, give them gold.
        If the player holds SHIFT and presses D, buff some stats.
        QAD.
        """

        screen = self.game.screen

        # Draw the background image
        screen.blit(background_image, (0, 0))

        # Draw player info
        renderCharacterData(self.game, shop=True)
        # get non-None items from player inventory
        inventory_items = len([item for item in self.game.player.inventory if item])
        # draw None inventory items
        for i in range(20 - inventory_items):
            printMe(self.game, "......", 8, 178 + (inventory_items + i) * 10)

        for button in self.buttons:
            button.draw()

        # if SHIFT is held...
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            # and if Q is pressed...
            if keys[pygame.K_q]:
                # load level Shift Q
                self.game.game_state = GameState.GAME
                self.game.level = LEVEL.SHIFT_Q
                self.game.shop = None
                print("Loading Shift Q...")
            # and if A is pressed...
            if keys[pygame.K_a]:
                # give player gold! What the heck!
                # note: because we are looping so much faster than the original game,
                # this is dropped from 100 to 1. We probably still give
                # more cash per second
                self.game.player.gold += 1
                # disallow this character from being uploaded to the leaderboards
                self.game.player.online_eligible = False
                # should we really be updating all the buttons every single time? I dunno
                self.updateItemHighlights()
            if keys[pygame.K_d]:
                # shift-D - major debug mode
                self.game.player.inventory[0] = get_item("Potion Of Health")
                self.game.player.inventory[1] = get_item("Potion Of Health")
                self.game.player.inventory[2] = get_item("Ramen Noodles")
                self.game.player.inventory[3] = get_item("Ramen Noodles")
                self.game.player.inventory[4] = get_item("Ramen Noodles")
                for stat in self.game.player.stat.keys():
                    self.game.player.stat[stat] = 100

                # disallow this character from being uploaded to the leaderboards
                self.game.player.online_eligible = False
                # redraw inventory
                # sort player inventory
                self.game.player.inventory = sortItems(self.game.player.inventory)
                self.setUpInventory()
                makeSound(SFX.HUZZAH)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # check for escape key
                if event.key == pygame.K_ESCAPE:
                    self.game.game_state = GameState.TITLE
                    self.game.reload_global_scores()
                    self.game.shop = None

            # check for left mouse click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                cursor_pos = pygame.mouse.get_pos()
                for _, button in enumerate(self.buttons):
                    if button.bounding_rect.collidepoint(cursor_pos):
                        # if button.command is an "Item" type, buy it
                        if button.command.__class__.__name__ == "Item":
                            # if we can carry it!
                            if self.game.player.roomToEquip(button.command):
                                self.buyItem(button)
                        elif button.command.__class__.__name__ == "int":
                            # sell item
                            self.sellItem(button.command)
                        else:
                            # otherwise, load level
                            self.game.game_state = GameState.GAME
                            self.game.level = button.command
                            # destroy Shop
                            self.game.shop = None

        # check for hover-over-item to display stat changes
        for _, button in enumerate(self.buttons):
            if button.bounding_rect.collidepoint(pygame.mouse.get_pos()):
                # yikes
                if button.command.__class__.__name__ == "Item":
                    item = button.command
                    # calculate stat changes
                    stat_changes = self.game.player.getStatChanges(item)
                    for i in range(len(stat_changes.keys())):
                        stat = list(stat_changes.keys())[i]
                        if stat_changes[stat] == 0:
                            continue
                        # render text
                        prefix = "+" if stat_changes[stat] > 0 else ""

                        color = pygame.Color("GREEN")
                        # if the stat change is a negative, render it in red
                        if stat_changes[stat] < 0:
                            color = pygame.Color("RED")

                        # life and carry capacity are rendered at a different y offset
                        y_offset = 0
                        if stat in [STAT.LIF, STAT.CAR]:
                            y_offset = 20
                        printMe(
                            self.game,
                            f"{prefix}{stat_changes[stat]}",
                            150,
                            28 + i * 10 + y_offset,
                            color=color,
                        )
                    # render gold cost minus sell price of item, if applicable
                    # get the cost of swapping the item
                    # multiply by -1 to properly display that your gold will increase, if true
                    # if negative, we actuall GAIN money from selling. So display
                    # that as a positive number, correctly formatting for the
                    # dollar sign. Ugh
                    cost = calcSwapCost(self.game.player, item)
                    cost_str = f"-${cost}"
                    color = pygame.Color("RED")
                    if cost < 0:
                        color = pygame.Color("GREEN")
                        cost_str = f"+${cost * -1}"
                    printMe(
                        self.game,
                        cost_str,
                        150,
                        138,
                        color=color,
                    )
                elif button.command.__class__.__name__ == "int":
                    # render stat change from selling item
                    item = self.game.player.inventory[button.command]
                    stat_changes = self.game.player.getStatChanges(item, False)
                    for i in range(len(stat_changes.keys())):
                        stat = list(stat_changes.keys())[i]

                        # don't show text for a +0 stat change
                        if stat_changes[stat] == 0:
                            continue

                        # render text
                        prefix = "+" if stat_changes[stat] > 0 else ""

                        # if stat will decrease, color it red. else green
                        color = pygame.Color("GREEN")
                        if stat_changes[stat] < 0:
                            color = pygame.Color("RED")

                        printMe(
                            self.game,
                            f"{prefix}{stat_changes[stat]}",
                            150,
                            28 + i * 10,
                            color=color,
                        )
                    # render gold value of item to sell
                    printMe(
                        self.game,
                        f"+${calcSell(self.game.player, item)}",
                        150,
                        138,
                        color=pygame.Color("GREEN"),
                    )


if __name__ == "__main__":
    import main

    main.main()

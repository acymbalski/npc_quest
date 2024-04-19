import random
import time

import pygame
from basics import TextButton
from character import renderCharacterData
from constants import GameState, ITEM_TYPE, LEVEL, LEVELS, SFX, SHOP_AMT
from display import printMe
from item import all_items, calcSwapCost, equipItem, get_item, getIcon, sortItems
from sound import makeSound

background_image = pygame.image.load("graphics/shop.tga")


class Shop:

    def __init__(self, game):
        self.game = game
        self.buttons = []
        self.available_items = []
        self.populateItems()

        max_text_width = 55
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
                icon=pygame.Surface((10, 10), pygame.SRCALPHA),
            )
            level_button.setBoundingRectSize(width=450)
            level_button.bounding_rect_bg_color = pygame.Color("GREEN")
            level_button.bounding_rect_color = None
            self.buttons.append(level_button)
        self.setUpInventory()

    def getItemHighlightColor(self, item):
        # if player can afford item, it is highlighted green on mouseover
        if item.cost > self.game.player.gold:
            return pygame.Color("RED")
        return pygame.Color("GREEN")

    def getValidItems(self):
        # ensure item is not already in shop
        # ensure item is not in player inventory
        # unless it is a potion, food, or ring
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
        # shop at level 1 always includes these
        if self.game.player.level == 1:
            self.available_items.append(get_item("Polka-Dot Garden Gloves"))
            self.available_items.append(get_item("Pointy Stick"))
            self.available_items.append(get_item("Orthopedic Sandals"))

        # and we always have these
        self.available_items.append(get_item("Potion Of Health"))
        self.available_items.append(get_item("Ramen Noodles"))

        # populate rest of shop
        for _ in range(SHOP_AMT - 5):
            # select random valid item
            valid_item = random.choice(self.getValidItems())
            if valid_item:
                self.available_items.append(valid_item)
            else:
                break

        self.available_items = sortItems(self.available_items)

    def setUpInventory(self):
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
        # get item from player inventory
        item = self.game.player.inventory[item_index]
        # add gold to player
        self.game.player.gold += item.cost
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

        # get item from button
        item = button.command
        # deduct cost of item from gold if affordable
        if self.game.player.gold >= item.cost:
            self.game.player.gold -= item.cost
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

    def update(self):

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
                # give player 10 gold! What the heck!
                # note: because we are looping so much faster than the original game,
                # this is dropped from 100 to 1. We probably still give
                # more cash per second
                self.game.player.gold += 1
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

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # check for escape key
                if event.key == pygame.K_ESCAPE:
                    self.game.game_state = GameState.TITLE
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

                        if stat_changes[stat] < 0:
                            color = pygame.Color("RED")

                        printMe(
                            self.game,
                            f"{prefix}{stat_changes[stat]}",
                            150,
                            28 + i * 10,
                            color=color,
                        )
                    # render gold cost minus sell price of item, if applicable
                    printMe(
                        self.game,
                        f"-${calcSwapCost(self.game.player, item)}",
                        150,
                        138,
                        color=pygame.Color("RED"),
                    )
                elif button.command.__class__.__name__ == "int":
                    # render stat change from selling item
                    item = self.game.player.inventory[button.command]
                    stat_changes = self.game.player.getStatChanges(item, False)
                    for i in range(len(stat_changes.keys())):
                        stat = list(stat_changes.keys())[i]
                        if stat_changes[stat] == 0:
                            continue
                        # render text
                        prefix = "+" if stat_changes[stat] > 0 else ""

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
                        f"+${item.cost}",
                        150,
                        138,
                        color=pygame.Color("GREEN"),
                    )


if __name__ == "__main__":
    import main

    main.main()

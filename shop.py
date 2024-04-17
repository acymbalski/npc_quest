import random

import pygame
from basics import TextButton
from character import renderCharacterData
from constants import GameState, LEVEL, LEVELS, SFX, SHOP_AMT
from item import all_items, equipItem, get_item, getIcon, sortItems
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
                item.ITEM_TYPE_POTION,
                item.ITEM_TYPE_FOOD,
                item.ITEM_TYPE_RING,
            ]:
                valid_items.remove(item)
        for item in self.available_items:
            if item in valid_items:
                valid_items.remove(item)
        return valid_items

    def populateItems(self):
        for _ in range(SHOP_AMT - 5):
            # select random valid item
            valid_item = random.choice(self.getValidItems())
            if valid_item:
                self.available_items.append(valid_item)
            else:
                break

        if self.game.player.level == 1:
            self.available_items.append(get_item("Polka-Dot Garden Gloves"))
            self.available_items.append(get_item("Pointy Stick"))
            self.available_items.append(get_item("Orthopedic Sandals"))

        self.available_items.append(get_item("Potion Of Health"))
        self.available_items.append(get_item("Ramen Noodles"))

        self.available_items = sortItems(self.available_items)

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
            self.available_items.remove(item)

            # gold changed; update button backgrounds and positions
            for button in self.buttons:
                # if button.command is an item...
                if button.command.__class__.__name__ == "Item":
                    button.bounding_rect_bg_color = self.getItemHighlightColor(
                        button.command
                    )
                    button.y = 20 + 10 * self.buttons.index(button)
                    button.rect.topleft = (button.x, button.y)
                    button.bounding_rect.topleft = (button.x, button.y)

            # play sound effect
            makeSound(SFX.CHACHING)

    def update(self):

        screen = self.game.screen

        # Draw the background image
        screen.blit(background_image, (0, 0))

        # Draw player info
        renderCharacterData(self.game)

        for button in self.buttons:
            button.draw()

        for event in pygame.event.get():
            # check for escape key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.game_state = GameState.QUIT

            # check for left mouse click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                cursor_pos = pygame.mouse.get_pos()
                for _, button in enumerate(self.buttons):
                    if button.bounding_rect.collidepoint(cursor_pos):
                        # if button.command is an "Item" type, buy it
                        if button.command.__class__.__name__ == "Item":
                            self.buyItem(button)
                        else:
                            # otherwise, load level
                            self.game.game_state = GameState.GAME
                            self.game.level = button.command
                            # destroy Shop
                            self.game.shop = None


if __name__ == "__main__":
    import main

    main.main()

import pygame
import random
from basics import TextButton
from enums import GameState
from item import all_items, get_item, sortItems

background_image = pygame.image.load("graphics/shop.tga")

LEVELS = [
    "Gnomey Plains",
    "Floofy Woods",
    "The Isle Of Terror",
    "Rocky Dirtville",
    "Lavalava Hot Springs",
    "The Temple Of Spoon",
    "Frosty Hill",
    "Deadly Dungeon",
    "A Weird Place",
    "The Evilness Pit",
]
SHOP_AMT = 40


class Shop:

    def __init__(self, game):
        self.game = game
        self.buttons = []
        self.available_items = []
        self.populateItems()
        print(self.available_items)
        for item in self.available_items:
            print(item)
            self.buttons.append(
                TextButton(
                    game,
                    item.name,
                    312,
                    20 + 10 * len(self.buttons),
                    item,
                )
            )

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
        for _ in range(SHOP_AMT):
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

    def update(self):

        screen = self.game.screen

        # Draw the background image
        screen.blit(background_image, (0, 0))

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
                for i, button in enumerate(self.buttons):
                    if button.bounding_rect.collidepoint(cursor_pos):
                        pass


if __name__ == "__main__":
    import main

    main.main()

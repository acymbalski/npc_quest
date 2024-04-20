import pygame
from basics import TextButton
from character import renderCharacterData
from constants import CLASS, GameState, NOTICE, SFX, STAT, STAT_NAMES
from display import printMe
from hiscore import drawDeathScore
from sound import makeSound
from utilities import resource_path

background_image = pygame.image.load(resource_path("graphics/charsheet.tga"))


class Notice:

    def __init__(self, game):
        self.game = game
        self.buttons = []

        self.charsheet_image = pygame.image.load(
            resource_path("graphics/charsheet.tga")
        )
        self.grave_image = pygame.image.load(resource_path("graphics/grave.tga"))
        self.charsheet_image.set_colorkey((255, 0, 255))
        self.grave_image.set_colorkey((255, 0, 255))

        self.level_up_buttons_initialized = False

    def init_level_up_buttons(self):
        self.level_up_buttons_initialized = True

        self.buttons = []

        # Add buttons for each stat
        # LIF and CAR are drawn a little lower
        for stat in STAT:
            y_pos = 28 + stat.value * 10
            if stat not in [
                STAT.STR,
                STAT.SPD,
                STAT.ACC,
                STAT.INT,
                STAT.DEF,
                STAT.STO,
                STAT.CHA,
            ]:
                y_pos = 48 + stat.value * 10
            text = "{:<10} ({}) {}".format(
                f"{STAT_NAMES[stat]}:",
                self.game.player.ptSpend[stat.value],
                self.game.player.stat[STAT.STR],
            )
            self.buttons.append(
                TextButton(
                    self.game,
                    stat,
                    8,
                    y_pos,
                    text,
                )
            )

        # Inflate button bounding rects to full width
        for button in self.buttons:
            button.setBoundingRectSize(width=210)

    def update(self):

        screen = self.game.screen

        if self.game.noticeType == NOTICE.STARVED:
            # blit(title,screen2,0,0,400-107,30,214,196);
            screen.blit(self.grave_image, (400 - 107, 30))
            printMe(self.game, "YOU STARVED TO DEATH!!", 300, 10)
            printMe(
                self.game,
                "... or rather, the guy you had no direct control over did,",
                150,
                240,
            )
            printMe(self.game, "and it was probably quite frustrating!", 180, 260)
            # renderDeathScore
            drawDeathScore(self.game)
        elif self.game.noticeType == NOTICE.MURDERED:
            # blit(title,screen2,0,0,400-107,30,214,196);
            screen.blit(self.grave_image, (400 - 107, 30))
            printMe(self.game, "YOU WERE MURDALIZED!!", 300, 10)
            printMe(self.game, "Next time, avoid getting hit by the enemies!", 200, 240)
            printMe(self.game, "That should help a lot!", 240, 260)
            # RenderDeathScore();
            drawDeathScore(self.game)
        elif self.game.noticeType == NOTICE.LEVELUP:

            # Draw the background image
            screen.blit(background_image, (0, 0))

            if not self.level_up_buttons_initialized:
                self.init_level_up_buttons()
            # blit(title,screen2,0,0,0,0,224,600);
            screen.blit(self.charsheet_image, (0, 0))
            # c = (mouse_y - 28) / 10
            # RenderLevelUpData(c);
            printMe(self.game, "HOORAY!!  LEVEL UP!!", 400, 200)
            printMe(
                self.game,
                f"{self.game.player.ptsLeft} more points to add to your stats!",
                350,
                240,
            )
            printMe(self.game, "Click on a stat to raise it.", 350, 280)
            renderCharacterData(self.game, levelUp=True)

        for button in self.buttons:
            button.draw()

        for event in pygame.event.get():
            # check for escape key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game.noticeType in [NOTICE.STARVED, NOTICE.MURDERED]:
                        self.game.game_state = GameState.TITLE
                    else:
                        # let the player return to the game without spending all their points, why not?
                        self.returnToGame()

            # check for left mouse click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.game.noticeType in [NOTICE.STARVED, NOTICE.MURDERED]:
                    self.game.game_state = GameState.TITLE
                cursor_pos = pygame.mouse.get_pos()
                for _, button in enumerate(self.buttons):
                    if button.bounding_rect.collidepoint(cursor_pos):
                        # if button clicked was a stat...
                        if button.command.__class__ == STAT:
                            stat = button.command
                            # if there are points left to spend, spend one
                            if self.game.player.ptsLeft > 0:
                                self.game.player.ptSpend[stat.value] += 1
                                self.game.player.ptsLeft -= 1
                                self.game.player.stat[button.command] += 1
                                makeSound(SFX.CHACHING)
                                self.init_level_up_buttons()

                                # re-class player
                                top_stat = 0
                                top_spend = self.game.player.ptSpend[0]

                                for i in range(len(STAT)):
                                    if self.game.player.ptSpend[i] > top_spend:
                                        top_stat = i
                                        top_spend = self.game.player.ptSpend[i]
                                self.game.player.chrClass = CLASS(top_stat + 1)

                            # if there are no points left to spend, remove buttons and return to Shop
                            if self.game.player.ptsLeft == 0:
                                self.returnToGame()
                                break

    def returnToGame(self):
        self.buttons = []
        self.level_up_buttons_initialized = False
        # level-ups happen in-game, so we don't return to shop
        self.game.game_state = GameState.GAME
        self.game.notice = None
        self.game.player.needXP = int(self.game.player.needXP * 2)


if __name__ == "__main__":
    import main

    main.main()

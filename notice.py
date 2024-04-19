import pygame
from basics import TextButton
from constants import GameState, NOTICE, SFX, STAT
from display import printMe
from hiscore import drawDeathScore
from sound import makeSound


class Notice:

    def __init__(self, game):
        self.game = game
        self.buttons = []

        self.charsheet_image = pygame.image.load("graphics/charsheet.tga")
        self.grave_image = pygame.image.load("graphics/grave.tga")
        self.charsheet_image.set_colorkey((255, 0, 255))
        self.grave_image.set_colorkey((255, 0, 255))

        self.level_up_buttons_initialized = False

    def init_level_up_buttons(self):
        self.level_up_buttons_initialized = True

        self.buttons = []

        # Add buttons for each stat
        # LIF and CAR are drawn a little lower
        for stat in STAT:
            y_pos = (28 + stat.value * 10 - 2,)
            if stat not in [
                STAT.STR,
                STAT.SPD,
                STAT.ACC,
                STAT.INT,
                STAT.DEF,
                STAT.STO,
                STAT.CHA,
            ]:
                y_pos = (58 + stat.value * 10 - 2,)
            self.buttons.append(
                TextButton(
                    self.game,
                    stat,
                    6,
                    y_pos,
                    f"{self.game.player.statNames[stat]}: ({self.game.player.ptSpend[stat]}) {self.game.player.stats[stat]}",
                )
            )

        # Inflate button bounding rects to full width
        for button in self.buttons:
            button.setBoundingRectSize(width=268)

    def update(self):

        screen = self.game.screen

        # Draw the background image
        # screen.blit(background_image, (0, 0))

        for button in self.buttons:
            button.draw()

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

        for event in pygame.event.get():
            # check for escape key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.game_state = GameState.QUIT

            # check for left mouse click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.game.noticeType in [NOTICE.STARVED, NOTICE.MURDERED]:
                    self.game.game_state = GameState.TITLE
                cursor_pos = pygame.mouse.get_pos()
                for _, button in enumerate(self.buttons):
                    if button.bounding_rect.collidepoint(cursor_pos):
                        # if button clicked was a stat...
                        print(f"Button clicked: {button.command.__class__}")
                        if button.command.__class__ == STAT:
                            stat = button.command
                            # if there are points left to spend, spend one
                            if self.game.player.ptsLeft > 0:
                                self.game.player.ptSpend[stat] += 1
                                self.game.player.ptsLeft -= 1
                                self.game.player.stats[button.command] += 1
                                makeSound(SFX.CHACHING)
                                self.init_level_up_buttons()

                            # if there are no points left to spend, remove buttons and return to Shop
                            if self.game.player.ptsLeft == 0:
                                self.buttons = []
                                self.level_up_buttons_initialized = False
                                self.game.game_state = GameState.SHOP
                                self.game.notice = None
                                self.game.player.needXP = self.game.player.needXP * 2
                                break


if __name__ == "__main__":
    import main

    main.main()

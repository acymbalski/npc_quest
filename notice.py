import pygame
from constants import GameState, NOTICE
from display import printMe


class Notice:

    def __init__(self, game):
        self.game = game
        self.buttons = []

        self.charsheet_image = pygame.image.load("graphics/charsheet.tga")
        self.grave_image = pygame.image.load("graphics/grave.tga")
        self.charsheet_image.set_colorkey((255, 0, 255))
        self.grave_image.set_colorkey((255, 0, 255))

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
        elif self.game.noticeType == NOTICE.MURDERED:
            # blit(title,screen2,0,0,400-107,30,214,196);
            screen.blit(self.grave_image, (400 - 107, 30))
            printMe(self.game, "YOU WERE MURDALIZED!!", 300, 10)
            printMe(self.game, "Next time, avoid getting hit by the enemies!", 200, 240)
            printMe(self.game, "That should help a lot!", 240, 260)
            # RenderDeathScore();
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
                cursor_pos = pygame.mouse.get_pos()
                for _, button in enumerate(self.buttons):
                    if button.bounding_rect.collidepoint(cursor_pos):
                        pass


if __name__ == "__main__":
    import main

    main.main()

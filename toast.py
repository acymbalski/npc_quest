import pygame
from display import printMe


class Toast:
    def __init__(self, game, text, x, y, duration=120, color=pygame.Color("WHITE")):
        self.game = game
        self.text = text
        self.x = x
        self.y = y
        self.duration = duration
        self.color = color

    def update(self):

        # get rounded y so we can move in smaller increments
        draw_y = round(self.y)

        # draw text shadow
        printMe(
            self.game,
            self.text,
            self.x - 1,
            draw_y - 1,
            pygame.Color("BLACK"),
        )
        printMe(
            self.game,
            self.text,
            self.x + 1,
            draw_y + 1,
            pygame.Color("BLACK"),
        )
        # draw text
        printMe(self.game, self.text, self.x, draw_y, self.color)

        # reduce duration
        self.duration -= 1
        # move up
        self.y -= 0.25

        # remove if duration is 0
        if self.duration == 0:
            self.game.toasts.remove(self)

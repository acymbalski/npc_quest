import pygame
from display import printMe


class Toast:
    """
    Toasts!
    These are the little messages that pop up when you gain or lose life,
    level up, etc.

    They float up the screen and disappear after a while.
    """

    def __init__(self, game, text, x, y, duration=120, color=pygame.Color("WHITE")):
        """
        Initialize the Toast object with a reference to the game object,
        the text to display, the x, y position, and the duration (in ticks)
         to display the text.
        """
        self.game = game
        self.text = text
        self.x = x
        self.y = y
        self.duration = duration
        self.color = color

    def update(self):
        """
        Update the Toast. Draw the text, move up, and reduce duration.
        """

        # get rounded y so we can move in smaller increments
        # i.e. not trying to draw at 0.5 pixels
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

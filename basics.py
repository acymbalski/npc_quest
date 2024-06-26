import pygame


class Button:
    """
    Base class for buttons, should not be used by itself.
    Not truly satisfied with how buttons work but it's okay for now.

    There was the original intention to make clickable text and clickable images
    but it turns out no images needed to be clickable, so ImageButton was never
    completed. Instead, TextButton was used for everything and expanded to allow
    for an icon.

    Other original intentions:
    - Buttons could have a mouseover command and a mouseoff command - should
        be passed as a function or method and automatically called as needed
    - Buttons should have a "command" also as a function or method. This has
        been butchered to just be "anything" and the calling game state
        (Title, Shop, etc) is responsible for checking what type of object
        is stored in there. This drives me nuts but, you know, sometimes you
        just need to move on.
    - Buttons can have a custom-defined bounding rectangle. This was preferred
        to just shrink-wrapping it to the text so you don't have to pad your
        text to be a specific size. In practice most buttons override this
        logic as they are created. Kind of dumb
    - Buttons can have a selection highlight. This is a yellow border around
        the button. It's a bit of a hack to make it work and it's not perfect
        but it's good enough for now.
    """

    def __init__(self, game, command, x, y):
        """
        Initialize the button with a game, a command, and an x, y position.
        """
        self.game = game
        self.command = command
        self.x = x
        self.y = y
        self.bounding_rect = None
        self.bounding_rect_color = pygame.Color("YELLOW")
        self.bounding_rect_buffer = 2
        self.selection_highlight = True
        self.bounding_rect_bg_color = None
        self.mouseon_command = None
        self.mouseoff_command = None

    def mouseover(self):
        """Called when the mouse is over the button."""
        pass

    def mouseclick(self):
        """Called when the button is clicked."""
        pass


class TextButton(Button):
    """
    Button with text and possibly an icon.
    """

    def __init__(
        self,
        game,
        command,
        x,
        y,
        text,
        color=pygame.Color("WHITE"),
        icon=None,
    ):
        super().__init__(game, command, x, y)
        self.font = game.font_8
        self.color = color
        self.icon = icon

        self.setText(str(text))

    def setText(self, text):
        """
        Set the text of the button, render with font, and set bounding rect.
        """
        self.text = text
        self.rendered_text = self.font.render(self.text, True, self.color)
        self.rect = self.rendered_text.get_rect()
        self.rect.topleft = (self.x, self.y)

        # Expand the bounding rectangle by the width of the icon if an icon is present

        if self.icon:
            self.rect.width += self.icon.get_width()
        self.bounding_rect = self.rect

    def setBoundingRectSize(self, width=None, height=None):
        """
        Manually the size of the bounding rect.
        You can use this to make the clickable area larger than the text.
        """
        if width:
            self.bounding_rect.width = width
        if height:
            self.bounding_rect.height = height

    def draw(self):
        """
        Draw the button and check for mouseover. If enabled, draw bounding rect with a buffer.
        """
        # check mouseover

        cursor_pos = pygame.mouse.get_pos()
        if self.bounding_rect and self.bounding_rect.collidepoint(cursor_pos):

            # should we highlight this on mouseover?

            if self.selection_highlight:
                highlight_rect = self.bounding_rect.inflate(
                    self.bounding_rect_buffer, self.bounding_rect_buffer
                )
                # draw highlight edge

                if self.bounding_rect_color:
                    pygame.draw.rect(
                        self.game.screen, self.bounding_rect_color, highlight_rect, 1
                    )
                if self.bounding_rect_bg_color:
                    pygame.draw.rect(
                        self.game.screen, self.bounding_rect_bg_color, highlight_rect
                    )
            self.mouseover()
        text_offset = 0
        # draw the icon

        if self.icon:
            self.game.screen.blit(self.icon, (self.x, self.y))
            text_offset = self.icon.get_width()
        # draw the text

        self.game.screen.blit(self.rendered_text, (self.x + text_offset, self.y))

        # check mouse click within hosting screen, not here


class ImageButton(Button):
    """
    Button with an image.
    """

    def __init__(self, game, command, x, y, image):
        super().__init__(game, command, x, y)
        self.image = image

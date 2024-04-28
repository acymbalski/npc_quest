import pygame


def printMe(
    game,
    text,
    x,
    y,
    color=pygame.Color("WHITE"),
    draw_bounding_box=False,
    bounding_box_width=None,
    bounding_box_height=None,
    bounding_box_color=pygame.Color("YELLOW"),
    buffer=2,
):
    """
    The only thing in this file.
    Print text to the screen at x, y.
    Optionally draw a bounding box around the text if it's hovered over.
    Not even sure that is used anymore. Probably superceded by that
    functionality in the Button class.
    """
    text = game.font_8.render(text, True, color)

    rect = text.get_rect()
    # this is gnarly and could use a cleanup, probably
    # also should be clear that the bounding box is only drawn if the mouse is over the text
    if draw_bounding_box:
        cursor_pos = pygame.mouse.get_pos()
        rect.topleft = (x, y)
        if bounding_box_width:
            rect.width = bounding_box_width
        if bounding_box_height:
            rect.height = bounding_box_height
        buffered_rect = rect.inflate(buffer, buffer)
        if buffered_rect.collidepoint(cursor_pos):
            pygame.draw.rect(game.screen, bounding_box_color, buffered_rect, 1)
    else:
        buffered_rect = rect

    game.screen.blit(text, (x, y))

    return buffered_rect

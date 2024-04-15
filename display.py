import pygame


def printMe(
    screen,
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
    font = pygame.font.Font("font/prstartk.ttf", 8)
    text = font.render(text, True, color)

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
            pygame.draw.rect(screen, bounding_box_color, buffered_rect, 1)
    else:
        buffered_rect = rect

    screen.blit(text, (x, y))

    return buffered_rect


# hate this
def printMeIsClicked(
    screen,
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
    rect = printMe(
        screen,
        text,
        x,
        y,
        color,
        draw_bounding_box,
        bounding_box_width,
        bounding_box_height,
        bounding_box_color,
        buffer,
    )
    cursor_pos = pygame.mouse.get_pos()
    # this is bad. Maybe make a custom clickable object (text/image/whatever) that has some function associated with it
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if rect.collidepoint(cursor_pos):
                return True
    return False

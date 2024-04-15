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

    # this is gnarly and could use a cleanup, probably
    # also should be clear that the bounding box is only drawn if the mouse is over the text
    if draw_bounding_box:
        cursor_pos = pygame.mouse.get_pos()
        rect = text.get_rect()
        rect.topleft = (x, y)
        if rect.collidepoint(cursor_pos):
            print("hello")
            if bounding_box_width:
                rect.width = bounding_box_width
            if bounding_box_height:
                rect.height = bounding_box_height
            buffered_rect = rect.inflate(buffer, buffer)
            pygame.draw.rect(screen, bounding_box_color, buffered_rect, 1)

    screen.blit(text, (x, y))

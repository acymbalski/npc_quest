import pygame

# Initialize Pygame
pygame.init()

# Set up the window dimensions
width = 800
height = 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Title Screen")

# Load the background image
background_image = pygame.image.load("graphics/title.tga")

# Set the user's mouse cursor
cursor_image = pygame.image.load(
    "graphics/cursor.tga"
).convert_alpha()  # Convert the cursor image to a surface


def set_custom_cursor(cursor_surface, hotspot_x, hotspot_y):
    pygame.mouse.set_visible(False)
    cursor_size = cursor_surface.get_size()
    cursor_surface.set_colorkey((255, 0, 255))  # key out pink for transparancy
    cursor_string = pygame.cursors.compile(pygame.surfarray.array2d(cursor_surface))
    cursor_tuple = (
        (cursor_size[0], cursor_size[1]),
        (hotspot_x, hotspot_y),
        cursor_string[0],
        cursor_string[1],
    )
    pygame.mouse.set_cursor(*cursor_tuple)


set_custom_cursor(cursor_image, hotspot_x=0, hotspot_y=0)

# Main game loop
running = True
while running:
    # fill black
    window.fill((0, 0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the background image
    window.blit(background_image, (int(width * 0.025), int(height * 0.05)))

    # Draw the cursor
    mouse_x, mouse_y = pygame.mouse.get_pos()
    window.blit(cursor_image, (mouse_x, mouse_y))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()

import pygame

#---------------------DEFINE COLOUR SCHEME---------------------#
GREEN = pygame.Color("#476930")
LIGHT_GREEN = pygame.Color("#477830")
GREY = pygame.Color("#D3D3D3")


def fill_screen(screen, colour):
    screen.fill(colour)

# Draws a grassy grid on the screen


def draw_grid(screen, grid_columns, grid_rows, grid_size):
    # Fill window with light green to start with (for light green squares)
    screen.fill((LIGHT_GREEN))
    # Initialise Grassy Grid
    for column in range(int(grid_rows)):
        if column % 2 == 0:
            for row in range(int(grid_columns)):
                grid_rect = pygame.Rect(
                    (row * grid_size), (column * grid_size), grid_size, grid_size)
                if (row % 2) == 0:
                    pygame.draw.rect(screen, GREEN, grid_rect)
        else:
            for row in range(int(grid_columns)):
                grid_rect = pygame.Rect(
                    (row * grid_size), (column * grid_size), grid_size, grid_size)
                if (row % 2) != 0:
                    pygame.draw.rect(screen, GREEN, grid_rect)


# Generic text rendering function
def create_text(text_to_write, font_size, x, y, colour=GREY):
    # Define Roboto Font
    roboto_font = pygame.font.Font("fonts/RobotoCondensed-Bold.ttf", font_size)
    # Render text
    text = roboto_font.render(text_to_write, 1, colour)
    text_rect = text.get_rect(center=(x, y))
    return text, text_rect


# ALL CREDIT GOES TO: https://stackoverflow.com/questions/49432109/how-to-wrap-text-in-pygame-using-pygame-font-font
def renderTextCenteredAt(text, fontsize, colour, x, y, screen, allowed_width):
    # first, split the text into words
    words = text.split()

    roboto_font = pygame.font.Font("fonts/RobotoCondensed-Bold.ttf", fontsize)

    # now, construct lines out of these words
    lines = []
    while len(words) > 0:
        # get as many words as will fit within allowed_width
        line_words = []
        while len(words) > 0:
            line_words.append(words.pop(0))
            fw, fh = roboto_font.size(' '.join(line_words + words[:1]))
            if fw > allowed_width:
                break

        # add a line consisting of those words
        line = ' '.join(line_words)
        lines.append(line)

    # now we've split our text into lines that fit into the width, actually
    # render them

    # we'll render each line below the last, so we need to keep track of
    # the cumulative height of the lines we've rendered so far
    y_offset = 0
    for line in lines:
        fw, fh = roboto_font.size(line)

        # (tx, ty) is the top-left of the font surface
        tx = x - fw / 2
        ty = y + y_offset

        font_surface = roboto_font.render(line, True, colour)
        screen.blit(font_surface, (tx, ty))

        y_offset += fh

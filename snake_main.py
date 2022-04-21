# NOTES:
# TO DO:

#-----------------------IMPORTS-----------------------#
from snake_settings import *
import time
import pygame
import sys
import random
from snake_ai_functions.a_star_search import a_star_path
from snake_ai_functions.find_adjacent_nodes import find_adjacent_nodes
from snake_ai_functions.prim_maze import maze
from snake_ai_functions.generate_path import path
from snake_helper_functions.helper import *

#---------------------DEFINE COLOUR SCHEME---------------------#
# Colour Scheme From Design
GREEN = pygame.Color("#476930")
LIGHT_GREEN = pygame.Color("#477830")
BACKGROUND_GREEN = pygame.Color("#47B430")
GREY = pygame.Color("#D3D3D3")
LIGHT_GREY = pygame.Color("#C4C4C4")
MEDIUM_GREY = pygame.Color("#A8A8A8")
DARK_GREY = pygame.Color("#545454")
RED = pygame.Color("#930000")
BLACK = pygame.Color("#000000")


#-----------------------\/ INITIALISATION \/-----------------------#
# Initialise Pygame
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

# Setup Screen
WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The (not quite) Perfect Game Of Snake")
#-----------------------/\ INITIALISATION /\-----------------------#

#---------------------LOAD SOUNDS---------------------#
# All sounds used were royalty free, the following are the links as an acreditation to the authors:
# https://freemusicarchive.org/music/Voodoo_Suite
background_music = pygame.mixer.Sound("sounds/Background_Music.mp3")

# https://mixkit.co/free-sound-effects/forest/
menu_music = pygame.mixer.Sound("sounds/Menu_Music.wav")

# https://www.storyblocks.com/audio/stock/potato-chips-crunch-eating-3-sfkbvefladuk8umg5js.html
apple_eaten_sound = pygame.mixer.Sound("sounds/Eat_Sound.wav")

# https://www.storyblocks.com/audio/stock/mouse-click-computer-hgu7a4t2ivrk0wxxi7h.html
mouse_click_sound = pygame.mixer.Sound("sounds/Mouse_Click.wav")

# https://mixkit.co/free-sound-effects/game/
game_won_sound = pygame.mixer.Sound("sounds/Game_Won_Sound.wav")

# https://mixkit.co/free-sound-effects/game/
game_lost_sound = pygame.mixer.Sound("sounds/Game_Lost_Sound.wav")


#---------------------LOAD IMAGES---------------------#
back_button_image = pygame.transform.scale(
    pygame.image.load('images/BackButton.png'), (100, 75)).convert_alpha()
apple_image = pygame.transform.scale(pygame.image.load(
    'images/Apple.png'), (GRID_SIZE, GRID_SIZE)).convert_alpha()
snake_head_image = pygame.transform.scale(pygame.image.load(
    'images/SnakeHead.png'), (GRID_SIZE, GRID_SIZE)).convert_alpha()
snake_head_dead_image = pygame.transform.scale(pygame.image.load(
    'images/SnakeHeadDead.png'), (GRID_SIZE, GRID_SIZE)).convert_alpha()

#-----------------------\/ CLASSES \/-----------------------#


# Snake Class, defines all the behaviours and attributes that snake needs in the game
class snake():
    # Snake movement directional definitions
    up = [0, -1]
    right = [1, 0]
    left = [-1, 0]
    down = [0, 1]
    current_direction = up

    def __init__(self):
        # Set to 1 so our tail doesn't spawn out of the grid
        head_x = random.randint(1, GRID_WIDTH-1)
        head_y = random.randint(0, GRID_HEIGHT-1)
        self.positions = [[head_x, head_y], [head_x-1, head_y]]

    def draw(self, screen=WINDOW):
        for pos in self.positions:
            snake_block = pygame.Rect(
                (pos[0]*(GRID_SIZE)), (pos[1]*(GRID_SIZE)), GRID_SIZE, GRID_SIZE)
            if pos == self.positions[0]:
                screen.blit(snake_head_image, snake_block)
            else:
                pygame.draw.rect(screen, LIGHT_GREY, snake_block)

    def move(self):
        new_positions = self.positions[:-1]
        new_positions.insert(0, self.addArrays(
            self.positions[0], self.current_direction))
        self.positions = new_positions

    @ staticmethod
    def addArrays(a, b):
        return [(a[0]+b[0]), (a[1]+b[1])]

    def grow(self):
        new_positions = self.positions[:]
        new_positions.insert(-1, self.positions[-1])
        self.positions = new_positions


# Apple Class, defines functions for drawing and randomising the position of the apple
class apple(object):
    def __init__(self):
        self.randomise_pos([])

    def draw(self, screen=WINDOW):
        apple_rect = pygame.Rect((self.x * GRID_SIZE),
                                 (self.y * GRID_SIZE), GRID_SIZE, GRID_SIZE)
        screen.blit(apple_image, apple_rect)

    def randomise_pos(self, snake_body):
        self.x = random.randint(0, (GRID_WIDTH-1))
        self.y = random.randint(0, (GRID_HEIGHT-1))
        # Check if apple has randomised to within the snakes body
        for pos in snake_body:
            if self.x == pos[0] and self.y == pos[1]:
                # Apple is within snake body so randomise again
                self.randomise_pos(snake_body)
        self.position = [self.x, self.y]


# Game Class, handles all the in-game behaviours such as collisions, game over, game labels etc
class game(object):

    def __init__(self, game_label):
        self.snake = snake()
        self.apple = apple()
        self.game_score = 0
        self.moves = 0
        self.game_label = game_label
        self.start_time = time.time()
        self.end_time = 0
        self.outcome = None
        menu_music.stop()
        background_music.play()

    def move_snake(self):
        self.snake.move()

    def update_game(self, screen=WINDOW):
        draw_grid(screen, GRID_WIDTH, GRID_HEIGHT, GRID_SIZE)
        self.display_score()
        self.display_moves()
        self.display_game_label()
        self.snake.draw(screen)
        self.apple.draw(screen)
        self.check_for_game_over()

    def check_collisions(self):
        # If snake has eaten the apple, reposition the apple and add to the body
        if self.snake.positions[0] == self.apple.position:
            # Add an extra block to the snake's body
            apple_eaten_sound.play()
            self.snake.grow()
            self.game_score += 1
            if self.game_score != (GRID_WIDTH*GRID_HEIGHT)-2:
                # Randomise apple position
                self.apple.randomise_pos(self.snake.positions)

            # Otherwise, we've filled up the entire screen and won!
            else:
                print("SNAKE HAS WON")
                self.outcome = "WIN"
                self.end_time = time.time()
                print("SCORE: " + str(self.game_score))
                print("MOVES: " + str(self.moves))
                print("TIME TAKEN: " +
                      str(int(self.end_time-self.start_time)) + " seconds")
                game_won_sound.play()
                self.game_over_screen("WON")

    def display_dead_snake(self, screen=WINDOW):
        clock = pygame.time.Clock()
        for pos in self.snake.positions:
            snake_block = pygame.Rect(
                (pos[0]*(GRID_SIZE)), (pos[1]*(GRID_SIZE)), GRID_SIZE, GRID_SIZE)
            if pos == self.snake.positions[0]:
                screen.blit(snake_head_dead_image, snake_block)
            pygame.display.update()
            clock.tick(500)

    def check_for_game_over(self, screen=WINDOW):
        # If the snake hits itself - game over
        for pos in self.snake.positions[1:]:
            if self.snake.positions[0][0] == pos[0] and self.snake.positions[0][1] == pos[1]:
                print("GAME OVER BY SNAKE")
                self.outcome = "LOSE"
                self.display_dead_snake()
                print("SCORE: " + str(self.game_score))
                print("MOVES: " + str(self.moves))
                self.end_time = time.time()
                game_lost_sound.play()
                self.game_over_screen("LOST")
        # If the snake hits the edge of a border - game over
        if not (0 <= self.snake.positions[0][0] < GRID_WIDTH) or not (0 <= self.snake.positions[0][1] < GRID_HEIGHT):
            print("GAME OVER BY BORDER")
            self.outcome = "LOSE"
            self.end_time = time.time()
            game_lost_sound.play()
            self.game_over_screen("LOST")

    def display_score(self, screen=WINDOW):
        score, score_rect = create_text(
            str("SCORE: " + str(self.game_score)), 20, 45, 20)
        screen.blit(score, score_rect)

    def display_moves(self, screen=WINDOW):
        moves, moves_rect = create_text(
            str("MOVES: " + str(self.moves)), 20, 47.5, 40)
        screen.blit(moves, moves_rect)

    def display_game_label(self, screen=WINDOW):
        # Get the right offset depending on the length of the game label
        offset = 150-(30-len(self.game_label)) * \
            5 if len(self.game_label) > 25 else 85
        game_label, game_label_rect = create_text(
            str(self.game_label), 20, (GRID_SIZE*GRID_WIDTH)-(offset), 20)
        screen.blit(game_label, game_label_rect)

    def game_over_screen(self, outcome, screen=WINDOW):
        background_music.stop()
        clock = pygame.time.Clock()
        fill_screen(screen, GREEN)

        # Game over title
        game_over_label, game_over_label_rect = create_text(
            "GAME OVER", 40, SCREEN_WIDTH/2, (SCREEN_HEIGHT/2)-15)
        screen.blit(game_over_label, game_over_label_rect)

        # Outcome
        outcome_label, outcome_label_rect = create_text(
            str("SNAKE HAS " + outcome), 20, SCREEN_WIDTH/2, (SCREEN_HEIGHT/2)+25)
        screen.blit(outcome_label, outcome_label_rect)

        # Score
        score_label, score_label_rect = create_text(
            str("SCORE: " + str(self.game_score)), 20, SCREEN_WIDTH/2, (SCREEN_HEIGHT/2)+50)
        screen.blit(score_label, score_label_rect)

        # Moves
        moves_label, moves_label_rect = create_text(
            str("MOVES: " + str(self.moves)), 20, SCREEN_WIDTH/2, (SCREEN_HEIGHT/2)+75)
        screen.blit(moves_label, moves_label_rect)

        # Time Taken
        time_label, time_label_rect = create_text(
            str("TIME TAKEN: " + str(int(self.end_time-self.start_time)) + " SECONDS"), 20, SCREEN_WIDTH/2, (SCREEN_HEIGHT/2)+100)
        screen.blit(time_label, time_label_rect)

        # Update Display, pause for reading, then return to the main menu
        pygame.display.update()
        clock.tick(.15)
        main_menu()


# Button Class, handles the creation, style, and behaviour of the settings buttons
class button_rect(object):
    def __init__(self, text,  pos, font_size, background_colour, text_colour):
        self.x, self.y = pos
        self.font = pygame.font.SysFont(
            "fonts/RobotoCondensed-Bold.ttf", font_size)
        self.set_text(text, background_colour, text_colour)

    def set_text(self, text, background_colour, text_colour):
        self.text = self.font.render(text, 1, text_colour)
        self.size = self.text.get_size()
        surface_size = (95, 27)
        self.surface = pygame.Surface(surface_size)
        self.surface.fill(background_colour)
        self.text_rect = self.text.get_rect(
            center=self.surface.get_rect().center)
        self.surface.blit(self.text, self.text_rect)
        self.rect = pygame.Rect(
            self.x, self.y, surface_size[0], surface_size[1])

    def show(self, window=WINDOW):
        window.blit(self.surface, (self.x, self.y))

    def click(self, event, setting, setting_value):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    if setting == "DIFFICULTY":
                        global DIFFICULTY
                        global GRID_SIZE
                        global GRID_WIDTH
                        global GRID_HEIGHT
                        global apple_image
                        global snake_head_image
                        global snake_head_dead_image
                        DIFFICULTY = setting_value
                        GRID_SIZE = DIFFICULTY_DICT[DIFFICULTY]
                        GRID_WIDTH = (SCREEN_WIDTH/GRID_SIZE)
                        GRID_HEIGHT = (SCREEN_HEIGHT/GRID_SIZE)
                        # Reload apple and head image for size of grid
                        apple_image = pygame.transform.scale(pygame.image.load(
                            'images/Apple.png'), (GRID_SIZE, GRID_SIZE)).convert_alpha()
                        snake_head_image = pygame.transform.scale(pygame.image.load(
                            'images/SnakeHead.png'), (GRID_SIZE, GRID_SIZE)).convert_alpha()
                        snake_head_dead_image = pygame.transform.scale(pygame.image.load(
                            'images/SnakeHeadDead.png'), (GRID_SIZE, GRID_SIZE)).convert_alpha()
                    elif setting == "ALGORITHM":
                        global AI_PLAY
                        AI_PLAY = setting_value
                    elif setting == "SPEED":
                        global SPEED
                        global SNAKE_SPEED
                        SPEED = setting_value
                        SNAKE_SPEED = SPEED_DICT[SPEED]

#-----------------------/\ CLASSES /\-----------------------#


#-----------------------\/ CONTROL FLOW FUNCTIONS \/-----------------------#
# Main Menu Screen
def main_menu():
    background_music.stop()
    menu_music.play()

    # Initialise clock object
    clock = pygame.time.Clock()

    # Main Menu Loop
    run = True
    while run:
        # Check for events
        for event in pygame.event.get():
            # Check for exit
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            # Check for mouse clicking
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    try:
                        if manual_play_text_rect.collidepoint(event.pos):
                            print("MANUAL PLAY PRESSED")
                            manual_play()
                        if ai_play_text_rect.collidepoint(event.pos):
                            print("AI PLAY PRESSED")
                            if AI_PLAY == "SIMPLE":
                                ai_play_simple_hamiltonian()
                            elif AI_PLAY == "IMPROVED":
                                ai_play_improved_hamiltonian()
                            elif AI_PLAY == "RISK":
                                ai_play_a_star_risk()
                            else:
                                print("Error, setting not selected")
                        if options_text_rect.collidepoint(event.pos):
                            print("OPTIONS BUTTON PRESSED")
                            options()
                        if more_info_text_rect.collidepoint(event.pos):
                            print("MORE INFO BUTTON PRESSED")
                            more_info()
                    except:
                        print("Buttons haven't loaded yet...")
                        pass

        # Fill Background
        fill_screen(WINDOW, GREEN)

        # Draw Side Line
        line_x = ((SCREEN_WIDTH/2)-65)
        line_y = ((SCREEN_HEIGHT/2)-50)
        pygame.draw.line(WINDOW, GREY, (line_x, line_y),
                         (line_x, line_y+160), 2)

        # Draw Text

        # Title Text
        snake_text, snake_text_rect = create_text(
            "SNAKE", 40, (SCREEN_WIDTH/2), (SCREEN_HEIGHT/4))
        WINDOW.blit(snake_text, snake_text_rect)

        # Manual Play Button
        manual_play_text, manual_play_text_rect = create_text(
            "Manual Play", 20, (SCREEN_WIDTH/2), (SCREEN_HEIGHT/2.5)+35)
        manual_play_text_rect.left = line_x+25
        WINDOW.blit(manual_play_text, manual_play_text_rect)

        # AI Play Button
        ai_play_text, ai_play_text_rect = create_text(
            "AI Play", 20, (SCREEN_WIDTH/2), (SCREEN_HEIGHT/2.5)+70)
        ai_play_text_rect.left = line_x+25
        WINDOW.blit(ai_play_text, ai_play_text_rect)

        # Options Button
        options_text, options_text_rect = create_text(
            "Options", 20, (SCREEN_WIDTH/2), (SCREEN_HEIGHT/2.5)+105)
        options_text_rect.left = line_x+25
        WINDOW.blit(options_text, options_text_rect)

        # More Info Button
        more_info_text, more_info_text_rect = create_text(
            "More Info", 20, (SCREEN_WIDTH/2), (SCREEN_HEIGHT/2.5)+140)
        more_info_text_rect.left = line_x+25
        WINDOW.blit(more_info_text, more_info_text_rect)

        clock.tick(FPS)
        pygame.display.update()


# Options Screen
def options():
    # Initialise clock object
    clock = pygame.time.Clock()

    # Difficulty Buttons
    easy_button = button_rect(
        "EASY", (225, (SCREEN_HEIGHT/4)+27), 25, GREY, BLACK)
    medium_button = button_rect(
        "MEDIUM", (350, (SCREEN_HEIGHT/4)+27), 25, GREY, BLACK)
    hard_button = button_rect(
        "HARD", (475, (SCREEN_HEIGHT/4)+27), 25, GREY, BLACK)

    # AI Algorithm Selection Buttons
    simple_button = button_rect(
        "SIMPLE", (225, (SCREEN_HEIGHT/4)+107), 25, GREY, BLACK)
    improved_button = button_rect(
        "IMPROVED", (350, (SCREEN_HEIGHT/4)+107), 20, GREY, BLACK)
    a_star_risk_button = button_rect(
        "RISK", (475, (SCREEN_HEIGHT/4)+107), 25, GREY, BLACK)

    # Speed Buttons
    slow_speed_button = button_rect(
        "SLOW", (225, (SCREEN_HEIGHT/4)+187), 25, GREY, BLACK)
    medium_speed_button = button_rect(
        "MEDIUM", (350, (SCREEN_HEIGHT/4)+187), 25, GREY, BLACK)
    fast_speed_button = button_rect(
        "FAST", (475, (SCREEN_HEIGHT/4)+187), 25, GREY, BLACK)

    # Main Menu Loop
    run = True
    while run:
        # Set currently selected options
        # DIFFICULTY
        if DIFFICULTY == "EASY":
            easy_button.set_text("EASY", DARK_GREY, GREY)
            medium_button.set_text("MEDIUM", GREY, BLACK)
            hard_button.set_text("HARD", GREY, BLACK)
        elif DIFFICULTY == "MEDIUM":
            easy_button.set_text("EASY", GREY, BLACK)
            medium_button.set_text("MEDIUM", DARK_GREY, GREY)
            hard_button.set_text("HARD", GREY, BLACK)
        elif DIFFICULTY == "HARD":
            easy_button.set_text("EASY", GREY, BLACK)
            medium_button.set_text("MEDIUM", GREY, BLACK)
            hard_button.set_text("HARD", DARK_GREY, GREY)
        # ALGORITHM
        if AI_PLAY == "SIMPLE":
            simple_button.set_text("SIMPLE", DARK_GREY, GREY)
            improved_button.set_text("IMPROVED", GREY, BLACK)
            a_star_risk_button.set_text("RISK", GREY, BLACK)
        elif AI_PLAY == "IMPROVED":
            simple_button.set_text("SIMPLE", GREY, BLACK)
            improved_button.set_text("IMPROVED", DARK_GREY, GREY)
            a_star_risk_button.set_text("RISK", GREY, BLACK)
        elif AI_PLAY == "RISK":
            simple_button.set_text("SIMPLE", GREY, BLACK)
            improved_button.set_text("IMPROVED", GREY, BLACK)
            a_star_risk_button.set_text("RISK", DARK_GREY, GREY)
        # SPEED
        if SPEED == "SLOW":
            slow_speed_button.set_text("SLOW", DARK_GREY, GREY)
            medium_speed_button.set_text("MEDIUM", GREY, BLACK)
            fast_speed_button.set_text("FAST", GREY, BLACK)
        elif SPEED == "MEDIUM":
            slow_speed_button.set_text("SLOW", GREY, BLACK)
            medium_speed_button.set_text("MEDIUM", DARK_GREY, GREY)
            fast_speed_button.set_text("FAST", GREY, BLACK)
        elif SPEED == "FAST":
            slow_speed_button.set_text("SLOW", GREY, BLACK)
            medium_speed_button.set_text("MEDIUM", GREY, BLACK)
            fast_speed_button.set_text("FAST", DARK_GREY, GREY)

        # Check for events
        for event in pygame.event.get():
            # Check for exit
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            # Check for mouse clicking
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if back_button_image.get_rect().collidepoint(event.pos):
                        main_menu()

            # Difficulty Button Clicked
            easy_button.click(event, "DIFFICULTY", "EASY")
            medium_button.click(event, "DIFFICULTY", "MEDIUM")
            hard_button.click(event, "DIFFICULTY", "HARD")

            # Algorithm Button Clicked
            simple_button.click(event, "ALGORITHM", "SIMPLE")
            improved_button.click(event, "ALGORITHM", "IMPROVED")
            a_star_risk_button.click(event, "ALGORITHM", "RISK")

            # Speed Button Clicked
            slow_speed_button.click(event, "SPEED", "SLOW")
            medium_speed_button.click(event, "SPEED", "MEDIUM")
            fast_speed_button.click(event, "SPEED", "FAST")

        # Fill Background
        fill_screen(WINDOW, GREEN)

        # Draw Side Line
        line_x = (50)
        line_y = (SCREEN_HEIGHT/8)+75
        pygame.draw.line(WINDOW, GREY, (line_x, line_y),
                         (line_x, line_y+(SCREEN_HEIGHT-(SCREEN_HEIGHT/2)-50)), 2)

        # Draw Back Button
        back_button_x = 50
        back_button_y = 35
        WINDOW.blit(back_button_image, (back_button_x, back_button_y))

        # Draw Text
        # Title Text
        snake_text, snake_text_rect = create_text(
            "OPTIONS    ", 40, (SCREEN_WIDTH/2), (SCREEN_HEIGHT/8))
        WINDOW.blit(snake_text, snake_text_rect)

        # Difficulty Text
        snake_text, snake_text_rect = create_text(
            "Difficulty:", 20, (SCREEN_WIDTH/4), (SCREEN_HEIGHT/4) + 40)
        WINDOW.blit(snake_text, snake_text_rect)

        # AI Option Text
        snake_text, snake_text_rect = create_text(
            "AI Algorithm:", 20, (SCREEN_WIDTH/4), (SCREEN_HEIGHT/4) + 120)
        WINDOW.blit(snake_text, snake_text_rect)

        # Speed Option Text
        snake_text, snake_text_rect = create_text(
            "Snake Speed:", 20, (SCREEN_WIDTH/4), (SCREEN_HEIGHT/4) + 200)
        WINDOW.blit(snake_text, snake_text_rect)

        # Show Difficulty Buttons
        easy_button.show()
        medium_button.show()
        hard_button.show()

        # Show AI Algorithm Selection Buttons
        simple_button.show()
        improved_button.show()
        a_star_risk_button.show()

        # Show Speed Buttons
        slow_speed_button.show()
        medium_speed_button.show()
        fast_speed_button.show()

        clock.tick(FPS)
        pygame.display.update()


# More Information Screen
def more_info():
    # Initialise clock object
    clock = pygame.time.Clock()
    # Main Menu Loop
    run = True
    while run:
        # Check for events
        for event in pygame.event.get():
            # Check for exit
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            # Check for mouse clicking
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if back_button_image.get_rect().collidepoint(event.pos):
                        main_menu()

        # Fill Background
        fill_screen(WINDOW, GREEN)

        # Draw Side Line
        line_x = (25)
        line_y = (SCREEN_HEIGHT/8)+50
        pygame.draw.line(WINDOW, GREY, (line_x, line_y),
                         (line_x, line_y+(SCREEN_HEIGHT-(SCREEN_HEIGHT/4)-50)), 2)

        # Draw Back Button
        back_button_x = 50
        back_button_y = 35
        WINDOW.blit(back_button_image, (back_button_x, back_button_y))

        # Draw Text

        # Title Text
        snake_text, snake_text_rect = create_text(
            "INFORMATION", 40, (SCREEN_WIDTH/2), (SCREEN_HEIGHT/8))
        WINDOW.blit(snake_text, snake_text_rect)

        # Informational Text
        renderTextCenteredAt("This game of snake is the work for a final year project at the University of Liverpool and has been created by the student Joe Moore. The game can be played manually by the player or a specially designed AI algorithm can play the “perfect” game for you. The difficulty can be increased or decreased by increasing or decreasing the size of the board in the options menu.",
                             30, GREY, (SCREEN_WIDTH/2), (SCREEN_HEIGHT/8)+75, WINDOW, SCREEN_WIDTH-100)

        clock.tick(FPS)
        pygame.display.update()


# Manual Play Game
def manual_play():
    # Initialise game class for manual play
    manual_play_game = game("MANUAL PLAY")

    # Initialise clock object
    clock = pygame.time.Clock()

    # Main game loop
    run = True
    keydown = False
    while run:
        for event in pygame.event.get():
            # Listen for exit
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            # Listen for user keystrokes to control the snake
            if event.type == pygame.KEYDOWN and not keydown:
                keydown = True
                manual_play_game.moves += 1
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and (manual_play_game.snake.current_direction != manual_play_game.snake.right):
                    manual_play_game.snake.current_direction = manual_play_game.snake.left
                if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and (manual_play_game.snake.current_direction != manual_play_game.snake.left):
                    manual_play_game.snake.current_direction = manual_play_game.snake.right
                if (event.key == pygame.K_UP or event.key == pygame.K_w) and (manual_play_game.snake.current_direction != manual_play_game.snake.down):
                    manual_play_game.snake.current_direction = manual_play_game.snake.up
                if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and (manual_play_game.snake.current_direction != manual_play_game.snake.up):
                    manual_play_game.snake.current_direction = manual_play_game.snake.down

        # Update the visuals
        manual_play_game.update_game()
        manual_play_game.move_snake()
        keydown = False
        manual_play_game.check_collisions()  # Check for any collisions
        pygame.display.update()
        clock.tick(FPS)
        # Half the speed for manual play to make it actually playable
        clock.tick(SNAKE_SPEED/2)

#-----------------------/\ CONTROL FLOW FUNCTIONS /\-----------------------#


#-----------------------\/ AI PLAY FUNCTIONS \/-----------------------#
# Simple Hamiltonian AI Play (PERFECT) - Follows a randomly generated hamiltonian path so that the snake never dies
def ai_play_simple_hamiltonian():
    # Initialise the maze and the path the snake is going to follow
    maze_object = maze(GRID_HEIGHT/2, GRID_WIDTH/2)
    prim_maze = maze_object.generate_prim_maze()
    path_object = path(GRID_HEIGHT, GRID_WIDTH)
    maze_path = path_object.generate_path(prim_maze)

    # Initialise game class for Simple Hamiltonian
    ai_play_game = game("AI PLAY - SIMPLE HAMILTONIAN")

    # Get the initial position of the snake
    snake_position = (
        ai_play_game.snake.positions[0][0], ai_play_game.snake.positions[0][1])

    # Get the index of the path to start at
    path_position = maze_path.index(snake_position)

    # Initialise clock object
    clock = pygame.time.Clock()

    # Main game loop
    run = True
    while run:
        for event in pygame.event.get():
            # Listen for exit
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

        # If we're not at the end of our path index
        if path_position < (len(maze_path)-1):
            pass
        # If we are, "reset" the index
        else:
            path_position = -1

        # PATH DIRECTION DEFINITIONS
        path_right = (maze_path[path_position+1] ==
                      (snake_position[0] + 1, snake_position[1]))
        path_left = (maze_path[path_position+1] ==
                     (snake_position[0] - 1, snake_position[1]))
        path_up = (maze_path[path_position+1] ==
                   (snake_position[0], snake_position[1] - 1))
        path_down = (maze_path[path_position+1] ==
                     (snake_position[0], snake_position[1] + 1))

        # Define directions before move, so that we can check if the AI has "pressed a key" in the traditional sense
        direction_before_move = ai_play_game.snake.current_direction

        # Determine which direction to move depending on where we are on the path
        if path_position < (len(maze_path)-1):
            if path_right:
                ai_play_game.snake.current_direction = ai_play_game.snake.right
                snake_position = (
                    snake_position[0]+1, snake_position[1])
                direction_after_move = ai_play_game.snake.right
            elif path_left:
                ai_play_game.snake.current_direction = ai_play_game.snake.left
                snake_position = (
                    snake_position[0]-1, snake_position[1])
                direction_after_move = ai_play_game.snake.left
            elif path_up:
                ai_play_game.snake.current_direction = ai_play_game.snake.up
                snake_position = (
                    snake_position[0], snake_position[1]-1)
                direction_after_move = ai_play_game.snake.up
            elif path_down:
                ai_play_game.snake.current_direction = ai_play_game.snake.down
                snake_position = (
                    snake_position[0], snake_position[1]+1)
                direction_after_move = ai_play_game.snake.down
            path_position += 1

        if (direction_after_move != direction_before_move):
            ai_play_game.moves += 1

        # Move the snake and check for collisions
        ai_play_game.move_snake()
        ai_play_game.check_collisions()

        # Update the visuals
        ai_play_game.update_game()
        pygame.display.update()
        clock.tick(FPS)
        clock.tick(SNAKE_SPEED)


# Improved Hamiltonian AI Play (PERFECT) - Builds on the simple hamiltonian by adding "safe" shortcutting where possible
def ai_play_improved_hamiltonian():
    # Initialise the maze and the path the snake is going to follow
    maze_object = maze(GRID_HEIGHT/2, GRID_WIDTH/2)
    prim_maze = maze_object.generate_prim_maze()
    path_object = path(GRID_HEIGHT, GRID_WIDTH)
    maze_path = path_object.generate_path(prim_maze)

    # Initialise game class for Improved Hamiltonian
    ai_play_game = game("AI PLAY - IMPROVED HAMILTONIAN")

    # Get the initial position of the snake
    snake_position = (
        ai_play_game.snake.positions[0][0], ai_play_game.snake.positions[0][1])

    # Get the index of the path to start at
    path_position = maze_path.index(snake_position)

    # Initialise shortcut repeat list
    shortcuts_taken = []
    shortcut_cooldown = 0

    # Initialise clock object
    clock = pygame.time.Clock()

    # Main game loop
    run = True
    while run:
        for event in pygame.event.get():
            # Listen for exit
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

        # Get % of the board the snake is filling, if we're at 50%, don't try to take anymore shortcuts
        snake_percent = (len(ai_play_game.snake.positions) /
                         (GRID_WIDTH*GRID_HEIGHT))*100
        # Get position of the apple
        apple_position = ai_play_game.apple.position
        # Get position of the head
        snake_head_position = ai_play_game.snake.positions[0]
        # Get position of the tail
        snake_tail_position = ai_play_game.snake.positions[-1]

        # Get the index of the snake's head and the snakes tail in the maze path
        snake_tail_index = maze_path.index(
            (snake_tail_position[0], snake_tail_position[1]))
        snake_head_index = maze_path.index(
            (snake_head_position[0], snake_head_position[1]))

        # Search for adjacent nodes to the head
        adjacent_nodes = find_adjacent_nodes(
            snake_head_position, GRID_HEIGHT, GRID_WIDTH, ai_play_game.snake.positions)

        # If we can take a shortcut, get the shortest path from the head to the apple
        if shortcut_cooldown == 0 and snake_percent < 50:
            shortest_path = a_star_path(
                snake_head_position, apple_position, GRID_WIDTH, GRID_HEIGHT, ai_play_game.snake.positions)

        # Reduce the shortcut cooldown if we're in one
        if shortcut_cooldown > 0:
            shortcut_cooldown -= 1
            print(shortcut_cooldown)

        # Check we were able to find a path and we're allowed to take a shortcut (shortcut cooldown and snake length)
        if shortest_path != None and len(shortest_path) > 1 and shortcut_cooldown == 0 and snake_percent < 50:
            # If there is an adjacent node in the shortest path
            for node in adjacent_nodes:
                if node == shortest_path[1]:
                    # Get information about the shortcut to potentially store
                    shortcut_info = [snake_head_index, snake_tail_index, len(
                        ai_play_game.snake.positions)]
                    # Check if the shortcut node is in the indexes inbetween where the head and the tail are
                    if snake_head_index > snake_tail_index:
                        non_elligble_range = maze_path[snake_tail_index:snake_head_index]
                    else:
                        non_elligble_range = maze_path[snake_tail_index:] + \
                            maze_path[:snake_head_index]

                    # If the adjacent node isn't inbetween the head and tail index and we've not already tried this shortcut before then try to take the shortcut
                    if ((node[0], node[1]) not in non_elligble_range) and (shortcut_info not in shortcuts_taken):
                        # Store shortcut info so we don't end up in a loop
                        shortcuts_taken.append(shortcut_info)
                        # Check that we're not overtaking the apple in the path in our shortcut
                        # If not, then set path position to 1 before the node we want to shortcut to
                        if maze_path.index((node[0], node[1]))-1 < maze_path.index((ai_play_game.apple.position[0], ai_play_game.apple.position[1])):
                            path_position = maze_path.index(
                                (node[0], node[1]))-1

                    # Otherwise we're either in the non elligble range (so just carry on the path)...
                    elif (node[0], node[1]) in non_elligble_range:
                        print(
                            "NODE " + str(node) + " IS IN NON ELLIGIBLE RANGE OF " + str(non_elligble_range))
                    # Or we're attempting a shortcut we've already tried, in which case initiate shortcut cooldown period
                    elif shortcut_info in shortcuts_taken:
                        print("shortcut_info is: " + str(shortcut_info))
                        print("shortcuts taken are: " +
                              str(shortcuts_taken))
                        print("\n Already taken this shortcut, cooling down...")
                        shortcut_cooldown = int(5000/GRID_SIZE)

        # If we're not at the end of our path index
        if path_position < (len(maze_path)-1):
            pass
        # If we are, "reset" the index
        else:
            path_position = -1

        # PATH DIRECTION DEFINITIONS
        path_right = (maze_path[path_position+1] ==
                      (snake_position[0] + 1, snake_position[1]))
        path_left = (maze_path[path_position+1] ==
                     (snake_position[0] - 1, snake_position[1]))
        path_up = (maze_path[path_position+1] ==
                   (snake_position[0], snake_position[1] - 1))
        path_down = (maze_path[path_position+1] ==
                     (snake_position[0], snake_position[1] + 1))

        # Define directions before move, so that we can check if the AI has "pressed a key" in the traditional sense
        direction_before_move = ai_play_game.snake.current_direction
        direction_after_move = ai_play_game.snake.current_direction

        # Determine which direction to move depending on where we are on the path
        if path_position < (len(maze_path)-1):
            if path_right:
                ai_play_game.snake.current_direction = ai_play_game.snake.right
                snake_position = (
                    snake_position[0]+1, snake_position[1])
                direction_after_move = ai_play_game.snake.right
            elif path_left:
                ai_play_game.snake.current_direction = ai_play_game.snake.left
                snake_position = (
                    snake_position[0]-1, snake_position[1])
                direction_after_move = ai_play_game.snake.left
            elif path_up:
                ai_play_game.snake.current_direction = ai_play_game.snake.up
                snake_position = (
                    snake_position[0], snake_position[1]-1)
                direction_after_move = ai_play_game.snake.up
            elif path_down:
                ai_play_game.snake.current_direction = ai_play_game.snake.down
                snake_position = (
                    snake_position[0], snake_position[1]+1)
                direction_after_move = ai_play_game.snake.down
            path_position += 1

        if (direction_after_move != direction_before_move):
            ai_play_game.moves += 1

        # Move the snake
        ai_play_game.move_snake()

        # If the snake eats the apple, reset shortcut cooldown
        if ai_play_game.snake.positions[0] == ai_play_game.apple.position:
            shortcut_cooldown = 0

        # Check for any collisions
        ai_play_game.check_collisions()

        # Update the visuals
        ai_play_game.update_game()
        pygame.display.update()
        clock.tick(FPS)
        clock.tick(SNAKE_SPEED)


# Improved A Star Risk AI Play (CAN FAIL) - Builds further on improved by adding a faster and more human like "risk" strategy
#                                           in the early game, with survival techniques in the early to mid-game in an attempt
#                                           to mitigate this.
def ai_play_a_star_risk():
    # Initialise the maze and the path the snake is going to follow
    maze_object = maze(GRID_HEIGHT/2, GRID_WIDTH/2)
    prim_maze = maze_object.generate_prim_maze()
    path_object = path(GRID_HEIGHT, GRID_WIDTH)
    maze_path = path_object.generate_path(prim_maze)

    # Initialise game class for AI Play
    ai_play_game = game("AI PLAY - A* RISK")

    # Get the initial position of the snake
    snake_position = (
        ai_play_game.snake.positions[0][0], ai_play_game.snake.positions[0][1])

    # Get the index of the path to start at
    path_position = maze_path.index(snake_position)

    # Initialise shortcut repeat list
    shortcuts_taken = []
    shortcut_cooldown = 0

    # Initialise clock object
    clock = pygame.time.Clock()

    # Initialise A* "risk mode" where we sacrifice guranteed survival for faster and more human looking performance
    a_star_risk_mode = True

    # Main game loop
    run = True
    while run:
        for event in pygame.event.get():
            # Listen for exit
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

        # Check percentage snake is filling up the board - if it reaches 15%, turn off A* risk mode
        snake_percent = (len(ai_play_game.snake.positions) /
                         (GRID_WIDTH*GRID_HEIGHT))*100
        if (snake_percent) > 15:
            a_star_risk_mode = False

        # Get position of the apple
        apple_position = ai_play_game.apple.position
        # Get position of the head
        snake_head_position = ai_play_game.snake.positions[0]
        # Get position of the tail
        snake_tail_position = ai_play_game.snake.positions[-1]

        # Get the index of the snake's head and the snakes tail in the maze path
        snake_tail_index = maze_path.index(
            (snake_tail_position[0], snake_tail_position[1]))
        snake_head_index = maze_path.index(
            (snake_head_position[0], snake_head_position[1]))

        # Search for adjacent nodes to the head
        adjacent_nodes = find_adjacent_nodes(
            snake_head_position, GRID_HEIGHT, GRID_WIDTH, ai_play_game.snake.positions)

        # If we can take a shortcut, get the shortest path from the head to the apple
        if shortcut_cooldown == 0 and snake_percent < 60:
            shortest_path = a_star_path(
                snake_head_position, apple_position, GRID_WIDTH, GRID_HEIGHT, ai_play_game.snake.positions)

        # Reduce the shortcut cooldown if we're in one
        if shortcut_cooldown > 0:
            shortcut_cooldown -= 1
            print(shortcut_cooldown)

        # Figure out what the coordinates are of the next position in the path
        if path_position == (len(maze_path)-1):
            coords_path_pos = 0
        else:
            coords_path_pos = [maze_path[path_position+1]
                               [0], maze_path[path_position+1][1]]

        # Check we were able to find a path
        # If we're smaller than 60% of the board (riskier than improved's 50%), try to take a shortcut, otherwise just follow the hamiltonian path
        if shortest_path != None and len(shortest_path) > 1 and shortcut_cooldown == 0 and snake_percent < 60:
            # If there is an adjacent node in the shortest path
            for node in adjacent_nodes:
                if node == shortest_path[1]:
                    # Get information about the shortcut to potentially store
                    shortcut_info = [snake_head_index, snake_tail_index, len(
                        ai_play_game.snake.positions)]
                    # Check if the shortcut node is in the indexes inbetween where the head and the tail are
                    if snake_head_index > snake_tail_index:
                        non_elligble_range = maze_path[snake_tail_index:snake_head_index]
                    else:
                        non_elligble_range = maze_path[snake_tail_index:] + \
                            maze_path[:snake_head_index]

                    # If we're not in A* Risk mode, then attempt a "safe" pertubated shortcut
                    if not a_star_risk_mode:
                        if (node[0], node[1]) not in non_elligble_range and shortcut_info not in shortcuts_taken:
                            # Store shortcut info so we don't end up in a loop
                            shortcuts_taken.append(shortcut_info)

                            # Check we're not overtaking the apple in the path and if not then set path position to 1 before the node we want to shortcut to
                            if maze_path.index((node[0], node[1]))-1 < maze_path.index((ai_play_game.apple.position[0], ai_play_game.apple.position[1])):
                                path_position = maze_path.index(
                                    (node[0], node[1]))-1
                            else:
                                # If we've just come out of A* risk mode, there's a chance our body is on our path. If this
                                # is the case, we're just going to try and find ANY free adjacent node in an attempt to survive
                                if coords_path_pos in ai_play_game.snake.positions:
                                    if adjacent_nodes == None:
                                        print("No adjacent nodes")
                                        clock.tick(.1)
                                    else:
                                        # If we can find an adjacent node, take the first one to survive
                                        for node in adjacent_nodes:
                                            path_position = maze_path.index(
                                                (node[0], node[1]))-1

                        elif (node[0], node[1]) in non_elligble_range:
                            # If we've just come out of A* risk mode, there's a chance our body is on our path. If this
                            # is the case, we're just going to try and find ANY free adjacent node in an attempt to survive
                            if coords_path_pos in ai_play_game.snake.positions:
                                if adjacent_nodes == None:
                                    print("No adjacent nodes")
                                    clock.tick(.1)
                                else:
                                    # If we can find an adjacent node, take the first one to survive
                                    for node in adjacent_nodes:
                                        path_position = maze_path.index(
                                            (node[0], node[1]))-1

                        # If we're in a shortcut loop, enter the cooldown period
                        elif shortcut_info in shortcuts_taken:
                            print("shortcut_info is: " + str(shortcut_info))
                            print("shortcuts taken are: " +
                                  str(shortcuts_taken))
                            print("\n Already taken this shortcut, cooling down...")
                            shortcut_cooldown = int(5000/GRID_SIZE)

                    # But If we are in a star risk mode, forget about everything else (risk it) and set the next step on the path to the A* path
                    elif a_star_risk_mode:
                        path_position = maze_path.index(
                            (node[0], node[1]))-1

        # Check that if we're in a* risk mode, then we'll TRY our best to ensure our next step won't kill us if we can't find a shortest path
        elif a_star_risk_mode:
            coords_path_pos = [maze_path[path_position]
                               [0], maze_path[path_position][1]]
            # If our next step on the path is about to kill us, try and take another adjacent node to survive
            if coords_path_pos in ai_play_game.snake.positions:
                if adjacent_nodes == None:
                    print("No adjacent nodes")
                    clock.tick(.1)
                else:
                    # If we can find an adjacent node, take the first one to survive
                    for node in adjacent_nodes:
                        print("potential node to move to is: ")
                        print(node)
                        path_position = maze_path.index(
                            (node[0], node[1]))-1

        # If we can't find a shortest path, we're not in A* risk mode and our next step is about to kill us, try to survive
        # (This is most likely when we've just exited A* risk mode)
        elif shortest_path == None and coords_path_pos in ai_play_game.snake.positions and not a_star_risk_mode:
            if adjacent_nodes == None:
                print("No adjacent nodes")
                clock.tick(.1)
            else:
                # If we can find an adjacent node, take the first one to survive
                for node in adjacent_nodes:
                    print("potential node to move to is: ")
                    print(node)
                    path_position = maze_path.index(
                        (node[0], node[1]))-1

        # If we are at the end of our path index, "reset" it
        if path_position == (len(maze_path)-1):
            path_position = -1

        # PATH DIRECTION DEFINITIONS
        path_right = (maze_path[path_position+1] ==
                      (snake_position[0] + 1, snake_position[1]))
        path_left = (maze_path[path_position+1] ==
                     (snake_position[0] - 1, snake_position[1]))
        path_up = (maze_path[path_position+1] ==
                   (snake_position[0], snake_position[1] - 1))
        path_down = (maze_path[path_position+1] ==
                     (snake_position[0], snake_position[1] + 1))

        # Define directions before move, so that we can check if the AI has "pressed a key" in the traditional sense
        direction_before_move = ai_play_game.snake.current_direction
        direction_after_move = ai_play_game.snake.current_direction

        # Determine which direction to move depending on where we are on the path
        if path_position < (len(maze_path)-1):
            if path_right:
                ai_play_game.snake.current_direction = ai_play_game.snake.right
                snake_position = (
                    snake_position[0]+1, snake_position[1])
                direction_after_move = ai_play_game.snake.right
            elif path_left:
                ai_play_game.snake.current_direction = ai_play_game.snake.left
                snake_position = (
                    snake_position[0]-1, snake_position[1])
                direction_after_move = ai_play_game.snake.left
            elif path_up:
                ai_play_game.snake.current_direction = ai_play_game.snake.up
                snake_position = (
                    snake_position[0], snake_position[1]-1)
                direction_after_move = ai_play_game.snake.up
            elif path_down:
                ai_play_game.snake.current_direction = ai_play_game.snake.down
                snake_position = (
                    snake_position[0], snake_position[1]+1)
                direction_after_move = ai_play_game.snake.down
            path_position += 1

        if (direction_after_move != direction_before_move):
            ai_play_game.moves += 1

        ai_play_game.move_snake()
        # If the snake eats the apple, reset shortcut cooldown
        if ai_play_game.snake.positions[0] == ai_play_game.apple.position:
            shortcut_cooldown = 0
        ai_play_game.check_collisions()  # Check for any collisions

        # Update the visuals
        ai_play_game.update_game()
        pygame.display.update()
        clock.tick(FPS)
        clock.tick(SNAKE_SPEED)


#-----------------------/\ AI PLAY FUNCTIONS /\-----------------------#


# Call Main Menu Function to begin the game
if __name__ == "__main__":
    main_menu()

# Use this file to change the starting settings of the snake game (ai/difficulty/speed can also be done via the options menu in-game)

# Settings
AI_PLAY = "SIMPLE"  # SIMPLE, IMPROVED, RISK
# Speed and difficulty are defined with a dictionary so the button functions are more descriptive
SPEED_DICT = {"SLOW": 10, "MEDIUM": 25, "FAST": 50}
SPEED = "FAST"
SNAKE_SPEED = SPEED_DICT[SPEED]
# Difficulty is defined through the grid size
DIFFICULTY_DICT = {"EASY": 75, "MEDIUM": 60, "HARD": 50}
DIFFICULTY = "EASY"
GRID_SIZE = DIFFICULTY_DICT[DIFFICULTY]

# Setup Grid
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
GRID_WIDTH = (SCREEN_WIDTH/GRID_SIZE)
GRID_HEIGHT = (SCREEN_HEIGHT/GRID_SIZE)

# Define FPS
FPS = 60

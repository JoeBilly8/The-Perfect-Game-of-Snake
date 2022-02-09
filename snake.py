# NOTES:
# TO DO:
# 1) Fix game labels
# 2) Unit Tests
# 3) Implement A* Improved Pertubated Hamiltonian (need a survival mode for early A* paths)
# 4) Split Code + Tidy
# 5) Do a testing cycle to collect lots of runs of data
# 6) Add head/tail graphics
# 7) Add background music and sounds
# 8) Credits page?


#-----------------------IMPORTS-----------------------#
import heapq
from operator import index
import time
import pygame
import sys
import random

#---------------------LOAD IMAGES---------------------#
back_button_image = pygame.transform.scale(
    pygame.image.load('images/BackButton.png'), (100, 75))


#-----------------------CONSTANTS-----------------------#
# Define FPS
FPS = 60

# Initialise Pygame
pygame.init()

# Setup Screen
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The (not quite) Perfect Game Of Snake")

# Settings
AI_PLAY = "IMPROVED"
# Speed is defined with a dictionary so the button functions are more descriptive
SPEED_DICT = {"SLOW": 10, "MEDIUM": 25, "FAST": 50}
SPEED = "MEDIUM"
SNAKE_SPEED = SPEED_DICT[SPEED]  # 10 = SLOW, 25 = MEDIUM, 50 = FAST
# Difficulty is defined through the grid size
DIFFICULTY_DICT = {"EASY": 75, "MEDIUM": 60, "HARD": 50}
DIFFICULTY = "EASY"
GRID_SIZE = DIFFICULTY_DICT[DIFFICULTY]  # EASY = 75, MEDIUM = 60, HARD = 50

# Setup Grid
GRID_WIDTH = (SCREEN_WIDTH/GRID_SIZE)
GRID_HEIGHT = (SCREEN_HEIGHT/GRID_SIZE)

# Colour Scheme From Design
GREEN = pygame.Color("#476930")
LIGHT_GREEN = pygame.Color("#477830")
BACKGROUND_GREEN = pygame.Color("#47B430")
GREY = pygame.Color("#D3D3D3")
DARK_GREY = pygame.Color("#545454")
RED = pygame.Color("#930000")
BLACK = pygame.Color("#000000")


#-----------------------CLASSES-----------------------#
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

    def draw(self, screen):
        for pos in self.positions:
            snake_block = pygame.Rect(
                (pos[0]*(GRID_SIZE)), (pos[1]*(GRID_SIZE)), GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, GREY, snake_block)

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


class apple(object):
    def __init__(self):
        self.randomise_pos([])

    def draw(self, screen):
        apple_rect = pygame.Rect((self.x * GRID_SIZE),
                                 (self.y * GRID_SIZE), GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, RED, apple_rect)

    def randomise_pos(self, snake_body):
        self.x = random.randint(0, (GRID_WIDTH-1))
        self.y = random.randint(0, (GRID_HEIGHT-1))
        # Check if apple has randomised to within the snakes body
        for pos in snake_body:
            if self.x == pos[0] and self.y == pos[1]:
                # Apple is within snake body so randomise again
                print("Apple is within snake body, rerandomising")
                self.randomise_pos(snake_body)
        self.position = [self.x, self.y]


class game(object):

    def __init__(self, game_label):
        self.snake = snake()
        self.apple = apple()
        self.game_score = 0
        self.moves = 0
        self.game_label = game_label
        self.start_time = time.time()

    def move_snake(self):
        self.snake.move()

    def update_game(self):
        draw_grid(WINDOW)
        self.display_score()
        self.display_moves()
        self.display_game_label()
        self.snake.draw(WINDOW)
        self.apple.draw(WINDOW)
        self.check_for_game_over()

    def check_collisions(self):
        # If snake has eaten the apple, reposition the apple and add to the body
        if self.snake.positions[0] == self.apple.position:
            # Add an extra block to the snake's body
            self.snake.grow()
            self.game_score += 1
            if self.game_score != (GRID_WIDTH*GRID_HEIGHT)-2:
                print("gamescore is: " + str(self.game_score))
                # Randomise apple position
                self.apple.randomise_pos(self.snake.positions)
            else:  # Otherwise we've won
                print("SNAKE HAS WON")
                end_time = time.time()
                print("SCORE: " + str(self.game_score))
                print("MOVES: " + str(self.moves))
                print("TIME TAKEN: " +
                      str(int(end_time-self.start_time)) + " seconds")
                main_menu()

    def check_for_game_over(self):
        # If the snake hits itself - game over
        for pos in self.snake.positions[1:]:
            if self.snake.positions[0][0] == pos[0] and self.snake.positions[0][1] == pos[1]:
                # If the snake has hit itself but it is filling the grid, we've won
                # if len(self.snake.positions) == (GRID_HEIGHT*GRID_WIDTH):
                #     print("SNAKE HAS WON")
                #     print("SCORE: " + str(self.game_score))
                #     print("")
                # else:
                print("GAME OVER BY SNAKE")
                print("SCORE: " + str(self.game_score))
                print("MOVES: " + str(self.moves))
                main_menu()
        # If the snake hits the edge of a border - game over
        if not (0 <= self.snake.positions[0][0] < GRID_WIDTH) or not (0 <= self.snake.positions[0][1] < GRID_HEIGHT):
            print("GAME OVER BY BORDER")
            main_menu()

    def display_score(self):
        roboto_font = pygame.font.Font("RobotoCondensed-Bold.ttf", 20)
        score = roboto_font.render(
            str("SCORE: " + str(self.game_score)), 1, GREY)
        score_rect = score.get_rect(center=(45, 20))
        WINDOW.blit(score, score_rect)

    def display_moves(self):
        roboto_font = pygame.font.Font("RobotoCondensed-Bold.ttf", 20)
        score = roboto_font.render(
            str("MOVES: " + str(self.moves)), 1, GREY)
        score_rect = score.get_rect(center=(47.5, 40))
        WINDOW.blit(score, score_rect)

    def display_game_label(self):
        roboto_font = pygame.font.Font("RobotoCondensed-Bold.ttf", 20)
        game_label = roboto_font.render(str(self.game_label), 1, GREY)
        offset = 90 if len(self.game_label) * \
            60 > 90 else len(self.game_label)*60
        game_label_rect = game_label.get_rect(
            center=((GRID_SIZE*GRID_WIDTH)-(offset), 20))
        WINDOW.blit(game_label, game_label_rect)


class maze(object):
    def __init__(self, grid_rows, grid_columns):
        # Define rows/columns from the width/height - easier to mentally picture
        self.grid_rows = grid_rows
        self.grid_columns = grid_columns

    def get_cell_neighbours(self, cell):
        # Get grid rows and columns from the object
        grid_rows = self.grid_rows
        grid_columns = self.grid_columns

        # Define neighbours as empty list to begin with
        neighbours = []

        # Define the 9 potential cases for neighbours of cells in a grid: (Note middle isn't listed as this will be "else")
        top_left_corner = (cell[0]-1 < 0 and cell[1] - 1 < 0)
        top_row = (cell[0] + 1 < grid_columns and cell[0] -
                   1 >= 0 and cell[1] - 1 < 0)
        top_right_corner = (cell[0]+1 >= grid_columns and cell[1] - 1 < 0)
        right_row = (cell[0]+1 >= grid_columns and cell[1] -
                     1 >= 0 and cell[1] + 1 < grid_rows)
        bottom_right_corner = (
            cell[0]+1 == grid_columns and cell[1] + 1 >= grid_rows)
        bottom_row = (cell[0]+1 <= grid_columns and cell[0] -
                      1 >= 0 and cell[1] + 1 >= grid_rows)
        bottom_left_corner = (cell[0]-1 < 0 and cell[1] + 1 >= grid_rows)
        left_row = (cell[0]-1 < 0 and cell[1] - 1 >=
                    0 and cell[1] + 1 < grid_rows)

        # Return different neighbours depending on where the cell is in the grid
        if(top_left_corner):
            neighbours = [(cell[0]+1, cell[1]), (cell[0], cell[1]+1)]
        elif(top_row):
            neighbours = [(cell[0]-1, cell[1]), (cell[0]+1,
                                                 cell[1]), (cell[0], cell[1]+1)]
        elif(top_right_corner):
            neighbours = [(cell[0]-1, cell[1]), (cell[0], cell[1]+1)]
        elif(right_row):
            neighbours = [(cell[0]-1, cell[1]),
                          (cell[0], cell[1]+1), (cell[0], cell[1]-1)]
        elif(bottom_right_corner):
            neighbours = [(cell[0]-1, cell[1]), (cell[0], cell[1]-1)]
        elif(bottom_row):
            neighbours = [(cell[0]-1, cell[1]), (cell[0]+1,
                                                 cell[1]), (cell[0], cell[1]-1)]
        elif(bottom_left_corner):
            neighbours = [(cell[0]+1, cell[1]), (cell[0], cell[1]-1)]
        elif(left_row):
            neighbours = [(cell[0]+1, cell[1]),
                          (cell[0], cell[1]+1), (cell[0], cell[1]-1)]
        # Use else for any cell in the middle of the grid
        else:
            neighbours = [(cell[0]+1, cell[1]), (cell[0], cell[1]+1),
                          (cell[0], cell[1]-1), (cell[0]-1, cell[1])]

        return neighbours

    def generate_prim_maze(self):
        # Get grid rows and columns from the object
        grid_rows = self.grid_rows
        grid_columns = self.grid_columns

        # Get number of cells in the grid
        number_of_cells = (grid_rows*grid_columns)

        # Pick a random cell
        x = random.randint(0, (grid_columns-1))
        y = random.randint(0, (grid_rows-1))
        cell = (x, y)

        # Add random cell and None entrance to maze_list
        # Maze List is a list of lists of the cells and their wall entrances and exists
        maze_list = [[cell]]
        cells_visited = [cell]
        neighbours_list = []

        while((len(cells_visited)) < number_of_cells):
            # Get all neighbours of the cell and add them to neighbours_list if they're not already in there
            neighbours_list = neighbours_list + list(set(self.get_cell_neighbours(
                cell)) - set(neighbours_list))

            # Pick a random neighbour from the neighbours_list
            cell_neighbour = neighbours_list[random.randint(
                0, len(neighbours_list)-1)]

            # If the neighbour is unvisitied then create a "wall" between the neighbour and the cell we're looking at
            if cell_neighbour not in cells_visited:
                cells_visited.append(cell_neighbour)

                # If the neighbour cell has a cell visited to it's left then then (cellx, celly): "wall_left"
                if((cell_neighbour[0]-1, cell_neighbour[1]) in cells_visited):
                    connection_cell = (cell_neighbour[0]-1, cell_neighbour[1])
                    for i in maze_list:
                        if connection_cell in i:
                            # Append connection cell wall exit information to maze list for cell
                            i.append("right")
                    # Append neighbour cell wall entrance information to maze list for cell neighbour
                    maze_list.append([cell_neighbour, "left"])

                # If the neighbour cell has a cell visited above it then (cellx, celly): "wall_above"
                elif((cell_neighbour[0], cell_neighbour[1]-1) in cells_visited):
                    connection_cell = (cell_neighbour[0], cell_neighbour[1]-1)
                    for i in maze_list:
                        if connection_cell in i:
                            # Append connection cell wall exit information to maze list for cell
                            i.append("bottom")
                    # Append neighbour cell wall entrance information to maze list for cell neighbour
                    maze_list.append([cell_neighbour, "top"])

                # If the neighbour cell has a cell visited to it's right then then (cellx, celly): "wall_right"
                elif((cell_neighbour[0]+1, cell_neighbour[1]) in cells_visited):
                    connection_cell = (cell_neighbour[0]+1, cell_neighbour[1])
                    for i in maze_list:
                        if connection_cell in i:
                            # Append connection cell wall exit information to maze list for cell
                            i.append("left")
                    # Append neighbour cell wall entrance information to maze list for cell neighbour
                    maze_list.append([cell_neighbour, "right"])

                # If the neighbour cell has a cell visitied below it then (cellx, celly): "wall_below"
                elif((cell_neighbour[0], cell_neighbour[1]+1) in cells_visited):
                    connection_cell = (cell_neighbour[0], cell_neighbour[1]+1)
                    for i in maze_list:
                        if connection_cell in i:
                            # Append connection cell wall exit information to maze list for cell
                            i.append("top")
                    # Append neighbour cell wall entrance information to maze list for cell neighbour
                    maze_list.append([cell_neighbour, "bottom"])

                # Move to the newly visited cell_neighbour and restart the process
                cell = cell_neighbour
            # Loop back round and look at the newly added cell

        return maze_list


class path(object):
    #### CLASS: PATH ####
    #### Description: Generates a path for a grid given a randomly generated prims maze of size (grid_columns/2), (grid_rows/2) ####

    # Define the direction change in a nested dictionary
    direction_change_definitions = {'NORTH': {'right': 'EAST', 'left': 'WEST'}, 'EAST': {'right': 'SOUTH', 'left': 'NORTH'}, 'SOUTH': {'right': 'WEST', 'left': 'EAST'}, 'WEST': {
        'right': 'NORTH', 'left': 'SOUTH'}}

    # Define the movement depending on direction in a nested dictionary
    direction_movement_definitions = {'NORTH': {'right': {'x': 1, 'y': 0}, 'forward': {'x': 0, 'y': -1}, 'left': {'x': -1, 'y': 0}}, 'EAST': {'right': {'x': 0, 'y': 1}, 'forward': {'x': 1, 'y': 0}, 'left': {
        'x': 0, 'y': -1}}, 'SOUTH': {'right': {'x': -1, 'y': 0}, 'forward': {'x': 0, 'y': 1}, 'left': {'x': 1, 'y': 0}}, 'WEST': {'right': {'x': 0, 'y': -1}, 'forward': {'x': -1, 'y': 0}, 'left': {'x': 0, 'y': 1}}}

    def __init__(self, grid_rows, grid_columns):
        self.grid_columns = grid_columns
        self.grid_rows = grid_rows

    def can_go_right(self, maze, direction, cell, node, grid_columns, grid_rows):
        if not self.is_wall_right(maze, direction, cell, node) and not self.is_edge_right(grid_columns, grid_rows, direction, node):
            return True
        else:
            return False

    def can_go_forward(self, maze, direction, cell, node, grid_columns, grid_rows):
        if not self.is_wall_infront(maze, direction, cell, node) and not self.is_edge_infront(grid_columns, grid_rows, direction, node):
            return True
        else:
            return False

    def is_wall_right(self, maze, direction, cell, node):
        # Retrieve maze infomation about the cell
        for i in maze:
            if i[0] == cell:
                cell_info = i

        # Retrieve where the node is in the cell is
        if node[0] % 2 == 0 and node[1] % 2 == 0:
            node_value = "top_left"
        elif node[0] % 2 == 1 and node[1] % 2 == 0:
            node_value = "top_right"
        elif node[0] % 2 == 0 and node[1] % 2 == 1:
            node_value = "bottom_left"
        else:
            node_value = "bottom_right"

        if direction == "NORTH":
            if node_value == "top_left":
                if "top" in cell_info:
                    is_wall_right = True
                else:
                    is_wall_right = False

            elif node_value == "bottom_left":
                if "bottom" in cell_info:
                    is_wall_right = True
                else:
                    is_wall_right = False
            else:
                is_wall_right = False

        elif direction == "SOUTH":
            if node_value == "top_right":
                if "top" in cell_info:
                    is_wall_right = True
                else:
                    is_wall_right = False

            elif node_value == "bottom_right":
                if "bottom" in cell_info:
                    is_wall_right = True
                else:
                    is_wall_right = False
            else:
                is_wall_right = False

        if direction == "EAST":
            if node_value == "top_left":
                if "left" in cell_info:
                    is_wall_right = True
                else:
                    is_wall_right = False

            elif node_value == "top_right":
                if "right" in cell_info:
                    is_wall_right = True
                else:
                    is_wall_right = False
            else:
                is_wall_right = False

        if direction == "WEST":
            if node_value == "bottom_left":
                if "left" in cell_info:
                    is_wall_right = True
                else:
                    is_wall_right = False

            elif node_value == "bottom_right":
                if "right" in cell_info:
                    is_wall_right = True
                else:
                    is_wall_right = False
            else:
                is_wall_right = False

        return is_wall_right

    def is_wall_infront(self, maze, direction, cell, node):
        # Retrieve maze infomation about the cell
        for i in maze:
            if i[0] == cell:
                cell_info = i

        # Retrieve where the node is in the cell is
        if node[0] % 2 == 0 and node[1] % 2 == 0:
            node_value = "top_left"
        elif node[0] % 2 == 1 and node[1] % 2 == 0:
            node_value = "top_right"
        elif node[0] % 2 == 0 and node[1] % 2 == 1:
            node_value = "bottom_left"
        else:
            node_value = "bottom_right"

        if direction == "NORTH":
            if node_value == "bottom_left":
                if "left" in cell_info:
                    is_wall_infront = True
                else:
                    is_wall_infront = False

            elif node_value == "bottom_right":
                if "right" in cell_info:
                    is_wall_infront = True
                else:
                    is_wall_infront = False
            else:
                is_wall_infront = False

        elif direction == "SOUTH":
            if node_value == "top_left":
                if "left" in cell_info:
                    is_wall_infront = True
                else:
                    is_wall_infront = False

            elif node_value == "top_right":
                if "right" in cell_info:
                    is_wall_infront = True
                else:
                    is_wall_infront = False
            else:
                is_wall_infront = False

        if direction == "EAST":
            if node_value == "top_left":
                if "top" in cell_info:
                    is_wall_infront = True
                else:
                    is_wall_infront = False

            elif node_value == "bottom_left":
                if "bottom" in cell_info:
                    is_wall_infront = True
                else:
                    is_wall_infront = False
            else:
                is_wall_infront = False

        if direction == "WEST":
            if node_value == "top_right":
                if "top" in cell_info:
                    is_wall_infront = True
                else:
                    is_wall_infront = False

            elif node_value == "bottom_right":
                if "bottom" in cell_info:
                    is_wall_infront = True
                else:
                    is_wall_infront = False
            else:
                is_wall_infront = False

        return is_wall_infront

    def is_edge_right(self, grid_columns, grid_rows, direction, node):
        # Retrieve where the node is in the cell is
        if node[0] % 2 == 0 and node[1] % 2 == 0:
            node_value = "top_left"
        elif node[0] % 2 == 1 and node[1] % 2 == 0:
            node_value = "top_right"
        elif node[0] % 2 == 0 and node[1] % 2 == 1:
            node_value = "bottom_left"
        else:
            node_value = "bottom_right"

        if direction == "NORTH":
            if node_value == "bottom_right":
                if node[0] == (grid_columns-1):
                    is_edge_right = True
                else:
                    is_edge_right = False

            elif node_value == "top_right":
                if node[0] == (grid_columns-1):
                    is_edge_right = True
                else:
                    is_edge_right = False
            else:
                is_edge_right = False

        elif direction == "SOUTH":
            if node_value == "top_left":
                if node[0] == 0:
                    is_edge_right = True
                else:
                    is_edge_right = False

            elif node_value == "bottom_left":
                if node[0] == 0:
                    is_edge_right = True
                else:
                    is_edge_right = False
            else:
                is_edge_right = False

        if direction == "EAST":
            if node_value == "bottom_left":
                if node[1] == (grid_rows-1):
                    is_edge_right = True
                else:
                    is_edge_right = False

            elif node_value == "bottom_right":
                if node[1] == (grid_rows-1):
                    is_edge_right = True
                else:
                    is_edge_right = False
            else:
                is_edge_right = False

        if direction == "WEST":
            if node_value == "top_left":
                if node[1] == 0:
                    is_edge_right = True
                else:
                    is_edge_right = False

            elif node_value == "top_right":
                if node[1] == 0:
                    is_edge_right = True
                else:
                    is_edge_right = False
            else:
                is_edge_right = False

        return is_edge_right

    def is_edge_infront(self, grid_columns, grid_rows, direction, node):
        # Retrieve where the node is in the cell is
        if node[0] % 2 == 0 and node[1] % 2 == 0:
            node_value = "top_left"
        elif node[0] % 2 == 1 and node[1] % 2 == 0:
            node_value = "top_right"
        elif node[0] % 2 == 0 and node[1] % 2 == 1:
            node_value = "bottom_left"
        else:
            node_value = "bottom_right"

        if direction == "NORTH":
            if node_value == "top_left":
                if node[1] == 0:
                    is_edge_infront = True
                else:
                    is_edge_infront = False

            elif node_value == "top_right":
                if node[1] == 0:
                    is_edge_infront = True
                else:
                    is_edge_infront = False
            else:
                is_edge_infront = False

        elif direction == "SOUTH":
            if node_value == "bottom_left":
                if node[1] == (grid_rows-1):
                    is_edge_infront = True
                else:
                    is_edge_infront = False

            elif node_value == "bottom_right":
                if node[1] == (grid_rows-1):
                    is_edge_infront = True
                else:
                    is_edge_infront = False
            else:
                is_edge_infront = False

        if direction == "EAST":
            if node_value == "top_right":
                if node[0] == (grid_columns-1):
                    is_edge_infront = True
                else:
                    is_edge_infront = False

            elif node_value == "bottom_right":
                if node[0] == (grid_columns-1):
                    is_edge_infront = True
                else:
                    is_edge_infront = False
            else:
                is_edge_infront = False

        if direction == "WEST":
            if node_value == "top_left":
                if node[0] == (grid_columns-1):
                    is_edge_infront = True
                else:
                    is_edge_infront = False

            elif node_value == "bottom_left":
                if node[0] == (grid_columns-1):
                    is_edge_infront = True
                else:
                    is_edge_infront = False
            else:
                is_edge_infront = False

        return is_edge_infront

    def generate_path(self, maze):
        # Get grid cols/rows
        grid_columns = self.grid_columns
        grid_rows = self.grid_rows

        # Get node number (should be double the number of "cells" in the initial prim maze)
        node_number = (grid_columns*grid_rows)

        # Initialise path as empty list to start with
        path = [(0, 0), (1, 0)]

        # Start at cell (0, 0)
        cell = (0, 0)

        # Start in node (top_left)
        node = (1, 0)

        # Head east to begin with
        direction = "EAST"

        while(len(path) < node_number):

            # Always try to go right first
            if self.can_go_right(maze, direction, cell, node, grid_columns, grid_rows):
                # Go to the node to the right depending on the direction
                new_node = (node[0]+self.direction_movement_definitions[direction]["right"]["x"],
                            node[1]+self.direction_movement_definitions[direction]["right"]["y"])

                # Change direction if we've gone right
                direction = self.direction_change_definitions[direction]["right"]

            # If we can't go right, try to go forward next
            elif self.can_go_forward(maze, direction, cell, node, grid_columns, grid_rows):
                # Go to the node in front depending on the direction
                new_node = (node[0]+self.direction_movement_definitions[direction]["forward"]["x"],
                            node[1]+self.direction_movement_definitions[direction]["forward"]["y"])

            # If we can't go right or forward we can only go left
            else:
                # Go to the node to the left depending on the direction
                new_node = (node[0]+self.direction_movement_definitions[direction]["left"]["x"],
                            node[1]+self.direction_movement_definitions[direction]["left"]["y"])

                # Change direction if we've gone left
                direction = self.direction_change_definitions[direction]["left"]

            # Add the new node to the path
            path.append(new_node)

            # Determine the cell we're now in depending on the node
            cell = (int(new_node[0]/2), int(new_node[1]/2))

            # Move to the new node and start the process over again
            node = new_node

        return path


class a_star_node(object):
    def __init__(self, position, parent=None):
        self.g = 0
        self.h = 0
        self.f = 0
        self.parent = parent
        self.position = [position[0], position[1]]

    def __eq__(self, other):
        return self.position == other.position

    def __repr__(self):
        return f"{self.position} - g: {self.g} h: {self.h} f: {self.f}"

    # defining less than for purposes of heap queue
    def __lt__(self, other):
        return self.f < other.f

    # defining greater than for purposes of heap queue
    def __gt__(self, other):
        return self.f > other.f


class button_rect(object):
    def __init__(self, text,  pos, font_size, background_colour, text_colour):
        self.x, self.y = pos
        self.font = pygame.font.SysFont("RobotoCondensed-Bold.ttf", font_size)
        self.set_text(text, background_colour, text_colour)

    def set_text(self, text, background_colour, text_colour):
        self.text = self.font.render(text, 1, text_colour)
        self.size = self.text.get_size()
        surface_size = (95, 27)
        print(surface_size)
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
                        DIFFICULTY = setting_value
                        GRID_SIZE = DIFFICULTY_DICT[DIFFICULTY]
                        GRID_WIDTH = (SCREEN_WIDTH/GRID_SIZE)
                        GRID_HEIGHT = (SCREEN_HEIGHT/GRID_SIZE)
                    elif setting == "ALGORITHM":
                        global AI_PLAY
                        AI_PLAY = setting_value
                    elif setting == "SPEED":
                        global SPEED
                        global SNAKE_SPEED
                        SPEED = setting_value
                        SNAKE_SPEED = SPEED_DICT[SPEED]

#-----------------------CLASSES-----------------------#

#-----------------------AI FUNCTIONS------------------#


def a_star_path(start, target, grid_columns, grid_rows, snake_positions):
    # Create a start node and a target node the specified node in the grid
    start_node = a_star_node(start)
    target = a_star_node(target)

    # Initialize the node open and closed list, add start_node to open list to begin with
    node_open_list = []
    node_closed_list = []

    # Heapify the node_open_list
    heapq.heapify(node_open_list)
    heapq.heappush(node_open_list, start_node)

    # Set a limit on the path_finding - if we reach this then break out and don't return a path
    max_iterations = ((GRID_HEIGHT*GRID_WIDTH))
    iteration_number = 0

    # Loop until you find the end
    while len(node_open_list) > 0 and iteration_number < max_iterations:
        iteration_number += 1

        # Get the current node
        current_node = heapq.heappop(node_open_list)
        node_closed_list.append(current_node)

        # If we've reached our target, return the path
        if current_node == target:
            print("FOUND A PATH")
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path

        # Generating the children of the current node
        children = []
        # Adjacent squares in the context of the snake game
        adjacent_positions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        for new_position in adjacent_positions:
            # Get the node position
            node_position = [
                current_node.position[0] + new_position[0], current_node.position[1] + new_position[1]]

            # Ensure we're not going past the edge of the snake grid
            if(node_position[0] > (grid_columns-1) or node_position[0] < 0 or node_position[1] > (grid_rows-1) or node_position[1] < 0):
                continue  # Skip the iteration

            # Ensure we're not in the body/tail
            if node_position in snake_positions:
                continue

            # Create a new node
            new_node = a_star_node(node_position, current_node)

            # Add it to the children
            children.append(new_node)

        # Loop through the children and add them to the node_open_list if not already in it
        for child in children:
            # If child is on the node closed list then skip
            if child in node_closed_list:
                continue
            # Otherwise create the f, g and h values of the child
            child.g = current_node.g + 1
            child.h = (abs(child.position[0] - target.position[0]) +
                       abs(child.position[1] - target.position[1]))
            child.f = child.g + child.h

            # If the child is already in the open node list and has a greater g value then skip
            for open_node in node_open_list:
                if child == open_node and child.g >= open_node.g:
                    continue

            # Otherwise add the child to the node open list
            heapq.heappush(node_open_list, child)

    print("Couldn't find a path")
    return None


def find_adjacent_nodes(node, grid_rows, grid_columns, snake_positions):
    adjacent_nodes = []
    # print("NODE IS: " + str(node))
    # Adjacent squares in the context of the snake game
    adjacent_positions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    for new_position in adjacent_positions:
        node_position = [node[0] + new_position[0], node[1] + new_position[1]]
        # Ensure we're not going past the edge of the snake grid
        if(node_position[0] > (grid_columns-1) or node_position[0] < 0 or node_position[1] > (grid_rows-1) or node_position[1] < 0):
            continue  # Skip the iteration
        # Ensure we're not in the body/tail
        if node_position in snake_positions:
            continue

        adjacent_nodes.append(node_position)

    return adjacent_nodes


#-----------------------AI FUNCTIONS------------------#


#---------------------HELPER FUNCTIONS----------------#

def fill_screen(screen, colour):
    screen.fill(colour)


def draw_grid(screen):
    # Fill window with light green to start with (for light green squares)
    screen.fill((LIGHT_GREEN))
    # Initialise Grassy Grid
    for column in range(int(GRID_HEIGHT)):
        if column % 2 == 0:
            for row in range(int(GRID_WIDTH)):
                grid_rect = pygame.Rect(
                    (row * GRID_SIZE), (column * GRID_SIZE), GRID_SIZE, GRID_SIZE)
                if (row % 2) == 0:
                    pygame.draw.rect(screen, GREEN, grid_rect)
        else:
            for row in range(int(GRID_WIDTH)):
                grid_rect = pygame.Rect(
                    (row * GRID_SIZE), (column * GRID_SIZE), GRID_SIZE, GRID_SIZE)
                if (row % 2) != 0:
                    pygame.draw.rect(screen, GREEN, grid_rect)


def create_text(text_to_write, font_size, x, y, colour=GREY):
    # Define Roboto Font
    roboto_font = pygame.font.Font("RobotoCondensed-Bold.ttf", font_size)
    # Render text
    text = roboto_font.render(text_to_write, 1, colour)
    text_rect = text.get_rect(center=(x, y))
    return text, text_rect


def renderTextCenteredAt(text, fontsize, colour, x, y, screen, allowed_width):
    # first, split the text into words
    words = text.split()

    roboto_font = pygame.font.Font("RobotoCondensed-Bold.ttf", fontsize)

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
    # the culmative height of the lines we've rendered so far
    y_offset = 0
    for line in lines:
        fw, fh = roboto_font.size(line)

        # (tx, ty) is the top-left of the font surface
        tx = x - fw / 2
        ty = y + y_offset

        font_surface = roboto_font.render(line, True, colour)
        screen.blit(font_surface, (tx, ty))

        y_offset += fh

#---------------------HELPER FUNCTIONS----------------#

#-----------------------CONTROL FLOW FUNCTIONS-----------------------#


def main_menu():
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
                    print("Difficulty is: " + DIFFICULTY)
                    print("AI PLAY is: " + AI_PLAY)
                    print("Speed is: " + SPEED)
                    if manual_play_text_rect.collidepoint(event.pos):
                        print("MANUAL PLAY PRESSED")
                        manual_play()
                    if ai_play_text_rect.collidepoint(event.pos):
                        print("AI PLAY PRESSED")
                        if AI_PLAY == "SIMPLE":
                            ai_play_simple_hamiltonian()
                        elif AI_PLAY == "PERTUBATED":
                            ai_play_pertubated_hamiltonian()
                        elif AI_PLAY == "IMPROVED":
                            ai_play_improved_a_star_hamiltonian()
                        else:
                            print("Error, setting not selected")
                    if options_text_rect.collidepoint(event.pos):
                        print("OPTIONS BUTTON PRESSED")
                        options()
                    if more_info_text_rect.collidepoint(event.pos):
                        print("MORE INFO BUTTON PRESSED")
                        more_info()

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
        clock.tick(SNAKE_SPEED)

# Simple Hamiltonian


def ai_play_simple_hamiltonian():
    # Initialise the maze and the path the snake is going to follow
    maze_object = maze(GRID_HEIGHT/2, GRID_WIDTH/2)
    prim_maze = maze_object.generate_prim_maze()
    path_object = path(GRID_HEIGHT, GRID_WIDTH)
    maze_path = path_object.generate_path(prim_maze)

    # Initialise game class for AI Play
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
        print("PATH POSITION: " + str(path_position))
        print("SNAKE POSITION: ")
        print(snake_position)

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

        for event in pygame.event.get():
            # Listen for exit
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

        direction_before_move = ai_play_game.snake.current_direction

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
        ai_play_game.check_collisions()  # Check for any collisions

        # Update the visuals
        ai_play_game.update_game()
        pygame.display.update()
        clock.tick(FPS)
        clock.tick(SNAKE_SPEED)

# Pertubated Hamiltonian


def ai_play_pertubated_hamiltonian():
    # Initialise the maze and the path the snake is going to follow
    maze_object = maze(GRID_HEIGHT/2, GRID_WIDTH/2)
    prim_maze = maze_object.generate_prim_maze()
    path_object = path(GRID_HEIGHT, GRID_WIDTH)
    maze_path = path_object.generate_path(prim_maze)

    # Initialise game class for AI Play
    ai_play_game = game("AI PLAY - PERTUBATED HAMILTONIAN")

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
        # Get position of the apple
        apple_position = ai_play_game.apple.position
        # Get position of the head
        snake_head_position = ai_play_game.snake.positions[0]
        # Get position of the tail
        snake_tail_position = ai_play_game.snake.positions[-1]

        snake_tail_index = maze_path.index(
            (snake_tail_position[0], snake_tail_position[1]))
        snake_head_index = maze_path.index(
            (snake_head_position[0], snake_head_position[1]))

        # Search for adjacent nodes to the head
        adjacent_nodes = find_adjacent_nodes(
            snake_head_position, GRID_HEIGHT, GRID_WIDTH, ai_play_game.snake.positions)

        # If we can take a shortcut, get the shortest path from the head to the apple
        if shortcut_cooldown == 0:
            shortest_path = a_star_path(
                snake_head_position, apple_position, GRID_WIDTH, GRID_HEIGHT, ai_play_game.snake.positions)

        # Reduce the shortcut cooldown if we're in one
        if shortcut_cooldown > 0:
            shortcut_cooldown -= 1
            print(shortcut_cooldown)

        # Check we were able to find a path
        if shortest_path != None and shortcut_cooldown == 0:
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

                    if ((node[0], node[1]) not in non_elligble_range) and (shortcut_info not in shortcuts_taken):
                        # Store shortcut info so we don't end up in a loop
                        shortcuts_taken.append(shortcut_info)
                        # Set path position to 1 before the node we want to shortcut to
                        path_position = maze_path.index(
                            (node[0], node[1]))-1
                    elif (node[0], node[1]) in non_elligble_range:
                        print("We're at path index: " + str(path_position))
                        print("Our path is: " + str(maze_path))
                        print(
                            "NODE " + str(node) + " IS IN NON ELLIGIBLE RANGE OF " + str(non_elligble_range))
                        print(snake_head_position)
                        print(snake_tail_position)
                    elif shortcut_info in shortcuts_taken:
                        print("shortcut_info is: " + str(shortcut_info))
                        print("shortcuts taken are: " +
                              str(shortcuts_taken))
                        print("\n Already taken this shortcut, cooling down...")
                        shortcut_cooldown = int(5000/GRID_SIZE)
                        # shortcuts_taken.clear()
                    # else:
                    #     path_position = maze_path.index(
                    #         (node[0], node[1]))-1

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

        for event in pygame.event.get():
            # Listen for exit
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

        direction_before_move = ai_play_game.snake.current_direction
        direction_after_move = ai_play_game.snake.current_direction

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


def ai_play_improved_a_star_hamiltonian():
    # Initialise the maze and the path the snake is going to follow
    maze_object = maze(GRID_HEIGHT/2, GRID_WIDTH/2)
    prim_maze = maze_object.generate_prim_maze()
    path_object = path(GRID_HEIGHT, GRID_WIDTH)
    maze_path = path_object.generate_path(prim_maze)

    # Initialise game class for AI Play
    ai_play_game = game("AI PLAY - IMPROVED A* HAMILTONIAN")

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
        print("length of snake is: " + str(len(ai_play_game.snake.positions)))
        snake_percent = (len(ai_play_game.snake.positions) /
                         (GRID_WIDTH*GRID_HEIGHT))*100
        print("SNAKE PERCENT IS: " + str(snake_percent))
        if (snake_percent) > 25:
            print("REACHED 25%")
            a_star_risk_mode = False  # If we've reached 25% turn off risk mode

        # Get position of the apple
        apple_position = ai_play_game.apple.position
        # Get position of the head
        snake_head_position = ai_play_game.snake.positions[0]
        # Get position of the tail
        snake_tail_position = ai_play_game.snake.positions[-1]

        snake_tail_index = maze_path.index(
            (snake_tail_position[0], snake_tail_position[1]))
        snake_head_index = maze_path.index(
            (snake_head_position[0], snake_head_position[1]))

        # Search for adjacent nodes to the head
        adjacent_nodes = find_adjacent_nodes(
            snake_head_position, GRID_HEIGHT, GRID_WIDTH, ai_play_game.snake.positions)

        # If we can take a shortcut, get the shortest path from the head to the apple
        if shortcut_cooldown == 0:
            shortest_path = a_star_path(
                snake_head_position, apple_position, GRID_WIDTH, GRID_HEIGHT, ai_play_game.snake.positions)

        # Reduce the shortcut cooldown if we're in one
        if shortcut_cooldown > 0:
            shortcut_cooldown -= 1
            print(shortcut_cooldown)

        # Check we were able to find a path
        if shortest_path != None and len(shortest_path) > 1 and shortcut_cooldown == 0:
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

                    if not a_star_risk_mode:
                        if (node[0], node[1]) not in non_elligble_range and shortcut_info not in shortcuts_taken:
                            # Store shortcut info so we don't end up in a loop
                            shortcuts_taken.append(shortcut_info)
                            # Set path position to 1 before the node we want to shortcut to
                            path_position = maze_path.index(
                                (node[0], node[1]))-1
                        elif (node[0], node[1]) in non_elligble_range:
                            print(
                                "NODE " + str(node) + " IS IN NON ELLIGIBLE RANGE OF " + str(non_elligble_range))
                        elif shortcut_info in shortcuts_taken:
                            print("shortcut_info is: " + str(shortcut_info))
                            print("shortcuts taken are: " +
                                  str(shortcuts_taken))
                            print("\n Already taken this shortcut, cooling down...")
                            shortcut_cooldown = int(5000/GRID_SIZE)
                        else:
                            next_potential_path_pos = maze_path.index(
                                (node[0], node[1]))-1
                            next_potential_path_pos = maze_path[next_potential_path_pos]
                            next_potential_path_pos = [
                                next_potential_path_pos[0], next_potential_path_pos[1]]
                            # If the planned route on the path is clear of our body, carry on as normal
                            if (next_potential_path_pos not in ai_play_game.snake.positions):
                                path_position = maze_path.index(
                                    (node[0], node[1]))-1
                            else:
                                print(
                                    "WE R FINNISH- SURVIVAL MODE ENGAGEd NOT A* RISK MODE")
                                for node in adjacent_nodes:
                                    next_potential_path_pos = maze_path.index(
                                        (node[0], node[1]))-1
                                    next_potential_path_pos = maze_path[next_potential_path_pos]
                                    next_potential_path_pos = [
                                        next_potential_path_pos[0], next_potential_path_pos[1]]
                                    # If the next step on our path isn't about to kill us, take it
                                    if not (next_potential_path_pos not in ai_play_game.snake.positions):
                                        path_position = maze_path.index(
                                            (node[0], node[1]))-1
                                    else:
                                        print("THERES A BODY AT: ")
                                        print(node[0])
                                        print(node[1])
                    # If we are in A* risk mode then follow the path
                    elif a_star_risk_mode:
                        path_position = maze_path.index(
                            (node[0], node[1]))-1
                    elif not a_star_risk_mode:
                        print(
                            "WE R FINNISH- SURVIVAL MODE ENGAGEd NOT A* RISK MODE")
                        for node in adjacent_nodes:
                            next_potential_path_pos = maze_path.index(
                                (node[0], node[1]))-1
                            next_potential_path_pos = maze_path[next_potential_path_pos]
                            next_potential_path_pos = [
                                next_potential_path_pos[0], next_potential_path_pos[1]]
                            # If the next step on our path isn't about to kill us, take it
                            if not (next_potential_path_pos not in ai_play_game.snake.positions):
                                path_position = maze_path.index(
                                    (node[0], node[1]))-1
                            else:
                                print("THERES A BODY AT: ")
                                print(node[0])
                                print(node[1])
        # If we're still in A* risk mode but can't find a path - stay alive until we can again
        elif a_star_risk_mode and (maze_path[path_position][0], maze_path[path_position][1]) in ai_play_game.snake.positions:
            print("WE R FINNISH- SURVIVAL MODE ENGAGEd A STAR RISQE MODE")
            for node in adjacent_nodes:
                next_potential_path_pos = maze_path.index(
                    (node[0], node[1]))-1
                next_potential_path_pos = maze_path[next_potential_path_pos]
                next_potential_path_pos = [
                    next_potential_path_pos[0], next_potential_path_pos[1]]
                # If the next step on our path isn't about to kill us, take it
                if not (next_potential_path_pos not in ai_play_game.snake.positions):
                    path_position = maze_path.index(
                        (node[0], node[1]))-1

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

        for event in pygame.event.get():
            # Listen for exit
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

        direction_before_move = ai_play_game.snake.current_direction
        direction_after_move = ai_play_game.snake.current_direction

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


def options():
    # Initialise clock object
    clock = pygame.time.Clock()

    # Difficulty Buttons
    difficulty_selected = "MEDIUM"
    easy_button = button_rect(
        "EASY", (225, (SCREEN_HEIGHT/4)+27), 25, GREY, BLACK)
    medium_button = button_rect(
        "MEDIUM", (350, (SCREEN_HEIGHT/4)+27), 25, GREY, BLACK)
    hard_button = button_rect(
        "HARD", (475, (SCREEN_HEIGHT/4)+27), 25, GREY, BLACK)

    # AI Algorithm Selection Buttons
    algorithm_selected = "SIMPLE"
    simple_button = button_rect(
        "SIMPLE", (225, (SCREEN_HEIGHT/4)+107), 25, GREY, BLACK)
    pertubated_button = button_rect(
        "PERTUBATED", (350, (SCREEN_HEIGHT/4)+107), 20, GREY, BLACK)
    improved_a_star_button = button_rect(
        "IMPROVED", (475, (SCREEN_HEIGHT/4)+107), 25, GREY, BLACK)

    # Speed Buttons
    speed_selected = "MEDIUM"
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
            pertubated_button.set_text("PERTUBATED", GREY, BLACK)
            improved_a_star_button.set_text("IMPROVED", GREY, BLACK)
        elif AI_PLAY == "PERTUBATED":
            simple_button.set_text("SIMPLE", GREY, BLACK)
            pertubated_button.set_text("PERTUBATED", DARK_GREY, GREY)
            improved_a_star_button.set_text("IMPROVED", GREY, BLACK)
        elif AI_PLAY == "IMPROVED":
            simple_button.set_text("SIMPLE", GREY, BLACK)
            pertubated_button.set_text("PERTUBATED", GREY, BLACK)
            improved_a_star_button.set_text("IMPROVED", DARK_GREY, GREY)
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
            pertubated_button.click(event, "ALGORITHM", "PERTUBATED")
            improved_a_star_button.click(event, "ALGORITHM", "IMPROVED")

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
        pertubated_button.show()
        improved_a_star_button.show()

        # Show Speed Buttons
        slow_speed_button.show()
        medium_speed_button.show()
        fast_speed_button.show()

        clock.tick(FPS)
        pygame.display.update()


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

        renderTextCenteredAt("This game of snake is the work for a final year project at the University of Liverpool and has been created by the student Joe Moore. The game can be played manually by the player or a specially designed AI algorithm can play the “perfect” game for you. The difficulty can be increased or decreased by increasing or decreasing the size of the board in the options menu.",
                             30, GREY, (SCREEN_WIDTH/2), (SCREEN_HEIGHT/8)+75, WINDOW, SCREEN_WIDTH-100)

        clock.tick(FPS)
        pygame.display.update()


# Call Main Menu Function to begin the game
main_menu()

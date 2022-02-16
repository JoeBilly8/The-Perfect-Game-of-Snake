
#-----------------------IMPORTS-----------------------#
from operator import is_
import pygame
import sys
import random

#-----------------------CONSTANTS-----------------------#
# Define FPS
FPS = 120

# Initialise Pygame
pygame.init()

# Setup Screen
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Prim Maze Generator Visual Example")

# Setup Grid
GRID_SIZE = 50
GRID_WIDTH = (3)
GRID_HEIGHT = (3)

# Colour Scheme From Design
GREEN = pygame.Color("#476930")
LIGHT_GREEN = pygame.Color("#477830")
BACKGROUND_GREEN = pygame.Color("#47B430")
GREY = pygame.Color("#D3D3D3")
DARK_GREY = pygame.Color("#545454")
RED = pygame.Color("#930000")

# 1) Generate a Prims maze
# 2) Find all nodes that can attach themselves to each other
# 3) Use this information to create a path alorithm

# Direction Definition:
#   EAST:
#       x+1 is forward
#       y+1 is right
#       y-1 is left
#   WEST:
#       x-1 is forward
#       y-1 is right
#       y+1 is left
#   NORTH:
#       y-1 is forward
#       x+1 is right
#       x-1 is left
#   SOUTH:
#       y+1 is forward
#       x-1 is right
#       x+1 is left

# Direction Change Definition:
#   EAST:
#       right: SOUTH
#       left: NORTH
#   WEST:
#       right: NORTH
#       left: SOUTH
#   NORTH:
#       right: EAST
#       left: WEST
#   SOUTH:
#       right: WEST
#       left: EAST


# Generates a path for a grid given a randomly generated prims maze of size (grid_columns/2), (grid_rows/2)
class path(object):
    # Define the direction change in a nested dictionary
    direction_change_definitions = {'NORTH': {'right': 'EAST', 'left': 'WEST'}, 'EAST': {'right': 'SOUTH', 'left': 'NORTH'}, 'SOUTH': {'right': 'WEST', 'left': 'EAST'}, 'WEST': {
        'right': 'NORTH', 'left': 'SOUTH'}}

    # Define the movement depending on direction in a nested dictionary
    direction_movement_definitions = {'NORTH': {'right': {'x': 1, 'y': 0}, 'forward': {'x': 0, 'y': -1}, 'left': {'x': -1, 'y': 0}}, 'EAST': {'right': {'x': 0, 'y': 1}, 'forward': {'x': 1, 'y': 0}, 'left': {
        'x': 0, 'y': -1}}, 'SOUTH': {'right': {'x': -1, 'y': 0}, 'forward': {'x': 0, 'y': 1}, 'left': {'x': 1, 'y': 0}}, 'WEST': {'right': {'x': 0, 'y': -1}, 'forward': {'x': -1, 'y': 0}, 'left': {'x': 0, 'y': 1}}}

    def __init__(self, grid_columns, grid_rows):
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

        print("CELL INFO IS: ")
        print(cell_info)

        # Retrieve where the node is in the cell is
        if node[0] % 2 == 0 and node[1] % 2 == 0:
            node_value = "top_left"
        elif node[0] % 2 == 1 and node[1] % 2 == 0:
            node_value = "top_right"
        elif node[0] % 2 == 0 and node[1] % 2 == 1:
            node_value = "bottom_left"
        else:
            node_value = "bottom_right"

        print("WE ARE IN NODE: ")
        print(node_value)

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

                print("CAN GO RIGHT")

                print("CHANGING DIRECTION FROM " + direction)
                # Change direction if we've gone right
                direction = self.direction_change_definitions[direction]["right"]

                print("TO " + direction)

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

            print("NEW NODE IS " + str(node))

            print("PATH IS ")
            print(path)
        return path


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


# Initialise clock object
clock = pygame.time.Clock()

# Main game loop
maze = maze(GRID_HEIGHT, GRID_WIDTH)
prim_maze = maze.generate_prim_maze()

# prim_maze = [[(2, 0), 'bottom', 'left'], [(2, 1), 'top', 'bottom'], [(2, 2), 'top', 'left'], [(1, 2), 'right', 'left'], [
#     (1, 0), 'right', 'left'], [(0, 2), 'right'], [(0, 0), 'right', 'bottom'], [(0, 1), 'top', 'right'], [(1, 1), 'left']]
print(prim_maze)

path = path(6, 6)
pathage = path.generate_path(prim_maze)
print(pathage)

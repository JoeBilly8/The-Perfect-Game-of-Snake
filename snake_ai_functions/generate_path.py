# Path Class: Generates a path for a grid given a randomly generated prims maze of size (grid_columns/2), (grid_rows/2)
# Works on the basis that we can follow a prim maze of half the size while always keeping the maze to our right to create a randomly generated hamiltonian cycle
class path(object):
    # Define the direction change in a nested dictionary
    direction_change_definitions = {'NORTH': {'right': 'EAST', 'left': 'WEST'}, 'EAST': {'right': 'SOUTH', 'left': 'NORTH'}, 'SOUTH': {'right': 'WEST', 'left': 'EAST'}, 'WEST': {
        'right': 'NORTH', 'left': 'SOUTH'}}

    # Define the movement depending on direction in a nested dictionary
    direction_movement_definitions = {'NORTH': {'right': {'x': 1, 'y': 0}, 'forward': {'x': 0, 'y': -1}, 'left': {'x': -1, 'y': 0}}, 'EAST': {'right': {'x': 0, 'y': 1}, 'forward': {'x': 1, 'y': 0}, 'left': {
        'x': 0, 'y': -1}}, 'SOUTH': {'right': {'x': -1, 'y': 0}, 'forward': {'x': 0, 'y': 1}, 'left': {'x': 1, 'y': 0}}, 'WEST': {'right': {'x': 0, 'y': -1}, 'forward': {'x': -1, 'y': 0}, 'left': {'x': 0, 'y': 1}}}

    def __init__(self, grid_rows, grid_columns):
        self.grid_columns = grid_columns
        self.grid_rows = grid_rows

    # If we don't have a wall or an edge to our right, we can turn right
    def can_go_right(self, maze, direction, cell, node, grid_columns, grid_rows):
        if not self.is_wall_right(maze, direction, cell, node) and not self.is_edge_right(grid_columns, grid_rows, direction, node, cell):
            return True
        else:
            return False

    # If we don't have a wall or an edge in front of us, we can go forward
    def can_go_forward(self, maze, direction, cell, node, grid_columns, grid_rows):
        if not self.is_wall_infront(maze, direction, cell, node) and not self.is_edge_infront(grid_columns, grid_rows, direction, node, cell):
            return True
        else:
            return False

    # Cross reference the direction we're going with our current position to check if there's a wall to our right
    def is_wall_right(self, maze, direction, cell, node):
        # Retrieve maze infomation about the cell
        for i in maze:
            if i[0] == cell:
                cell_info = i

        # Retrieve where the node is in the cell
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

    # Cross reference the direction we're going with our current position to check if there's a wall infront of us
    def is_wall_infront(self, maze, direction, cell, node):
        # Retrieve maze infomation about the cell
        for i in maze:
            if i[0] == cell:
                cell_info = i

        # Retrieve where the node is in the cell
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

    # Cross reference the direction we're going with our current position to check if there's a edge to our right
    def is_edge_right(self, grid_columns, grid_rows, direction, node, cell):
        # Retrieve where the node is in the cell
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
                if cell[0] == (grid_columns-1):
                    is_edge_right = True
                else:
                    is_edge_right = False

            elif node_value == "top_right":
                if cell[0] == (grid_columns-1):
                    is_edge_right = True
                else:
                    is_edge_right = False
            else:
                is_edge_right = False

        elif direction == "SOUTH":
            if node_value == "top_left":
                if cell[0] == 0:
                    is_edge_right = True
                else:
                    is_edge_right = False

            elif node_value == "bottom_left":
                if cell[0] == 0:
                    is_edge_right = True
                else:
                    is_edge_right = False
            else:
                is_edge_right = False

        if direction == "EAST":
            if node_value == "bottom_left":
                if cell[1] == (grid_rows-1):
                    is_edge_right = True
                else:
                    is_edge_right = False

            elif node_value == "bottom_right":
                if cell[1] == (grid_rows-1):
                    is_edge_right = True
                else:
                    is_edge_right = False
            else:
                is_edge_right = False

        if direction == "WEST":
            if node_value == "top_left":
                if cell[1] == 0:
                    is_edge_right = True
                else:
                    is_edge_right = False

            elif node_value == "top_right":
                if cell[1] == 0:
                    is_edge_right = True
                else:
                    is_edge_right = False
            else:
                is_edge_right = False

        return is_edge_right

    # Cross reference the direction we're going with our current position to check if there's an edge infront of us
    def is_edge_infront(self, grid_columns, grid_rows, direction, node, cell):
        # Retrieve where the node is in the cell
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
                if cell[1] == 0:
                    is_edge_infront = True
                else:
                    is_edge_infront = False

            elif node_value == "top_right":
                if cell[1] == 0:
                    is_edge_infront = True
                else:
                    is_edge_infront = False
            else:
                is_edge_infront = False

        elif direction == "SOUTH":
            if node_value == "bottom_left":
                if cell[1] == (grid_rows-1):
                    is_edge_infront = True
                else:
                    is_edge_infront = False

            elif node_value == "bottom_right":
                if cell[1] == (grid_rows-1):
                    is_edge_infront = True
                else:
                    is_edge_infront = False
            else:
                is_edge_infront = False

        if direction == "EAST":
            if node_value == "top_right":
                if cell[0] == (grid_columns-1):
                    is_edge_infront = True
                else:
                    is_edge_infront = False

            elif node_value == "bottom_right":
                if cell[0] == (grid_columns-1):
                    is_edge_infront = True
                else:
                    is_edge_infront = False
            else:
                is_edge_infront = False

        if direction == "WEST":
            if node_value == "top_left":
                if cell[0] == 0:
                    is_edge_infront = True
                else:
                    is_edge_infront = False

            elif node_value == "bottom_left":
                if cell[0] == 0:
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

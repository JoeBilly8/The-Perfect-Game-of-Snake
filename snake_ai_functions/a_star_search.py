# FULL DISCLOSURE: I used the following articles pseudocode/code https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
# As well as the following github gist: https://gist.github.com/ryancollingwood/32446307e976a11a1185a5394d6657bc
# For the ideas to implement the A* algorithm into my code

import heapq


# Node class for use in the A Star Search
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

    # Defining less than for purposes of heap queue
    def __lt__(self, other):
        return self.f < other.f

    # Defining greater than for purposes of heap queue
    def __gt__(self, other):
        return self.f > other.f


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
    max_iterations = (grid_rows*grid_columns)+25
    iteration_number = 0

    # Loop until you find the end
    while len(node_open_list) > 0 and iteration_number < max_iterations:
        iteration_number += 1

        # Get the current node
        current_node = heapq.heappop(node_open_list)
        node_closed_list.append(current_node)

        # If we've reached our target, return the path
        if current_node == target:
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

    # If we can't find a path, return None
    return None

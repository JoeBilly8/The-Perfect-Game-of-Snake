# FULL DISCLOSURE: I used the following articles pseudocode/code https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
# As well as the following github gist: https://gist.github.com/ryancollingwood/32446307e976a11a1185a5394d6657bc
# For the ideas and implementation of the A* algorithm
# No point in reinventing the wheel!

import heapq


class a_star_node:
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


def a_star_path(start, target, grid_columns, grid_rows, snake_positions):
    #print("Starting A* Search")
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
    max_iteration = ((grid_columns*grid_rows) // 2)*100
    iteration_number = 0

    # Loop until you find the end
    while len(node_open_list) > 0 and iteration_number < max_iteration:
        iteration_number += 1

        # Get the current node
        current_node = heapq.heappop(node_open_list)
        node_closed_list.append(current_node)

        # If we've reached our target, return the path
        if current_node == target:
            #print("REACHED TAGET NODE")
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
            #print("CURRENT NODE IS: " + str(current_node.position))
            # Get the node position
            node_position = [
                current_node.position[0] + new_position[0], current_node.position[1] + new_position[1]]
            #print("NEW NODE POSITION IS: " + str(node_position))

            # Ensure we're not going past the edge of the snake grid
            if(node_position[0] > (grid_columns-1) or node_position[0] < 0 or node_position[1] > (grid_rows-1) or node_position[1] < 0):
                #print("GOING OUT OF GRID")
                continue  # Skip the iteration

            # Ensure we're not in the body/tail
            if node_position in snake_positions:
                #print("IN SNAKE BODY")
                continue

            # Create a new node
            #print("NOT OUT OF GRID OR IN SNAKE BODY")
            new_node = a_star_node(node_position, current_node)
            #print("APPENDING " + str(new_node.position) + " TO CIHLDREN")

            # Add it to the children
            children.append(new_node)

        #print("CHILDREN ARE: ")
        # for child in children:
            # print(str(child.position))
        # Loop through the children and add them to the node_open_list if not already in it
        for child in children:
            # If child is on the node closed list then skip
            if child in node_closed_list:
                #print("CHILD IS IN CLOSED LIST")
                continue
            # Otherwise create the f, g and h values of the child
            child.g = current_node.g + 1
            child.h = (abs(child.position[0] - target.position[0]) +
                       abs(child.position[1] - target.position[1]))
            child.f = child.g + child.h

            # If the child is already in the open node list and has a greater g value then skip
            for open_node in node_open_list:
                if child == open_node and child.g >= open_node.g:
                    #print("CHILD IS IN OPEN LIST")
                    continue

            # Otherwise add the child to the node open list
            # node_open_list.append(child)
            #print("APPENDING CHILD: " + str(child.position) + " TO OPEN LIST")
            heapq.heappush(node_open_list, child)

    print("Couldn't find a path")
    return None


def test():
    grid_rows = 20
    grid_columns = 20

    snake_positions = [[0, 2], [1, 2]]

    start = snake_positions[0]
    apple = [19, 15]

    path = a_star_path(start, apple, grid_columns, grid_rows, snake_positions)

    print(path)


test()

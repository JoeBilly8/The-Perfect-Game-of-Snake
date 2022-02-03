# // A* (star) Pathfinding Pseudocode (https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2)
# // Initialize both open and closed list
# let the openList equal empty list of nodes
# let the closedList equal empty list of nodes
# // Add the start node
# put the startNode on the openList (leave it's f at zero)
# // Loop until you find the end
# while the openList is not empty
#     // Get the current node
#     let the currentNode equal the node with the least f value
#     remove the currentNode from the openList
#     add the currentNode to the closedList
#     // Found the goal
#     if currentNode is the goal
#         Congratz! You've found the end! Backtrack to get path
#     // Generate children
#     let the children of the currentNode equal the adjacent nodes

#     for each child in the children
#         // Child is on the closedList
#         if child is in the closedList
#             continue to beginning of for loop
#         // Create the f, g, and h values
#         child.g = currentNode.g + distance between child and current
#         child.h = distance from child to end
#         child.f = child.g + child.h
#         // Child is already in openList
#         if child.position is in the openList's nodes positions
#             if the child.g is higher than the openList node's g
#                 continue to beginning of for loop
#         // Add the child to the openList
#         add the child to the openList


from snake import SNAKE_SPEED


class a_star_node:
    def __init__(self, position, parent=None):
        self.g = 0
        self.h = 0
        self.f = 0
        self.parent = parent
        self.position = position

    def equivalent(self, other):
        return self.position == other.position


def a_star_path(start, target, grid_columns, grid_rows, snake_positions):
    # Create a start node and a target node the specified node in the grid
    start_node = a_star_node(start)
    target = a_star_node(target)

    # Initialize the node open and closed list, add start_node to open list to begin with
    node_open_list = [start_node]
    node_closed_list = []

    # Loop until you find the end
    while len(node_open_list) > 0:
        # Get the current node
        current_node = node_open_list[0]
        current_index = 0
        for index, node in enumerate(node_open_list):
            if node.f < current_node.f:
                current_node = node
                current_index = index

        # Pop current off open list, add to closed list
        node_closed_list.append(node_open_list.pop(current_index))

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
            node_position = (
                current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Ensure we're not going past the edge of the snake grid
            if(node_position[0] > len(grid_columns)-1 or node_position[0] < 0 or node_position[1] > len(grid_rows)-1 or node_position[1] < 0):
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
            for closed_node in node_closed_list:
                if child == closed_node:
                    continue

            # Otherwise create the f, g and h values of the child
            child.g = current_node.g + 1
            child.h = (abs(child.position[0] - target.position[0]) +
                       abs(child.position[1] - target.position[1]))
            child.f = child.g + child.h

            # If the child is already in the open node list and has a greater g value then skip
            for open_node in node_open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Otherwise add the child to the node open list
            node_open_list.append(child)


def test():
    grid_rows = 4
    grid_columns = 4

    snake_positions = [[0, 2], [1, 2]]

    start = snake_positions[0]
    apple = [0, 3]

    path = a_star_path(start, apple, grid_columns, grid_rows, snake_positions)

    print(path)

# Function for finding all the adjacent nodes from the head of the snake
# Discard any nodes past the edge of the grid or ones that are in the snake body
def find_adjacent_nodes(node, grid_rows, grid_columns, snake_positions):
    adjacent_nodes = []
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

import random


# Maze Class: Generates a Prim's maze using prim's algorithm, which is then passed to the Path class to generate a hamiltonian path.
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

            # If the neighbour is unvisited then create a "wall" between the neighbour and the cell we're looking at
            if cell_neighbour not in cells_visited:
                cells_visited.append(cell_neighbour)

                # If the neighbour cell has a cell visited to it's left then (cellx, celly): "wall_left"
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

                # If the neighbour cell has a cell visited below it then (cellx, celly): "wall_below"
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

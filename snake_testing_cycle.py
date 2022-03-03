# Imports
import csv
import sys
import time
import pygame
from snake_ai_functions.a_star_search import a_star_path
from snake_ai_functions.find_adjacent_nodes import find_adjacent_nodes
from snake_ai_functions.prim_maze import maze
from snake_ai_functions.generate_path import path
from snake_helper_functions.helper import *
from snake_settings import *
from snake_main import snake, apple

# Initialise Pygame
pygame.init()

# Setup Screen
WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Perfect Game Of Snake TESTING CYCLE")

# Set for breaking out of a game at game over to start the loop over again
game_running = True


# Testing cycle function - runs a chosen algorithm on a loop, recording the stats for each game
def testing_cycle():
    # Set the number of cycles we want to run
    test = AI_PLAY
    cycles = 100
    count = 0

    # Define the data header
    header = ['algorithm', 'difficulty', 'moves', 'time_taken', 'win']
    data = []

    # Testing loop
    while count < cycles:
        if test == "SIMPLE":
            print("testing simple")
            game = ai_play_simple_hamiltonian()
        elif test == "IMPROVED":
            print("testing improved")
            game = ai_play_improved_hamiltonian()
        elif test == "RISK":
            print("testing a* risk")
            game = ai_play_a_star_risk()

        algorithm = test
        difficulty = DIFFICULTY
        moves = game.moves
        time_taken = int(game.end_time-game.start_time)
        win = game.outcome

        row = [algorithm, difficulty, moves, time_taken, win]
        data.append(row)

        count += 1
        print("Count is: " + str(count))

    filename = ("testing_data/snake_testing_" +
                test + "_" + difficulty + ".csv")
    # Write the collected data to our csv file
    with open(filename, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        # write multiple rows
        writer.writerows(data)


# Almost the same game class as in the main game - just slightly editted to suit our "test loop" needs
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
        global game_running
        # If snake has eaten the apple, reposition the apple and add to the body
        if self.snake.positions[0] == self.apple.position:
            # Add an extra block to the snake's body
            self.snake.grow()
            self.game_score += 1
            if self.game_score != (GRID_WIDTH*GRID_HEIGHT)-2:
                # Randomise apple position
                self.apple.randomise_pos(self.snake.positions)
            else:  # Otherwise we've won
                self.end_time = time.time()
                print("SNAKE HAS WON")
                print("SCORE: " + str(self.game_score))
                print("MOVES: " + str(self.moves))
                print("TIME TAKEN: " +
                      str(int(self.end_time-self.start_time)) + " seconds")
                self.outcome = "WIN"
                game_running = False

    def check_for_game_over(self, screen=WINDOW):
        global game_running
        clock = pygame.time.Clock()
        # If the snake hits itself - game over
        for pos in self.snake.positions[1:]:
            if self.snake.positions[0][0] == pos[0] and self.snake.positions[0][1] == pos[1]:
                print("GAME OVER BY SNAKE")
                print("SCORE: " + str(self.game_score))
                print("MOVES: " + str(self.moves))
                self.outcome = "LOSE"
                self.end_time = time.time()
                game_running = False
        # If the snake hits the edge of a border - game over
        if not (0 <= self.snake.positions[0][0] < GRID_WIDTH) or not (0 <= self.snake.positions[0][1] < GRID_HEIGHT):
            print("GAME OVER BY BORDER")
            self.outcome = "LOSE"
            self.end_time = time.time()
            game_running = False

    def display_score(self, screen=WINDOW):
        roboto_font = pygame.font.Font("fonts/RobotoCondensed-Bold.ttf", 20)
        score = roboto_font.render(
            str("SCORE: " + str(self.game_score)), 1, GREY)
        score_rect = score.get_rect(center=(45, 20))
        screen.blit(score, score_rect)

    def display_moves(self, screen=WINDOW):
        roboto_font = pygame.font.Font("fonts/RobotoCondensed-Bold.ttf", 20)
        score = roboto_font.render(
            str("MOVES: " + str(self.moves)), 1, GREY)
        score_rect = score.get_rect(center=(47.5, 40))
        screen.blit(score, score_rect)

    def display_game_label(self, screen=WINDOW):
        roboto_font = pygame.font.Font("fonts/RobotoCondensed-Bold.ttf", 20)
        game_label = roboto_font.render(str(self.game_label), 1, GREY)
        # Get the right offset depending on the length of the game label
        offset = 150-(30-len(self.game_label)) * \
            5 if len(self.game_label) > 25 else 85
        game_label_rect = game_label.get_rect(
            center=((GRID_SIZE*GRID_WIDTH)-(offset), 20))
        screen.blit(game_label, game_label_rect)


# The same functions as used in the main game - just slightly editted to suit our "test loop" needs
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
    global game_running
    game_running = True
    while game_running:
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

    return ai_play_game


def ai_play_improved_hamiltonian():
    # Initialise the maze and the path the snake is going to follow
    maze_object = maze(GRID_HEIGHT/2, GRID_WIDTH/2)
    prim_maze = maze_object.generate_prim_maze()
    path_object = path(GRID_HEIGHT, GRID_WIDTH)
    maze_path = path_object.generate_path(prim_maze)

    # Initialise game class for AI Play
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
    global game_running
    game_running = True
    while game_running:
        # Get % of the board the snake is filling, if we're at 50%, don't try to take anymore shortcuts
        snake_percent = (len(ai_play_game.snake.positions) /
                         (GRID_WIDTH*GRID_HEIGHT))*100
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

                    if ((node[0], node[1]) not in non_elligble_range) and (shortcut_info not in shortcuts_taken):
                        # Store shortcut info so we don't end up in a loop
                        shortcuts_taken.append(shortcut_info)
                        # Set path position to 1 before the node we want to shortcut to
                        if maze_path.index((node[0], node[1]))-1 < maze_path.index((ai_play_game.apple.position[0], ai_play_game.apple.position[1])):
                            print(
                                "apple isnt being overtaken, take the shortcut")
                            path_position = maze_path.index(
                                (node[0], node[1]))-1
                        else:
                            print("we'd be overtaking the apple in the path")
                    elif (node[0], node[1]) in non_elligble_range:
                        print(
                            "NODE " + str(node) + " IS IN NON ELLIGIBLE RANGE OF " + str(non_elligble_range))
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

    return ai_play_game


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
    global game_running
    game_running = True
    while game_running:
        snake_percent = (len(ai_play_game.snake.positions) /
                         (GRID_WIDTH*GRID_HEIGHT))*100
        if (snake_percent) > 15:
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

        # Figure out what the coordinates are of the next position in the path
        if path_position == (len(maze_path)-1):
            coords_path_pos = 0
        else:
            coords_path_pos = [maze_path[path_position+1]
                               [0], maze_path[path_position+1][1]]

        # Check we were able to find a path
        # If we're smaller than 50% of the board, try to take a shortcut, otherwise just follow the hamiltonian path
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
                            # Set path position to 1 before the node we want to shortcut to
                            if maze_path.index((node[0], node[1]))-1 < maze_path.index((ai_play_game.apple.position[0], ai_play_game.apple.position[1])):
                                print(
                                    "apple isnt being overtaken, take the shortcut")
                                path_position = maze_path.index(
                                    (node[0], node[1]))-1
                            else:
                                print("we'd be overtaking the apple in the path")
                                if coords_path_pos in ai_play_game.snake.positions:
                                    print(
                                        "We're in non elligble territory, and our body is on the path, so now we're just going to try and survive")
                                    # clock.tick(.85)
                                    if adjacent_nodes == None:
                                        print("No adjacent nodes")
                                        clock.tick(.1)
                                    else:
                                        # If we can find an adjacent node, take the first one to survive
                                        for node in adjacent_nodes:
                                            path_position = maze_path.index(
                                                (node[0], node[1]))-1

                        elif (node[0], node[1]) in non_elligble_range:
                            print(
                                "NODE " + str(node) + " IS IN NON ELLIGIBLE RANGE OF " + str(non_elligble_range))
                            if coords_path_pos in ai_play_game.snake.positions:
                                print(
                                    "We're in non elligble territory, and our body is on the path, so now we're just going to try and survive")
                                # clock.tick(.85)
                                if adjacent_nodes == None:
                                    print("No adjacent nodes")
                                    clock.tick(.1)
                                else:
                                    # If we can find an adjacent node, take the first one to survive
                                    for node in adjacent_nodes:
                                        path_position = maze_path.index(
                                            (node[0], node[1]))-1

                        elif shortcut_info in shortcuts_taken:
                            print("shortcut_info is: " + str(shortcut_info))
                            print("shortcuts taken are: " +
                                  str(shortcuts_taken))
                            print("\n Already taken this shortcut, cooling down...")
                            shortcut_cooldown = int(5000/GRID_SIZE)

                    # But If we are in a star risk mode, set the next step on the path to the A* path
                    elif a_star_risk_mode:
                        path_position = maze_path.index(
                            (node[0], node[1]))-1

        # Check that if we're in a* risk mode, our next step won't kill us if we can't find a shortest path
        elif a_star_risk_mode:
            # path_position = maze_path.index(
            #     (node[0], node[1]))-1
            coords_path_pos = [maze_path[path_position]
                               [0], maze_path[path_position][1]]
            print("Coords path pos is: " + str(coords_path_pos))
            if coords_path_pos in ai_play_game.snake.positions:
                print("Entering survival mode for A*")
                # clock.tick(.85)
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

        # If we're out of A* risk mode but still not on the safety path, and we can't find a shortest path, try to survive
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

        print(coords_path_pos)
        # If we are at the end of our path index, "reset" it
        if path_position == (len(maze_path)-1):
            print("Resetting index............")
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

    return ai_play_game


print("Beginning Test Cycle")
testing_cycle()
print("Testing Cycle Complete")

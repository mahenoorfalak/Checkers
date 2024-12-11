import argparse
import sys
import time
import heapq
#====================================================================================

char_single = '2'
class Piece:
    """
    Code has been removed from this class, as per the instructor's guidelines.
    """
    pass

class Board:
    """
    Code has been removed from this class, as per the instructor's guidelines.
    """
    
    def can_move(self, piece, direction, empty_spaces):
        """
        Checks whether a given piece can move in the specified direction.

        Args:
            piece (Piece): The piece object to evaluate for movement.
            direction (str): The direction of movement ('up', 'down', 'left', 'right').
            empty_spaces (Board): A set of tuples representing the coordinates of empty spaces on the board.

        Returns:
            bool: True if the piece can move, False otherwise.
        """
        # piece corrdinate
        x = piece.coord_x  
        y = piece.coord_y

        if piece.is_2_by_2:
            if direction == 'up':
                if (y - 1) < 0:
                    return False
                elif (y - 1, x) not in empty_spaces or (y - 1, x + 1) not in empty_spaces:
                    return False
            elif direction == 'down':
                if y + 2 >= self.height:
                    return False
                elif (y + 2, x) not in empty_spaces or (y + 2, x + 1) not in empty_spaces:
                    return False
            elif direction == 'left':
                if (x - 1) < 0:
                    return False
                elif (y, x - 1) not in empty_spaces or (y + 1, x - 1) not in empty_spaces:
                    return False
            elif direction == 'right':
                if x + 2 >= 4:
                    return False
                elif (y, x + 2) not in empty_spaces or (y + 1, x + 2) not in empty_spaces:
                    return False
        
        elif piece.orientation == 'h':
            if direction == 'up':
                if y - 1 < 0:
                    return False
                elif (y - 1, x) not in empty_spaces or (y - 1, x + 1) not in empty_spaces:
                    return False
            elif direction == 'down':
                if (y + 1) >= self.height:
                    return False
                elif (y + 1, x) not in empty_spaces or (y + 1, x + 1) not in empty_spaces:
                    return False
            elif direction == 'left':
                if (x - 1) < 0:
                    return False
                elif (y, x - 1) not in empty_spaces:
                    return False
            elif direction == 'right':
                if (x + 2) >= self.width or (y, x + 2) not in empty_spaces:
                    return False
        
        elif piece.orientation == 'v':
            if direction == 'up':
                if (y - 1) < 0:
                    return False
                elif (y - 1, x) not in empty_spaces:
                    return False
            elif direction == 'down':
                if (y + 2) >= self.height:
                    return False
                elif (y + 2, x) not in empty_spaces:
                    return False
            elif direction == 'left':
                if (x - 1) < 0 or (y, x - 1) not in empty_spaces or (y + 1, x - 1) not in empty_spaces:
                    return False
            elif direction == 'right':
                if (x + 1) >= self.width or (y, x + 1) not in empty_spaces or (y + 1, x + 1) not in empty_spaces:
                    return False

        elif piece.is_single:
            if direction == 'up':
                if (y - 1) < 0 or (y - 1, x) not in empty_spaces:
                    return False
            elif direction == 'down':
                if (y + 1) >= self.height or (y + 1, x) not in empty_spaces:
                    return False
            elif direction == 'left':
                if (x - 1) < 0 or (y, x - 1) not in empty_spaces:
                    return False
            elif direction == 'right':
                if (x + 1) >= self.width or (y, x + 1) not in empty_spaces:
                    return False
        
        return True

    def move_piece(self, piece, direction):
        """
        Moves the piece in the given direction and return a new board configuration.

        Args:
        piece (Piece): The piece to be moved. 
        direction (str): The direction in which to move the piece ('up', 'down', 'left', 'right').

        Returns:
             Board: A new Board object representing the updated game state after the move.

        """
        # Copy the current grid
        new_grid = [row[:] for row in self.grid]
        new_pieces = self.pieces[:]

        x, y = piece.coord_x, piece.coord_y

        # Change current position of the piece as empty
        if piece.is_2_by_2:
            new_grid[y][x] = '.'
            new_grid[y][x + 1] = '.'
            new_grid[y + 1][x] = '.'
            new_grid[y + 1][x + 1] = '.'
        elif piece.orientation == 'h':
            new_grid[y][x] = '.'
            new_grid[y][x + 1] = '.'
        elif piece.orientation == 'v':
            new_grid[y][x] = '.'
            new_grid[y + 1][x] = '.'
        elif piece.is_single:
            new_grid[y][x] = '.'

        # calculate new position
        if direction == 'up':
            new_y = y - 1
            new_x = x
        elif direction == 'down':
            new_y = y + 1
            new_x = x
        elif direction == 'left':
            new_y = y
            new_x = x - 1
        elif direction == 'right':
            new_y = y
            new_x = x + 1

        # Update the piece coordinates in the new_pieces list
        for i, p in enumerate(new_pieces):
            if p == piece: 
                new_pieces[i] = Piece(piece.is_2_by_2, piece.is_single, new_x, new_y, piece.orientation)
                break

        # new position in the new grid
        if piece.is_2_by_2:
            new_grid[new_y][new_x] = '1'
            new_grid[new_y][new_x + 1] = '1'
            new_grid[new_y + 1][new_x] = '1'
            new_grid[new_y + 1][new_x + 1] = '1'
        elif piece.orientation == 'h': 
            new_grid[new_y][new_x] = '<'
            new_grid[new_y][new_x + 1] = '>'
        elif piece.orientation == 'v': 
            new_grid[new_y][new_x] = '^'
            new_grid[new_y + 1][new_x] = 'v'
        elif piece.is_single:
            new_grid[new_y][new_x] = '2'

        # new Board object with the updated grid and updated pieces
        new_board = Board(self.height, new_pieces) 
        new_board.grid = new_grid  

        new_board.blanks = new_board.find_empty_spaces() 

        return new_board

class State:
    """
    Code has been removed from this class, as per the instructor's guidelines.
    """
    
    def manhattan_distance(self, goal_state):
        """
        (Heuristic function) Calculates the Manhattan distance for the current state 
        relative to the goal state.This function computes the sum of the absolute differences 
        between the current coordinates of each piece in the board and its corresponding 
        position in the goal state. The Manhattan distance is used as a heuristic to measure how far 
        the current state is from the goal state in terms of horizontal and vertical 
        moves required to reach the goal.

        Args:
            goal_state (Board): The target or goal board configuration used to 
                                compare the current state.

        Returns:
            int: The total Manhattan distance of all pieces from their current positions to the goal positions. 
            A lower value indicates a closer configuration to the goal state.
        """
        total_distance = 0
        for piece in self.board.pieces:
            # Find the corresponding piece in the goal state
            goal_position = None
            for goal_piece in goal_state.board.pieces:
                if piece.is_2_by_2 and goal_piece.is_2_by_2:
                    goal_position = (goal_piece.coord_x, goal_piece.coord_y)
                elif piece.is_single and goal_piece.is_single:
                    goal_position = (goal_piece.coord_x, goal_piece.coord_y)
                elif piece.orientation == 'h' and goal_piece.orientation == 'h':
                    goal_position = (goal_piece.coord_x, goal_piece.coord_y)
                elif piece.orientation == 'v' and goal_piece.orientation == 'v':
                    goal_position = (goal_piece.coord_x, goal_piece.coord_y)

                if goal_position:
                    total_distance += abs(piece.coord_x - goal_position[0]) + abs(piece.coord_y - goal_position[1])
                    break

        return total_distance

    
    def generate_successor(self):
        """
        Generates all possible successor states by moving pieces into empty spaces.
        This method explores all possible directions ('up', 'down', 'left', 'right') 
        for each piece on the board. If the move is valid, it creates a new board 
        configuration (successor state) and adds it to the list of successors.

        Returns:
            list: A list of successor states generated by valid piece movements.
        """
        successors = []
        empty_spaces = self.board.find_empty_spaces()
        
        for piece in self.board.pieces:
            for direction in ['up', 'down', 'left', 'right']:
                if self.board.can_move(piece, direction, empty_spaces): 
                    new_board = self.board.move_piece(piece, direction)
                    new_state = State(new_board, hfn=0, f=0, depth=self.depth + 1, parent=self)
                    # Add this new state to the successors list
                    successors.append(new_state)
        
        return successors
    

def dfs(initial_state, goal_state):
    """
    Performs Depth-First Search (DFS) to find a solution from initial_state to goal_state.
    Explores the search space by expanding the most recent state (using a stack, LIFO order). 

    Args:
        initial_state (State): The starting state of the search.
        goal_state (State): The goal state to reach.

    Returns:
        State or str: The goal state if found, or "No solution" if no solution exists.
    """
    frontier = [initial_state]
    # Explored set to avoid revisiting states (stores string representations of the grid)
    explored = set()

    while frontier:
        current_state = frontier.pop() #LIFO

        # Convert the grid to a string representation for comparison
        current_state_str = grid_to_string(current_state.board.grid)
        
        # Check if state is goal
        if current_state.is_goal(goal_state):
            return current_state
        
        # If the current state is not explored, add it to the explored set
        if current_state_str not in explored:
            explored.add(current_state_str)
            successors = current_state.generate_successor()
            for successor in successors:
                frontier.append(successor)

    return "No solution" 

def a_star(initial_state, goal_state):
    """
    Performs A* search to find the optimal solution from initial_state to goal_state.
    This function uses a priority queue (min-heap) to explore states, selecting the
    one with the lowest f(n) = g(n) + h(n), where g(n) is the path cost and h(n)
    is the heuristic estimate (Manhattan distance).

    Args:
        initial_state (State): The starting state of the search.
        goal_state (State): The goal state to reach.

    Returns:
        State or str: The goal state if found, or "No solution" if no solution exists.
    """
    # Priority queue
    frontier = []
    initial_state.f = initial_state.depth + initial_state.manhattan_distance(goal_state) 
    heapq.heappush(frontier, (initial_state.f, initial_state))

    explored = set()

    while frontier:
        # Get the state with the lowest f(n) from the priority queue
        current_f_value, current_state = heapq.heappop(frontier)
        if current_state.is_goal(goal_state):
            return current_state       
        current_state_str = grid_to_string(current_state.board.grid)
        if current_state_str not in explored:
            explored.add(current_state_str)
            successors = current_state.generate_successor()
            for successor in successors:
                # Calculate g(n) + h(n) for the successor
                g_value = current_state.depth + 1 
                h_value = successor.manhattan_distance(goal_state) 
                successor.f = g_value + h_value
                heapq.heappush(frontier, (successor.f, successor))

    return "No solution"


def read_from_file(filename):
    """
    Load initial board from a given file.
    :param filename: The name of the given file.
    :type filename: str
    :return: A loaded board
    :rtype: Board
    """
    puzzle_file = open(filename, "r")
    line_index = 0
    pieces = []
    final_pieces = []
    final = False
    found_2by2 = False
    finalfound_2by2 = False
    height_ = 0

    for line in puzzle_file:
        height_ += 1
        if line == '\n':
            if not final:
                height_ = 0
                final = True
                line_index = 0
            continue

        if not final: #initial board
            for x, ch in enumerate(line):
                if ch == '^': # found vertical piece
                    pieces.append(Piece(False, False, x, line_index, 'v'))
                elif ch == '<': # found horizontal piece
                    pieces.append(Piece(False, False, x, line_index, 'h'))
                elif ch == char_single:
                    pieces.append(Piece(False, True, x, line_index, None))
                elif ch == '1':
                    if found_2by2 == False:
                        pieces.append(Piece(True, False, x, line_index, None))
                        found_2by2 = True
        else: #goal board
            for x, ch in enumerate(line):
                if ch == '^': # found vertical piece
                    final_pieces.append(Piece(False, False, x, line_index, 'v'))
                elif ch == '<': # found horizontal piece
                    final_pieces.append(Piece(False, False, x, line_index, 'h'))
                elif ch == char_single:
                    final_pieces.append(Piece(False, True, x, line_index, None))
                elif ch == '1':
                    if finalfound_2by2 == False:
                        final_pieces.append(Piece(True, False, x, line_index, None))
                        finalfound_2by2 = True
        line_index += 1
    puzzle_file.close()
    board = Board(height_, pieces)
    goal_board = Board(height_, final_pieces)
    return board, goal_board

def grid_to_string(grid):

    string = ""
    for i, line in enumerate(grid):
        for ch in line:
            string += ch
        string += "\n"
    return string


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfile",
        type=str,
        required=True,
        help="The input file that contains the puzzles."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The output file that contains the solution."
    )
    parser.add_argument(
        "--algo",
        type=str,
        required=True,
        choices=['astar', 'dfs'],
        help="The searching algorithm."
    )
    args = parser.parse_args()
    
    board, goal_board = read_from_file(args.inputfile)

    initial_state = State(board, hfn=0, f=0, depth=0) 
    goal_state = State(goal_board, hfn=0, f=0, depth=0)

    if args.algo == 'dfs':
        solution = dfs(initial_state, goal_state)
    else:
        solution = a_star(initial_state, goal_state)

    if solution != "No solution":
        steps = []
        current_state = solution
        while current_state:
            steps.append(current_state)
            current_state = current_state.parent
        steps.reverse() 

        # solution steps to the output file
        with open(args.outputfile, 'w') as f:
            for idx, step in enumerate(steps):
                f.write(grid_to_string(step.board.grid))
                if idx != len(steps) - 1:
                    f.write("\n")
    else:
        with open(args.outputfile, 'w') as f:
            f.write("No solution")
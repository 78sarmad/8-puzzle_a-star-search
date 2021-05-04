# represents position for a tile on puzzle board
class Position:
    def __init__(self, horizontal, vertical):
        self.horizontal = horizontal
        self.vertical = vertical

# find position of a tile on puzzle board
def find_position(state, value):
    for row in range(3):
        for col in range(3):
            # if value matches, pass to Position class as horizontal = col, vertical = row
            if state[row][col] == value:
                return Position(col, row) 

# distance between two tiles along x and y axis on board
def calculate_distance(state, value):
    current_pos = find_position(state, value) # position of value in current state
    goal_pos = find_position(goal_state, value) # position of value in goal_state state
    # find and return difference for both axes - horizontally and vertically
    diff = abs(goal_pos.horizontal - current_pos.horizontal) + abs(goal_pos.vertical - current_pos.vertical)
    return diff

# get heuristic value for board's current state
def calculate_heuristic(state):
    heuristic_value = 0 # initialize heuristic value as zero for each board
    # 3x3 board so we consider range as 3
    for i in range(3):
        for j in range(3):
            # calculate heuristic only for non-empty tile
            if state[i][j] != empty_tile:
                heuristic_value += calculate_distance(state, state[i][j])
    return heuristic_value

# represents Puzzle board
class Board:
    def __init__(self, state, g, parent):
        self.state = state
        self.g = g                          # distance from root
        self.h = calculate_heuristic(state) # heuristic for board state
        self.f = g + self.h
        self.parent = parent

# check if board state is goal state
def is_goal_state(state):
    return state == goal_state

# shuffle_board
def shuffle_board(node: Board):
    # set board configuration as explored and remove from frontier
    frontier.remove(node)
    explored.append(node.state)
    for direction in ['right', 'left', 'up', 'down']:
        # for all 4 directions, check if tile can move
        if can_move_tile(node.state, direction):
            # maintain a copy of current state before moving
            copy_state = [[x for x in y] for y in node.state]
            move_tile(copy_state, direction)
            # if the move is already not performed, execute it and add to frontier
            if copy_state not in explored:
                # create new board configuration branch, increase distance from root by 1
                new_node = Board(copy_state, node.g + 1, node)
                frontier.append(new_node)

# find empty tile for a board state
def find_empty_tile(state):
    return find_position(state, empty_tile)

# check if we can move tile in a direction
def can_move_tile(state, direction):
    position = find_empty_tile(state)
    # restrict left move if on last horizontal position i.e. [i][0] on 3x3 board
    if direction == 'left':
        return position.horizontal != 0
    # restrict right move if on last horizontal position i.e. [i][2] on 3x3 board
    elif direction == 'right':
        return position.horizontal != 2
    # restrict up move if on last horizontal position i.e. [0][j] on 3x3 board
    elif direction == 'up':
        return position.vertical != 0
    # restrict down move if on last horizontal position i.e. [2][j] on 3x3 board
    elif direction == 'down':
        return position.vertical != 2

# move an empty tile in a given direction
def move_tile(state, direction):
    if can_move_tile(state, direction):
        x = find_empty_tile(state).horizontal
        y = find_empty_tile(state).vertical
        
        # swap empty tile with the tile on left        
        if direction == 'left':
            state[y][x] = state[y][x - 1]
            state[y][x - 1] = empty_tile
        # swap empty tile with the tile on right
        elif direction == 'right':
            state[y][x] = state[y][x + 1]
            state[y][x + 1] = empty_tile
        # swap empty tile with the tile above
        elif direction == 'up':
            state[y][x] = state[y - 1][x]
            state[y - 1][x] = empty_tile
        # swap empty tile with the tile below
        elif direction == 'down':
            state[y][x] = state[y + 1][x]
            state[y + 1][x] = empty_tile

def a_star_search(initial_state, frontier, explored):
    current_board = frontier[0] # set first tile to current tile
    
    # if current tile state is not goal state
    while not is_goal_state(current_board.state):
        for board in frontier:
            current_board = frontier[0]
            # if board has lower value than current, replace current with with that
            if (board.f < current_board.f):
                current_board = board
        # shuffle board for all branch configurations in frontier
        shuffle_board(current_board)
    
    return current_board

if __name__ == "__main__":
    empty_tile = '0' # we denote an empty tile having zero value
    initial_state = [[1, 2, 4], [3, 5, 6], [8, empty_tile, 7]]
    goal_state = [[empty_tile, 1, 2], [3, 4, 5], [6, 7, 8]]
    
    frontier = [Board(initial_state, 0, None)]  # add first tile to frontier list
    explored = []                               # initialize explored tiles list

    print("Initial State: ", end=" ")
    print(initial_state)
    print("Goal State: ", end=" ")
    print(goal_state)

    # using a star search to reorder board
    final_board = a_star_search(initial_state, frontier, explored)
    board = final_board # a copy created to find parent boards
    stack = []
    total_moves = 0
    
    # appending all parent boards to stack
    while board.parent != None:
        total_moves += 1
        stack.append(board)
        board = board.parent
    
    # using stack to reverse the output 
    while len(stack):
        board = stack.pop()
        for j in range(3):
            print(board.state[j])
        print('\n')

    # finally print goal state and total moves
    print("Goal state reached: ")
    for i in range(3):
        print(final_board.state[i])
    
    print("\nTotal Moves: " + str(total_moves))
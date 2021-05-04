empty_tile = '0'
GOAL = [[empty_tile, 1, 2], [3, 4, 5], [6, 7, 8]]


def find_position(state, value):
    for i in range(3):
        for j in range(3):
            if state[i][j] == value:
                return Position(j, i)


def get_heuristic_value(state):
    def get_manhattan_distance(value):
        current_position = find_position(state, value)
        goal_position = find_position(GOAL, value)
        return abs(goal_position.width - current_position.width) + abs(goal_position.height - current_position.height)

    heuristic_value = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != empty_tile:
                heuristic_value += get_manhattan_distance(state[i][j])
    return heuristic_value


class Position:
    def __init__(self, width, height):
        self.width = width
        self.height = height


# states that exists in frontier
class LeafStatus:
    # g : distance from root (initial state)
    # h : heuristic value for this state
    def __init__(self, state, g, parent):
        self.state = state
        self.g = g
        self.h = get_heuristic_value(state)
        self.f = g + self.h
        self.parent = parent


def goal_test(state):
    return state == GOAL


# expand leaf if frontier and update frontier
def expand(leaf: LeafStatus):
    frontier.remove(leaf)
    explored.append(leaf.state)
    for arrow in ['right', 'left', 'top', 'bottom']:
        if can_move(leaf.state, arrow):
            # because in python Parameters are passed by reference, so we keep a copy of state
            copy_state = [[x for x in y] for y in leaf.state]
            move(copy_state, arrow)
            if copy_state not in explored:
                new_leaf = LeafStatus(copy_state, leaf.g + 1, leaf)
                frontier.append(new_leaf)


def find_blank(state):
    return find_position(state, empty_tile)


def can_move(state, direction):
    position = find_blank(state)
    if direction == 'right':
        return position.width != 2
    elif direction == 'left':
        return position.width != 0
    elif direction == 'top':
        return position.height != 0
    elif direction == 'bottom':
        return position.height != 2


def move(state, direction):
    if can_move(state, direction):
        b_width = find_blank(state).width
        b_height = find_blank(state).height

        if direction == 'right':
            state[b_height][b_width] = state[b_height][b_width + 1]
            state[b_height][b_width + 1] = empty_tile
        elif direction == 'left':
            state[b_height][b_width] = state[b_height][b_width - 1]
            state[b_height][b_width - 1] = empty_tile
        elif direction == 'top':
            state[b_height][b_width] = state[b_height - 1][b_width]
            state[b_height - 1][b_width] = empty_tile
        elif direction == 'bottom':
            state[b_height][b_width] = state[b_height + 1][b_width]
            state[b_height + 1][b_width] = empty_tile


initial_state = [[1, 2, 4], [3, 5, 6], [8, empty_tile, 7]]
frontier = [LeafStatus(initial_state, 0, None)]
selected_leaf = frontier[0]
explored = []

while not goal_test(selected_leaf.state):
    for leaf in frontier:
        selected_leaf = frontier[0]
        if leaf.f < selected_leaf.f:
            selected_leaf = leaf
    expand(selected_leaf)

print(selected_leaf.state)
a=selected_leaf
while  a.parent!=None:

    for i in range(3):
        print(a.parent.state[i])
    print('\n\n')
    a=a.parent
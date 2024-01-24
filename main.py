class Puzzle:
    def __init__(self, data):
        self.data = data
        self.blank_pos = []
        self.num_misplaced_tiles = 0
        self.manhatten_distance = 0
        self.total_cost = 0


def generate_states(current_state):
    states = []

    def swap_elements(puzz, blank_pos, new_pos):
        puzz.data[blank_pos[0]][blank_pos[1]], puzz.data[new_pos[0]][new_pos[1]] = puzz.data[new_pos[0]][new_pos[1]], \
            puzz.data[blank_pos[0]][blank_pos[1]]

    find_blank_pos(current_state)
    blank_pos = current_state.blank_pos

    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for move in moves:
        new_pos = (blank_pos[0] + move[0], blank_pos[1] + move[1])
        if 0 <= new_pos[0] < 3 and 0 <= new_pos[1] < 3:
            new_puzz = Puzzle([row.copy() for row in current_state.data])

            swap_elements(new_puzz, blank_pos, new_pos)

            new_puzz.blank_pos = new_pos
            find_total_cost(new_puzz)

            states.append(new_puzz)

    return states


def print_state(state):
    for row in state.data:
        print("+---+---+---+")
        print("|", "|".join(map(lambda x: f" {x} " if x != 9 else "   ", row)), "|")
    print("+---+---+---+")


def find_blank_pos(puzz):
    for row_index, line in enumerate(puzz.data):
        for column_index, l in enumerate(line):
            if l == 9:
                puzz.blank_pos = [row_index, column_index]


def find_misplaced_tiles(puzz):
    num_misplaced_tiles = 0
    goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    for row in range(3):
        for column in range(3):
            if goal_state[row][column] != puzz.data[row][column]:
                num_misplaced_tiles += 1
    puzz.num_misplaced_tiles = num_misplaced_tiles


def find_manhatten_distance(puzz):
    total_distance = 0
    for row in range(3):
        for column in range(3):
            num = puzz.data[row][column]
            goal_row = int((num - 1) / 3)
            goal_column = int((num - 1) % 3)
            total_distance += abs(row - goal_row) + abs(column - goal_column)
    puzz.manhatten_distance = total_distance


def find_total_cost(puzz):
    find_manhatten_distance(puzz)
    find_misplaced_tiles(puzz)
    puzz.total_cost = puzz.num_misplaced_tiles + puzz.manhatten_distance


def check_state_in_closed_list(state, closed_list):
    return state.data in closed_list


def is_solvable(puzz):
    flatten_puzz = []
    for row in puzz:
        for val in row:
            if val != 9:
                flatten_puzz.append(val)

    inversions = 0

    for i in range(len(flatten_puzz) - 1):
        for j in range(i + 1, len(flatten_puzz)):
            if flatten_puzz[i] > flatten_puzz[j]:
                inversions += 1

    if inversions % 2 == 0:
        return True
    else:
        return False


def solve_puzzle(initial_state):
    if not is_solvable(initial_state.data):
        print("Unsolvable Puzzle! No solution found.")
        return

    closed_states = []
    open_states = [initial_state]

    step = 0

    while open_states:
        current_state = open_states.pop(0)
        closed_states.append(current_state.data)

        print(f"\nStep {step}")
        print_state(current_state)

        if current_state.num_misplaced_tiles == 0:
            print("\nPuzzle Solved!")
            print_state(current_state)
            print(f"Number of Moves to solve the puzzle: {step}")
            break

        successors = generate_states(current_state)
        for state in successors:
            if state.data not in closed_states and state not in open_states:
                open_states.append(state)

        open_states.sort(key=lambda x: x.total_cost)
        step += 1


def get_user_input():
    print("Enter the initial 8-puzzle configuration (use 9 for blank tile):")
    initial_puzzle = []

    for i in range(3):
        while True:
            try:
                row_input = input(f"Enter row {i + 1} (comma-separated values, e.g., 1,2,3): ")
                row_values = [int(val) for val in row_input.split(",")]

                if len(row_values) != 3:
                    raise ValueError("Each row should have 3 values.")

                initial_puzzle.append(row_values)
                break
            except ValueError as e:
                print(f"Error: {e}. Please enter valid input.")

    return Puzzle(initial_puzzle)


puzz = get_user_input()
find_blank_pos(puzz)
find_total_cost(puzz)

solve_puzzle(puzz)

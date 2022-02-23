import numpy as np


# Node class to store the nodes
class Node:
    def __init__(self, pos, prev, state):
        self.pos = pos
        self.prev = prev
        self.state = state


# Function to print the states
def print_puzzle(puzzle):
    print('|', puzzle[0], '|', puzzle[1], '|', puzzle[2], '|')
    print('|', puzzle[3], '|', puzzle[4], '|', puzzle[5], '|')
    print('|', puzzle[6], '|', puzzle[7], '|', puzzle[8], '|')
    print('-------------')


# Function to perform right movement
def ActionMoveRight(puzzle, element):
    temp_puz = puzzle.copy()
    moved = False
    if (element + 1) % np.sqrt(len(temp_puz)) != 0:
        temp_ele = temp_puz[element + 1]
        temp_puz[element + 1] = temp_puz[element]
        temp_puz[element] = temp_ele

        return temp_puz, element + 1, not moved
    else:
        return None, None, moved


# Function to perform left movement
def ActionMoveLeft(puzzle, element):
    temp_puz = puzzle.copy()
    moved = False
    if (element + 1) % np.sqrt(len(temp_puz)) != 1:
        temp_ele = temp_puz[element - 1]
        temp_puz[element - 1] = temp_puz[element]
        temp_puz[element] = temp_ele

        return temp_puz, element - 1, not moved
    else:
        return None, None, moved


# Function to perform up movement
def ActionMoveUp(puzzle, element):
    temp_puz = puzzle.copy()
    moved = False
    if not 0 <= element <= (np.sqrt(len(temp_puz)) - 1):
        sq_len = int(np.sqrt(len(temp_puz)))
        temp_ele = temp_puz[element - sq_len]
        temp_puz[element - sq_len] = temp_puz[element]
        temp_puz[element] = temp_ele

        return temp_puz, element - sq_len, not moved
    else:
        return None, None, moved


# Function to perform down movement
def ActionMoveDown(puzzle, element):
    temp_puz = puzzle.copy()
    moved = False
    if not (len(temp_puz) - np.sqrt(len(temp_puz))) <= element <= (len(temp_puz) - 1):
        sq_len = int(np.sqrt(len(temp_puz)))
        temp_ele = temp_puz[element + sq_len]
        temp_puz[element + sq_len] = temp_puz[element]
        temp_puz[element] = temp_ele

        return temp_puz, element + sq_len, not moved
    else:
        return None, None, moved


# Global variables to store the nodes, states, visited states and yet to visit states
node_list = np.array([])
visited = np.array([])
not_visited = np.array([0])
states_list = np.array([])
path = np.array([])


# Function to solve the puzzle
def solve(puzzle, goal):
    puzzle = puzzle.T.flatten()
    position = np.where(puzzle == 0)[0][0]
    global node_list
    global visited
    global not_visited
    global states_list

    node_list = np.append(node_list, Node(position, None, puzzle))
    states_list = np.append(states_list, int("".join(map(str, puzzle))))

    goal = goal.T.flatten()
    isGoal = False

    puzzle_copy = puzzle.copy()
    node_idx = 0
    parent = 0
    counter = 0

    while not isGoal:
        counter += 1
        visited = np.append(visited, not_visited[0])
        not_visited = np.delete(not_visited, 0)

        temp_move, position_new, moved = ActionMoveDown(puzzle_copy, position)
        if moved and not isGoal and not (int("".join(map(str, temp_move))) in states_list):
            node_list = np.append(node_list, Node(position_new, parent, temp_move))
            states_list = np.append(states_list, int("".join(map(str, temp_move))))

            node_idx += 1
            if (goal == temp_move).all():
                isGoal = True
            not_visited = np.append(not_visited, node_idx)

        temp_move, position_new, moved = ActionMoveUp(puzzle_copy, position)
        if moved and not isGoal and not (int("".join(map(str, temp_move))) in states_list):
            node_list = np.append(node_list, Node(position_new, parent, temp_move))
            states_list = np.append(states_list, int("".join(map(str, temp_move))))

            node_idx += 1
            if (goal == temp_move).all():
                isGoal = True
            not_visited = np.append(not_visited, node_idx)

        temp_move, position_new, moved = ActionMoveRight(puzzle_copy, position)

        if moved and not isGoal and not (int("".join(map(str, temp_move))) in states_list):
            node_list = np.append(node_list, Node(position_new, parent, temp_move))
            states_list = np.append(states_list, int("".join(map(str, temp_move))))

            node_idx += 1
            if (goal == temp_move).all():
                isGoal = True
            not_visited = np.append(not_visited, node_idx)

        temp_move, position_new, moved = ActionMoveLeft(puzzle_copy, position)

        if moved and not isGoal and not (int("".join(map(str, temp_move))) in states_list):
            node_list = np.append(node_list, Node(position_new, parent, temp_move))
            states_list = np.append(states_list, int("".join(map(str, temp_move))))

            node_idx += 1
            if (goal == temp_move).all():
                isGoal = True
            not_visited = np.append(not_visited, node_idx)

        if not_visited.size == 0:
            print("Unsolvable Initial State")
            break
        puzzle_copy = node_list[not_visited[0]].state.copy()
        position = node_list[not_visited[0]].pos.copy()
        parent = not_visited[0]

    print("Solved!")

    global path

    backtracker()

    nodePath_file = open('nodePath.txt', 'w')
    for element in reversed(path):
        new_element = element.reshape(3, 3).T
        new_element = new_element.flatten()
        nodePath_file.writelines('%s ' % str(elements) for elements in new_element)
        nodePath_file.writelines('\n')
        print_puzzle(element)
    nodePath_file.close

    nodes_file = open('Nodes.txt', 'w')
    for nodes in node_list:
        new_elements = nodes.state.reshape(3, 3).T
        new_elements = new_elements.flatten()
        nodes_file.writelines('%s ' % str(elements_n) for elements_n in new_elements)
        nodes_file.writelines('\n')
    nodes_file.close

    nodesInfo_file = open('NodesInfo.txt', 'w')
    nodesInfo_file.write("Node_index\t  Parent_Node_index\t\tCost\n")
    for iter_num in node_list:
        nodesInfo_file.write(str(np.where(node_list == iter_num)[0][0]) + "\t\t\t")
        nodesInfo_file.write(str(iter_num.prev) + '\t\t\t0\n')
    nodesInfo_file.close()


# Backtracking Algorithm
def backtracker():
    itr = -1

    global path
    path = np.array([node_list[-1].state])

    while node_list[itr].prev is not None:
        itr = node_list[itr].prev
        path = np.append(path, [node_list[itr].state], axis=0)


if __name__ == "__main__":
    init_mat = np.array([[4, 7, 0], [1, 2, 8], [3, 5, 6]])  # Test case 1
    # init_mat = np.array([[1, 4, 7], [5, 0, 8], [2, 3, 6]])  # Test case 2

    goal_state = np.array([[1, 4, 7], [2, 5, 8], [3, 6, 0]])  # Goal State

    solve(init_mat, goal_state)

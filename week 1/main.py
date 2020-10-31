# Challenge: Write a piece of Python code which takes a problem representation and prints out the
# corresponding search tree up to a specified depth. Then, alter your code to check if the goal has
# been reached and halt when it has, printing only the tree up to the goal state.

# problem representation
# states
# initial state
# actions
# path cost
# goal test

# actions

def pour_to_small(x, y):
    # pre-conditions
    if x != 0:
        raise ValueError("5L cannot be empty when pouring")
    if y == 2:
        raise ValueError("2L is full already")
    # post-conditions
    p = min(x, 2-y)
    return (x-p, y+p)


def pour_to_big(x, y):
    # pre-conditions
    if x != 5:
        raise ValueError("5L is full already")
    if y != 0:
        raise ValueError("2L cannot be empty when pouring")
    # post-conditions
    p = min(5-x, y)
    return (x+p, y-p)


def dispose_small(x, y):
    # pre-conditions
    if y == 0:
        raise ValueError("Already empty")
    # post-conditions
    return (x, 0)


def dispose_big(x, y):
    # pre-conditions
    if x == 0:
        raise ValueError("Already empty")
    # post-conditions
    return (0, y)


actions = [
    pour_to_small,
    pour_to_big,
    dispose_small,
    dispose_big
]


def goal_test(x, y):
    if y == 1:
        return True
    return False


def problem_representation_solver(actions: list[tuple], init_state: tuple, goal_test, max_depth: int):

    # successor function
    def successor_func(state):
        result = []
        for func in range(actions):
            try:
                newState = func(state)
                result.append((func, newState))
            except:
                pass
        return result

    # variables
    states = [init_state, ]
    goal = False

    output = ""
    for cur_depth in range(max_depth):
        output += "Depth: %d " % cur_depth

        # loop through each state
        for cur_state in states:
            # check if its okay
            goal = goal_test(cur_state)
            if goal:
                return output
            successor_func(states[cur_state][1])

        output += states

        output += "\n"
    return output


print(problem_representation_solver(actions, (5, 0), goal_test, 2))

import queue

a_graph = {'A': ['B', 'C'], 'B': ['D'], 'C':['A'], 'D':[]}

class problem:
    def __init__(self, init_node, goal_node, graph):
        self.init = init_node
        self.goal = goal_node
        self.graph = graph
    
    def is_goal(self, state):
        return state == self.goal

def tree_search(problem):
    print('unknown search')
    class node:
        def __init__(self, state, parent_node, action, path_cost, depth):
            self.state = state
            self.parent_node = parent_node
            self.action = action
            self.path_cost = path_cost
            self.depth = depth

    fringe = []

    def make_node(state, problem):
        return node(problem.init, 0, problem.graph[problem.init], 0, 0)

    def get_solution(cur_node):
        if cur_node == 0:
            return
        print(cur_node.state)
        get_solution(cur_node.parent_node)

    def expand(parent_node, problem):
        possible_states = problem.graph[parent_node.state]
        for state in possible_states:
            new_node = node(state, parent_node, problem.graph[state], 0, parent_node.depth+1)
            fringe.append(new_node)



    fringe.append(make_node(problem.init, problem))
    while len(fringe) != 0:
        cur_node = fringe.pop()
        print("checking node: " + cur_node.state)
        if problem.is_goal(cur_node.state):
            return get_solution(cur_node)
        expand(cur_node, problem)

def tree_search_breadth_first(problem):
    print("breadth first search")
    class node:
        def __init__(self, state, parent_node, action, path_cost, depth):
            self.state = state
            self.parent_node = parent_node
            self.action = action
            self.path_cost = path_cost
            self.depth = depth

    fringe = queue.Queue()

    def make_node(state, problem):
        return node(problem.init, 0, problem.graph[problem.init], 0, 0)

    def get_solution(cur_node):
        if cur_node == 0:
            return
        print(cur_node.state)
        get_solution(cur_node.parent_node)

    def expand(parent_node, problem):
        possible_states = problem.graph[parent_node.state]
        for state in possible_states:
            new_node = node(state, parent_node, problem.graph[state], 0, parent_node.depth+1)
            fringe.put(new_node)



    fringe.put(make_node(problem.init, problem))
    while fringe.empty() == False:
        cur_node = fringe.get()
        print("checking node: " + cur_node.state)
        if problem.is_goal(cur_node.state):
            return get_solution(cur_node)
        expand(cur_node, problem)

tree_search_breadth_first(problem('A', 'D', a_graph))
#tree_search(problem('A', 'D', a_graph))

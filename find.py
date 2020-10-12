import queue

a_graph = {'A': ['B', 'C'], 'B': ['D'], 'C':[], 'D':[]}

class problem:
    """
    A class to represent a problem representation

    Attributes
    ----------
    init: str
        The initial state
    goal: str
        The goal state
    graph: list
        All possible permutations
    
    Methods
    -------
    is_goal(state):
        Checks if the state satisfies some specific requirement for the problem
    """
    def __init__(self, init_node, goal_node, graph):
        self.init = init_node
        self.goal = goal_node
        self.graph = graph
    
    def is_goal(self, state):
        return state == self.goal

def tree_search(problem, search_type):
    """
    perform either a depth-first search or a breadth-search search
    on a problem representation.

    Parameters:
        problem (problem): A problem representation
        search_type (str): Either "depth" or "breadth"
    """
    class node:
        """
        A class representing a state with metadata

        Attributes
        ----------
        state: str
            Represents current information about the state.
        parent_node: node
            The precursor node.
        action:
            Possible reachable states, that are possible from current state.
        path_cost:
            The cost of the path.
        depth:
            It's current depth in the tree/graph.
        """
        def __init__(self, state, parent_node, action, path_cost, depth):
            self.state = state
            self.parent_node = parent_node
            self.action = action
            self.path_cost = path_cost
            self.depth = depth

    if search_type == "breadth":
        print("breadth-first search")
        fringe = queue.Queue()
    else:
        print("depth-first search")
        fringe = queue.LifoQueue()
    

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
        if problem.is_goal(cur_node.state):
            return get_solution(cur_node)
        expand(cur_node, problem)

tree_search(problem('A', 'D', a_graph), "depth")
tree_search(problem('A', 'D', a_graph), "breadth")

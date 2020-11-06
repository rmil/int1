import queue

class arc():
    def __init__(self, dst, cost):
        self.dst = dst
        self.cost = cost

class castle():
    def __init__(self, name, neighbours, sld, altitude):
        self.name = name
        self.neighbours = neighbours
        self.sld = sld # straight line distance, hardcoded distance between node and J currently
        self.altitude = altitude
        self.heuristic = sld

        # priority queue needs < to be implemented
    def __lt__(self, other):
        return (self.name < other.name)
    
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name


A = castle('A', {}, 30, 0)
B = castle('B', {}, 20, 200)
C = castle('C', {}, 20, 600)
D = castle('D', {}, 20, 100)
E = castle('E', {}, 15, 300)
F = castle('F', {}, 10, 300)
G = castle('G', {}, 5, 100)
H = castle('H', {}, 5, 500)
I = castle('I', {}, 5, 400)
J = castle('J', {}, 0, 500)

A.neighbours = {B: 5, C: 5, D: 5}
B.neighbours = {A: 5, F: 5}
C.neighbours = {A: 5, E: 5}
D.neighbours = {A: 5, E: 10, F: 10}
E.neighbours = {C: 5, D: 5, G: 10, H: 5}
F.neighbours = {B: 5, D: 10, I: 5}
G.neighbours = {E: 10, H: 5, J: 5}
H.neighbours = {E: 5, G: 5, J: 5}
I.neighbours = {F: 5, J: 5}
J.neighbours = {G: 5, H: 5, I: 5}


# Breadth-first search, converted to Uniform cost search
def ucs(start, goal):
    visited = []
    fringe = queue.PriorityQueue()
    fringe.put((0, start))

    while not fringe.empty():
        (cost, node) = fringe.get()
        if node not in visited:
            visited.append(node)

            if node == goal:
                return((cost, visited))
            for neighbour in node.neighbours.items():
                if neighbour[0] not in visited:
                    new_cost = cost + neighbour[1]
                    new_node = neighbour[0]
                    fringe.put((new_cost, new_node))
    return (visited)

def a_star(start, goal, heuristic):
    visited = []
    fringe = queue.PriorityQueue()
    fringe.put((start.heuristic, 0, start))

    while not fringe.empty():
        (_, cost, node) = fringe.get()
        if node not in visited:
            visited.append(node)

            if node == goal:
                return((cost, visited))
            for neighbour in node.neighbours.items():
                if neighbour[0] not in visited:
                    new_cost = cost + neighbour[1]
                    new_node = neighbour[0]
                    print(str(node) + " -> " + str(neighbour) + " = " + str(heuristic(node, new_node, False) + new_cost))
                    fringe.put((heuristic(node, new_node, True) + new_cost, new_cost, new_node))
    return (visited)

def naismith(src, dst, enable_alt):
    alt_time = 0
    flat_time = 0
    if enable_alt:
        alt_time = (src.altitude - dst.altitude) / 600
        flat_time = src.neighbours[dst] / 5
    else:
        flat_time = src.neighbours[dst]
    return alt_time + flat_time 

print(ucs(A, J))
print(a_star(A, J, naismith))

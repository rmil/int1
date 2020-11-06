from queue import PriorityQueue

class Castle():
  def __init__(self, name, 
                     neighbours, 
                     SLD, 
                     altitude):
    self.name = name
    self.neighbours = neighbours
    self.SLD = SLD
    self.heur_value = SLD    # default to SLD for heuristic value
    self.altitude = altitude

  def setNeighbours(self, neighbours):
    self.neighbours = neighbours

  def setHeuristic(self, heur_value):
    self.heur_value = heur_value

  def __str__(self):
    return(self.name)
  def __repr__(self):
    return(self.name)

  # needed for priority queue implementation
  # if two path costs are equal, return the first 
  # castle alphabetically
  def __lt__(self, other):
    return(self.name < other.name)

A = Castle("A", {}, 30, 0)
B = Castle("B", {}, 20, 200)
C = Castle("C", {}, 20, 600)
D = Castle("D", {}, 20, 100)
E = Castle("E", {}, 15, 300)
F = Castle("F", {}, 10, 300)
G = Castle("G", {}, 5, 100)
H = Castle("H", {}, 5, 500)
I = Castle("I", {}, 5, 400)
J = Castle("J", {}, 0, 500)

A.setNeighbours({B: 5, C: 5, D: 5})
B.setNeighbours({A: 5, F: 5})
C.setNeighbours({A: 5, E: 5})
D.setNeighbours({A: 5, E: 5, F: 10})
E.setNeighbours({C: 5, D: 5, G: 10, H: 5})
F.setNeighbours({B: 5, D: 10, I:5})
G.setNeighbours({E: 10, H: 5, J: 5})
H.setNeighbours({E: 5, G: 5, J:5})
I.setNeighbours({F: 5, J: 5})
J.setNeighbours({G: 5, H: 5, I:5})


# Breadth-first search from last week, converted to UCS
def ucs(start, goal):
    visited = []
    fringe = PriorityQueue()
    fringe.put((0, start))

    while not fringe.empty():
        (cost, node) = fringe.get()
        if node not in visited:
            visited.append(node)

            if node == goal:
                return((cost,visited))
            for neighbour in node.neighbours.items():
                if neighbour[0] not in visited:
                    new_cost = cost + neighbour[1]
                    new_node = neighbour[0]
                    fringe.put((new_cost, new_node))
    return(visited)

def aStar(start, goal):
    visited = []
    pathcost = 0
    fringe = PriorityQueue()
    # (a*value, pathcost, node)
    fringe.put((start.heur_value, 0, start))

    while not fringe.empty():
        (_, cost, node) = fringe.get()
        if node not in visited:
            visited.append(node)

            if node == goal:
                return((cost,visited))
            for neighbour in node.neighbours.items():
                if neighbour[0] not in visited:
                    new_cost = cost + neighbour[1]
                    new_node = neighbour[0]
                    fringe.put((new_node.heur_value + new_cost, new_cost, new_node))
    return(visited)


def naismith(castle):
  global J
  alt_time      = (J.altitude - castle.altitude) / 600
  flat_time     = castle.SLD / 5
  naismith_val  = flat_time + alt_time
  return(naismith_val)



print(ucs(A, J))
print(aStar(A, J))


# this code replaces the straight-line distance 
# heuristic value with the Naismith's rule 
# heuristic value

all_castles = [A,B,C,D,E,F,G,H,I,J]
for castle in all_castles:
  castle.heur_value = naismith(castle)

print(aStar(A,J))
  

# timing code as before
import time
import numpy as np
tic = []
tac = []
toc = []

for i in range(1,10):
  tic.append(time.perf_counter())
  ucs(A,J)
  tac.append(time.perf_counter())
  aStar(A,J)
  toc.append(time.perf_counter())

diff1 = np.median(np.subtract(tac,tic))
diff2 = np.median(np.subtract(toc,tac))

print("UCS " + str(diff1))
print("A* " + str(diff2))

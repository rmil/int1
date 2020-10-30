pixeldale = {
            'A': ([('B', 5), ('C', 5), ('D', 5)], 0),
            'B': ([('A', 5), ('F', 5)], 200),
            'C': ([('A', 5), ('E', 5)], 600),
            'D': ([('A', 5), ('E', 10), ('F', 10)], 100),
            'E': ([('C', 5), ('D', 5), ('G', 10), ('H', 5)], 300),
            'F': ([('B', 5), ('D', 10), ('I', 5)], 300),
            'G': ([('E', 10), ('H', 5), ('J', 5)], 100),
            'H': ([('E', 5), ('G', 5), ('J', 5)], 500),
            'I': ([('F', 5), ('J', 5)], 400),
            'J': ([('G', 5), ('H', 5), ('I', 5)], 500)
            }

class arc():
    def __init__(self, dst, cost):
        self.dst = dst
        self.cost = cost

class castle():
    def __init__(self, name, routes, heuristic):
        self.name = name
        self.arc = routes
        self.heuristic = heuristic

castles = []
for location, attributes in pixeldale.items():
    routes = []
    cur_altitude = attributes[1]
    for path in attributes[0]:
        duration = 0
        dst_altitude = pixeldale[path[0]][1]
        if dst_altitude > cur_altitude:
            # we're going up
            difference = dst_altitude - cur_altitude
            duration += (difference / 100) * 10 # amount of minutes extra
        duration += path[1] * 60 
        a_path = arc(path[0], duration)
        routes.append(a_path)
    

    castles.append(castle(location, routes, 0))

print(castles)
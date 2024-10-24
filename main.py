import math
import sys

# Increase recursion limit if necessary
sys.setrecursionlimit(2000)

# Global counter for Node instances
node_count = 0

# Coordinates of cities (same as before)
city_coordinates = {
    'Arad': (46.1833, 21.3167),
    'Bucharest': (44.4325, 26.1039),
    'Craiova': (44.3167, 23.8000),
    'Drobeta': (44.6369, 22.6597),
    'Eforie': (44.0584, 28.6336),
    'Fagaras': (45.8416, 24.9731),
    'Giurgiu': (43.9000, 25.9667),
    'Hirsova': (44.6894, 27.9457),
    'Iasi': (47.1622, 27.5889),
    'Lugoj': (45.6886, 21.9031),
    'Mehadia': (44.9041, 22.3645),
    'Neamt': (46.9759, 26.3819),
    'Oradea': (47.0722, 21.9211),
    'Pitesti': (44.8560, 24.8692),
    'Rimnicu Vilcea': (45.1047, 24.3750),
    'Sibiu': (45.7928, 24.1522),
    'Timisoara': (45.7597, 21.2300),
    'Urziceni': (44.7165, 26.6415),
    'Vaslui': (46.6407, 27.7277),
    'Zerind': (46.6167, 21.5167),
}

# Function to calculate the Haversine distance (same as before)
def haversine_distance(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0)**2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2.0)**2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    radius = 6371.0  # Earth's radius in kilometers

    distance = radius * c

    return distance

# Create the heuristics dictionary (same as before)
heuristics = {}
cities = list(city_coordinates.keys())
for city1 in cities:
    heuristics[city1] = {}
    for city2 in cities:
        if city1 == city2:
            heuristics[city1][city2] = 0.0
        else:
            coord1 = city_coordinates[city1]
            coord2 = city_coordinates[city2]
            distance = haversine_distance(coord1, coord2)
            heuristics[city1][city2] = distance

# Graph of Romanian cities with bidirectional edges (same as before)
graph = {
    'Arad': [('Zerind', 75), ('Sibiu', 140), ('Timisoara', 118)],
    'Bucharest': [('Fagaras', 211), ('Pitesti', 101), ('Giurgiu', 90), ('Urziceni', 85)],
    'Craiova': [('Drobeta', 120), ('Rimnicu Vilcea', 146), ('Pitesti', 138)],
    'Drobeta': [('Mehadia', 75), ('Craiova', 120)],
    'Eforie': [('Hirsova', 86)],
    'Fagaras': [('Sibiu', 99), ('Bucharest', 211)],
    'Giurgiu': [('Bucharest', 90)],
    'Hirsova': [('Urziceni', 98), ('Eforie', 86)],
    'Iasi': [('Neamt', 87), ('Vaslui', 92)],
    'Lugoj': [('Timisoara', 111), ('Mehadia', 70)],
    'Mehadia': [('Lugoj', 70), ('Drobeta', 75)],
    'Neamt': [('Iasi', 87)],
    'Oradea': [('Zerind', 71), ('Sibiu', 151)],
    'Pitesti': [('Rimnicu Vilcea', 97), ('Craiova', 138), ('Bucharest', 101)],
    'Rimnicu Vilcea': [('Sibiu', 80), ('Pitesti', 97), ('Craiova', 146)],
    'Sibiu': [('Arad', 140), ('Oradea', 151), ('Fagaras', 99), ('Rimnicu Vilcea', 80)],
    'Timisoara': [('Arad', 118), ('Lugoj', 111)],
    'Urziceni': [('Bucharest', 85), ('Hirsova', 98), ('Vaslui', 142)],
    'Vaslui': [('Urziceni', 142), ('Iasi', 92)],
    'Zerind': [('Arad', 75), ('Oradea', 71)],
}
# Add reverse edges to make the graph bidirectional
for city in list(graph.keys()):
    for neighbor, cost in graph[city]:
        if neighbor not in graph:
            graph[neighbor] = []
        if (city, cost) not in graph[neighbor]:
            graph[neighbor].append((city, cost))

class Node:
    __slots__ = ('name', 'g', 'h', 'f', 'parent', 'visited')

    def __init__(self, name, g=0, h=0, f=0, parent=None):
        global node_count
        self.name = name
        self.g = g
        self.h = h
        self.f = f
        self.parent = parent
        self.visited = False
        node_count += 1  # Increment node count

    def __del__(self):
        global node_count
        node_count -= 1  # Decrement node count

    def __lt__(self, other):
        return self.f < other.f

def heuristic(node_name, goal_name):
    return heuristics.get(node_name, {}).get(goal_name, float('inf'))

def rbfs(node, goal, f_limit):
    print(f"Visiting Node: {node.name}, f: {node.f:.2f}, g: {node.g}, h: {node.h:.2f}, f_limit: {f_limit:.2f}")
    print(f"Current node count: {node_count}")
    if node.name == goal:
        return node, node.f

    successors = []
    for (child_name, cost) in graph.get(node.name, []):
        # Avoid cycles by checking the path from the root to the current node
        in_path = False
        current = node
        while current is not None:
            if current.name == child_name:
                in_path = True
                break
            current = current.parent
        if in_path:
            continue

        g = node.g + cost
        h = heuristic(child_name, goal)
        f = max(g + h, node.f)
        child_node = Node(child_name, g, h, f, parent=node)
        successors.append(child_node)
        print(f"  Generated Successor: {child_name}, f: {f:.2f}, g: {g}, h: {h:.2f}")
        print(f"  Current node count after successor creation: {node_count}")

    if not successors:
        return None, float('inf')

    while True:
        # Sort successors based on their f-values
        successors.sort(key=lambda n: n.f)
        best = successors[0]
        if best.f > f_limit:
            return None, best.f
        alternative = successors[1].f if len(successors) > 1 else float('inf')

        # Recursive call
        result, best.f = rbfs(best, goal, min(f_limit, alternative))

        # Update best in successors list
        successors[0] = best

        if result is not None:
            return result, best.f

        # If all successors have f-values greater than f_limit, return failure
        if all(s.f > f_limit for s in successors):
            return None, min(s.f for s in successors)

def reconstruct_path(node):
    path = []
    while node:
        path.append(node.name)
        node = node.parent
    return path[::-1]

def main():
    print("Available cities:")
    print(", ".join(sorted(city_coordinates.keys())))
    start_city = input("Enter the start city: ").strip()
    goal_city = input("Enter the goal city: ").strip()

    if start_city not in city_coordinates or goal_city not in city_coordinates:
        print("Invalid city names. Please enter valid cities from the list.")
        return

    h_start = heuristic(start_city, goal_city)
    start_node = Node(start_city, g=0, h=h_start, f=h_start)

    result, f = rbfs(start_node, goal_city, float('inf'))

    if result:
        path = reconstruct_path(result)
        total_cost = result.g
        print("Path found:", ' -> '.join(path))
        print(f"Total cost from {start_city} to {goal_city}: {total_cost}")
    else:
        print(f"No path found from {start_city} to {goal_city}")

    print(f"Final node count: {node_count}")

if __name__ == "__main__":
    main()

from Matroid import Matroid
from collections import defaultdict

###
### MAXIMUM COST FOREST
#we will represent graph by sets of edges {(0, 1), (2, 3), ...} and so on where (0, 1) represents an edge with endpoints of 0, 1
#assumes that if (0, 1) is included, then (1, 0) is not necessary (since it is implied) (should work fine when both are included)
#we have a forest if and only if there are no cycles
def is_forest(graph):
    def dfs_cycle(prev_vertex, vertex, adjacency, visited_vertices):
        neighbours = adjacency[vertex]
        for neighbour in neighbours:
            if neighbour == prev_vertex:
                continue
            else:
                #found a cycle
                if neighbour in visited_vertices:
                    return True
                else:
                    visited_vertices.add(neighbour)
                    #tries to find a cycle through the path from that neighbour, if found, then return True
                    #else continue the search
                    if dfs_cycle(vertex, neighbour, adjacency, visited_vertices):
                        return True
        return False

                
    ### determines adjacency relationship
    adjacency = defaultdict(list)
    vertices = set()
    for vertex1, vertex2 in graph:
        adjacency[vertex1].append(vertex2)
        adjacency[vertex2].append(vertex1)
        vertices.add(vertex1)
        vertices.add(vertex2)
    visited_vertices = set()
    for vertex in vertices:
        if vertex in visited_vertices:
            continue
        else:
            prev_vertex = None
            visited_vertices.add(vertex)
            if dfs_cycle(prev_vertex, vertex, adjacency, visited_vertices):
                return False
    return True

# graph = {
#     ("a", "b"),
#     ("a", "c"),
#     ("a", "d"),
#     ("b", "c"),
#     ("b", "d"),
#     ("c", "d")
# }

# costs = {
#     ("a", "b"): 2,
#     ("a", "c"): 4,
#     ("a", "d"): 7,
#     ("b", "c"): 1,
#     ("b", "d"): 3,
#     ("c", "d"): 5,
# }

# graph = {
#     (0, 1),
#     (0, 2),
#     (1, 2),
# }

# costs = {
#     (0, 1): -1,
#     (0, 2): -2,
#     (1, 2): -3,
# }

graph = {
    (0, 1),
    (0, 3),
    (0, 4),
    (1, 2),
    (1, 4),
    (2, 3),
    (2, 4),
    (3, 4)
}

costs = {
    (0, 1): -1,
    (0, 3): 6,
    (0, 4): 5,
    (1, 2): 10,
    (1, 4): -2,
    (2, 3): -1,
    (2, 4): -4,
    (3, 4): 4
}


Forests = Matroid(ground_set = graph)
# Forests.set_costs(costs)
Forests.is_independent = is_forest
print(Forests.max_cost_greedy(costs))
print(Forests.min_cost_greedy(costs))


    






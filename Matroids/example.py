from Matroid import Matroid
from collections import defaultdict
import numpy as np
from numpy.linalg import matrix_rank

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


# Forests = Matroid(ground_set = graph)
# # Forests.set_costs(costs)
# Forests.is_independent = is_forest
# print(Forests.max_cost_greedy(costs))
# print(Forests.min_cost_greedy(costs))


### UNIFORM MATROID

R = 2



def is_uniform_matroid(set):
    return len(set) <= R


###U_5^2
# Uniform_Matroid = Matroid(ground_set = frozenset({1, 2, 3, 4, 5}))
# Uniform_Matroid.is_independent = is_uniform_matroid
# Uniform_Matroid.form_independent_set()
# print(Uniform_Matroid.check_independent_sets())
# print(Uniform_Matroid.independent_set)




### LINEAR MATROID
### VECTOR_DICT (assigns index to column)

vector_dict = {
    1: np.array([2, 0, 0]),
    2: np.array([0, 1, 0]),
    3: np.array([0, 0, 1]),
    4: np.array([1, 0, 0]),
    5: np.array([0, 2, 2]),
    6: np.array([0, 0, 0])
}

def is_linear_matroid(index_set):
    if len(index_set) == 0:
        return True
    vector_lst = []
    for index in index_set:
        vector_lst.append(vector_dict[index])
    vector_tuple = tuple(vector_lst)
    matrix = np.vstack(vector_tuple).T
    return matrix_rank(matrix) == len(matrix[0])

# Linear_Matroid = Matroid(frozenset({1, 2, 3, 4, 5, 6}))
# Linear_Matroid.is_independent = is_linear_matroid
# Linear_Matroid.form_independent_set()
# print(Linear_Matroid.check_independent_sets())


# Matroid_1 = Matroid(ground_set = frozenset({1, 2, 3, 4}), circuits = frozenset({frozenset({4}), frozenset({1, 2, 3})}))
# Matroid_1.form_independent_set_from_circuits()
# print(Matroid_1.independent_set)
# print(Matroid_1.check_independent_sets())
# print(Matroid_1.check_circuits())


Matroid_2 = Matroid(ground_set = frozenset({1, 2, 3, 4}), bases = frozenset({frozenset({1, 2}), frozenset({1, 3}), frozenset({2, 3})}))
Matroid_2.form_independent_set_from_bases()
print(Matroid_2.independent_set)
print(Matroid_2.check_independent_sets())
print(Matroid_2.check_bases())




    






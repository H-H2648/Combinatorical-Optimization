from collections import defaultdict
from copy import deepcopy

class Graph:
    #vertices = any collection of objects
    #where n the value vertex_size
    #takes edges of the form [((vertex1, vertex2), weight), ...]
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges
        self.adjacency = defaultdict(list)
        for edge, _ in self.edges:
            vertex1, vertex2 = edge
            self.adjacency[vertex1].append(vertex2)
            self.adjacency[vertex2].append(vertex1)

    ###BFS search if there is a path from two vertices
    ###returns True, path if exists
    ###returns False, None if it does not
    def BFS(self, vertex1, vertex2):
        vertices_visited = {vertex1}
        ### records the neighbours of the "current" vertices and its path so far
        next_steps = {}
        for neighbour in self.adjacency[vertex1]:
            next_steps[neighbour] = [vertex1, neighbour]
        while len(next_steps) > 0:
            next_next_steps = {}
            for neighbour in next_steps:
                path = next_steps[neighbour]
                for neigh_neighbour in self.adjacency[neighbour]:
                    if neigh_neighbour == vertex2:
                        return True, (path + [vertex2])
                    if neigh_neighbour in vertices_visited:
                        continue
                    else:
                        next_next_steps[neigh_neighbour] = path + [neigh_neighbour]
                        vertices_visited.add(neighbour)
            next_steps = next_next_steps
        return False, None

        
    ### basic algorithm first assuming bipartite
    def match(self):
        def continue_tree(even_tree_vertices, odd_tree_vertices, adjacency, vertices_to_match):
            for vertex in even_tree_vertices:
                for neighbour in adjacency[vertex]:
                    if not(neighbour in odd_tree_vertices) and (neighbour in vertices_to_match):
                        return True, (vertex, neighbour)
            return False, None

        def unwrap(vertex1, vertex2, match_edge_set, new_match_edge_set, adjacency):
            #### we have new_match_edge_set because we usually use this function with loop respect to match_edge_set and we cannot change the size of match_edge_set when looping
            ### assumes (vertex1, vertex2) in match_edge_set
            if type(vertex1) == tuple:
                cycle = vertex1
                for ii in range(len(cycle)):
                    vertex = cycle[ii]
                    if vertex2 in adjacency[vertex]:
                        unwrap(vertex, vertex2, match_edge_set, new_match_edge_set, adjacency)
                        break
                cycle_lst = list(cycle)
                other_elem = cycle_lst[ii+1:] + cycle_lst[:ii]
                for ii in range(0, len(other_elem), 2):
                    unwrap(other_elem[ii], other_elem[ii+1], match_edge_set, new_match_edge_set, adjacency)
            elif type(vertex2) == tuple:
                cycle = vertex2
                for ii in range(len(cycle)):
                    vertex = cycle[ii]
                    if vertex1 in adjacency[vertex]:
                        unwrap(vertex1, vertex, match_edge_set, new_match_edge_set, adjacency)
                        break
                cycle_lst = list(cycle)
                other_elem =  cycle_lst[ii+1:] + cycle_lst[:ii]
                for ii in range(0, len(other_elem), 2):
                    unwrap(other_elem[ii], other_elem[ii+1], match_edge_set, new_match_edge_set, adjacency)
            else:
                new_match_edge_set.add((vertex1, vertex2))

        def match_root_node(root_node, match_edge_set, adjacency):
            if type(root_node) == tuple:
                for ii in range(1, len(root_node), 2):
                    unwrap(root_node[ii], root_node[ii+1], match_edge_set, match_edge_set, adjacency)
                match_root_node(root_node[0], match_edge_set, adjacency)
                     

                


        match_edge_set = set()
        match_partner = {}
        vertices_to_match = set(self.vertices)
        exposed_vertices = set(vertices_to_match)
        adjacency = deepcopy(self.adjacency)
        while len(exposed_vertices) > 0:
            #we just pick the first exposed vertex as exposed_vertex
            for exposed_vertex in exposed_vertices:
                break
            root_node = exposed_vertex
            # alternating_tree_edges = set()
            even_tree_vertices = {root_node}
            odd_tree_vertices = set()
            ### tree_path_history: for each vertex, shows the path from the rootnode to that vertex
            tree_path_history = {}
            tree_path_history[root_node] = [root_node]
            extendable, extend_edge = continue_tree(even_tree_vertices, odd_tree_vertices, adjacency, vertices_to_match)
            while extendable:
                # print(f"B(T): {even_tree_vertices}")
                # print(f"A(T): {odd_tree_vertices}")
                even_vertex, odd_vertex = extend_edge
                # print(f"found new edge: {extend_edge}")
                if not(odd_vertex in even_tree_vertices) and (odd_vertex in exposed_vertices):
                    # print("augmenting...")
                    ###we have an augmenting path
                    tree_path_history[odd_vertex] = tree_path_history[even_vertex] + [odd_vertex]
                    even_parity = True
                    augmented_path = tree_path_history[odd_vertex] 
                    for ii in range(len(augmented_path)- 1):
                        if even_parity:
                            match_edge_set.add((augmented_path[ii], augmented_path[ii+1]))
                            match_partner[augmented_path[ii]] = augmented_path[ii+1]
                            match_partner[augmented_path[ii+1]] = augmented_path[ii]
                            even_parity = False
                        else:
                            #remove the edge, it could be in one of the two ways so remove both
                            match_edge_set.discard((augmented_path[ii], augmented_path[ii+1]))
                            match_edge_set.discard((augmented_path[ii+1], augmented_path[ii]))
                            ### no need to change match_partner because the above case will do it
                            even_parity = True
                        ##we add the root_node and the final vertex of the augmented_path to the atching
                    exposed_vertices.discard(augmented_path[0])
                    exposed_vertices.discard(augmented_path[-1])
                    # print(f"new match: {match_edge_set}")
                    if len(exposed_vertices) == 0:
                        new_match_edge_set = set()
                        for edge in match_edge_set:
                            x, y = edge
                            unwrap(x, y, match_edge_set, new_match_edge_set, adjacency)
                        return new_match_edge_set
                    else:
                        for exposed_vertex in exposed_vertices:
                            break
                        root_node = exposed_vertex
                        even_tree_vertices = {root_node}
                        odd_tree_vertices = set()
                        tree_path_history = {root_node: [root_node]}

                    
                elif not(odd_vertex in  even_tree_vertices) and not(odd_vertex in exposed_vertices):
                    # print("extending...")
                    odd_tree_vertices.add(odd_vertex)
                    tree_path_history[odd_vertex] = tree_path_history[even_vertex] + [odd_vertex]
                    even_tree_vertices.add(match_partner[odd_vertex])
                    tree_path_history[match_partner[odd_vertex]] = tree_path_history[odd_vertex] + [match_partner[odd_vertex]]

                #odd cycle
                else:
                    # print("finding cycle..")
                    path1 = tree_path_history[even_vertex]  
                    path2 = tree_path_history[odd_vertex]
                    ##finds the last point of intersection:
                    diverged=False
                    for ii in range(min(len(path1), len(path2))):
                        if path1[ii] != path2[ii]:
                            diverged=True
                            break
                    if diverged:
                        last_intersect = ii-1
                        cycle_part1 = path1[last_intersect:]
                        cycle_part2 = path2[last_intersect+1:]
                        cycle_part2.reverse()   
                        cycle_lst = cycle_part1 + cycle_part2
                    else:
                        if len(path2) > len(path1):
                            cycle_lst = path2 
                        else:
                            cycle_lst = path1
                    cycle = tuple
                    cycle = tuple(cycle_lst)
                    if root_node in cycle:
                        root_node = cycle
                    # print(f"found a cycle: {cycle}")
                    cycle_matched = False
                    removable_edges = set()
                    addable_edges = set()
                    for edge in match_edge_set:
                        x, y = edge
                        x_in_cycle = (x in cycle)
                        y_in_cycle = (y in cycle)
                        if (x_in_cycle) and not(y_in_cycle):
                            removable_edges.add(edge)
                            addable_edges.add((cycle, y))
                            cycle_matched = True
                        elif not(y_in_cycle) and (x_in_cycle):
                            removable_edges.add(edge)
                            addable_edges.add((x, cycle))
                            cycle_matched = True
                        elif x_in_cycle and y_in_cycle:
                            removable_edges.add(edge)
                    if not(cycle_matched):
                        exposed_vertices.add(cycle)
                    match_edge_set  = match_edge_set.difference(removable_edges)
                    match_edge_set = match_edge_set.union(addable_edges)
                    for vertex in cycle:
                        if vertex in exposed_vertices:
                            exposed_vertices.remove(vertex)
                    for vertex in tree_path_history:
                        path = tree_path_history[vertex] 
                        index = 0
                        while (index < len(path)) and not(path[index] in cycle):
                            index +=1
                        if index == len(path):
                            continue
                        else: 
                            start_cycle_index = index
                        while (index < len(path)) and (path[index] in cycle):
                            index +=1
                        end_cycle_index = index
                        new_path = path[:start_cycle_index] + [cycle] + path[end_cycle_index:]
                        tree_path_history[vertex] = new_path
                    for vertex in cycle:
                        neighbours = adjacency[vertex]
                        for neighbour in neighbours:
                            if not(neighbour in adjacency[cycle]) and not(neighbour in cycle):
                                adjacency[cycle].append(neighbour)
                                adjacency[neighbour].append(cycle)
                    #even_vertex is on the cycle
                    cycle_history_path = tree_path_history[even_vertex]     
                    for vertex in cycle:
                        del tree_path_history[vertex]  
                        vertices_to_match.discard(vertex) 
                        even_tree_vertices.discard(vertex)
                        odd_tree_vertices.discard(vertex)       
                    tree_path_history[cycle] = cycle_history_path     
                    vertices_to_match.add(cycle)
                    even_tree_vertices.add(cycle)
                extendable, extend_edge = continue_tree(even_tree_vertices, odd_tree_vertices, adjacency, vertices_to_match)

            #Tree Frustrated
            vertices_to_match = vertices_to_match.difference(even_tree_vertices)
            vertices_to_match = vertices_to_match.difference(odd_tree_vertices)
            exposed_vertices = vertices_to_match
            match_root_node(root_node, match_edge_set, adjacency)
            if len(exposed_vertices) == 0:
                new_match_edge_set = set()
                for edge in match_edge_set:
                    x, y = edge
                    unwrap(x, y, match_edge_set, new_match_edge_set, adjacency)
                # print(adjacency)
                return new_match_edge_set
            
            


            






    
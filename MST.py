class MST:
    #for now takes in inputs of vertices = [0, 1, ..., n-1]
    #where n the value vertex_size
    #takes edges of the form [((vertex1, vertex2), weight), ...]
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges
    

    #naive kruskal
    #return minimum spanning tree in the form of a list of edges as well as its edges
    def naive_kruskal(self):
        mst = []
        connected_components = []
        for vertex in range(self.vertices):
            connected_components.append(vertex)
        sorted_edges = sorted(self.edges, key = lambda x: x[1])
        for edge, weight in sorted_edges:
            vertex1, vertex2 = edge[0], edge[1]
            if connected_components[vertex1] != connected_components[vertex2]:
                mst.append((edge, weight))
                component_vertex2 = connected_components[vertex2]
                for vertex in range(self.vertices):
                    if connected_components[vertex] == component_vertex2:
                        connected_components[vertex] = connected_components[vertex1]
        return mst
            
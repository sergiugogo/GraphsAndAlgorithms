from Lab01 import Graph
from copy import deepcopy


def is_complete(graph):
    vertices = graph.get_vertices()
    n = len(vertices)
    for u in vertices:
        neighbors = set(graph.out_neighbors(u)) | set(graph.in_neighbors(u))
        if len(neighbors) != n - 1:
            return False
    return True


def is_complete_bipartite(graph):
    vertices = graph.get_vertices()
    visited = set()
    color = {}

    def bfs(start):
        queue = [start]
        color[start] = 0
        while queue:
            u = queue.pop(0)
            for v in set(graph.out_neighbors(u)) | set(graph.in_neighbors(u)):
                if v not in color:
                    color[v] = 1 - color[u]
                    queue.append(v)
                elif color[v] == color[u]:
                    return False
        return True

    for v in vertices:
        if v not in color:
            if not bfs(v):
                return False

    part1 = [v for v in color if color[v] == 0]
    part2 = [v for v in color if color[v] == 1]

    for u in part1:
        for v in part2:
            if not graph.is_edge(u, v) and not graph.is_edge(v, u):
                return False

    # Ensure no edges within partitions
    for u in part1:
        for v in part1:
            if u != v and (graph.is_edge(u, v) or graph.is_edge(v, u)):
                return False
    for u in part2:
        for v in part2:
            if u != v and (graph.is_edge(u, v) or graph.is_edge(v, u)):
                return False

    return True


def reduce_graph(graph):
    g = deepcopy(graph)
    changed = True

    while changed:
        changed = False
        for vertex in list(g.get_vertices()):
            neighbors = list(set(g.out_neighbors(vertex)) | set(g.in_neighbors(vertex)))
            if len(neighbors) == 2:
                u, v = neighbors
                if not g.is_edge(u, v) and not g.is_edge(v, u):
                    g.remove_vertex(vertex)
                    g.add_edge(u, v)
                    changed = True
                    break
    return g


def is_homeomorphic_to_complete_or_bipartite(graph):
    if graph.directed:
        raise ValueError("This function works only on undirected graphs.")

    reduced = reduce_graph(graph)
    return is_complete(reduced) or is_complete_bipartite(reduced)

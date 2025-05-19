"""
Given an undirected graph, find a Hamiltonian cycle using backtracking

"""

from Lab01 import *


def Hamiltonian(graph):
    vertices = graph.get_vertices()
    n = len(vertices)
    path = [vertices[0]]
    visited = set([vertices[0]])

    def backtracking(current_vertex):
        if len(path) == n:
            if vertices[0] in graph.out_neighbors(current_vertex):
                path.append(vertices[0])
                return True
            return False

        for neighbor in graph.out_neighbors(current_vertex):
            if neighbor not in visited:
                path.append(neighbor)
                visited.add(neighbor)
                if backtracking(neighbor):
                    return True
                visited.remove(neighbor)
                path.pop()
        return False

    if backtracking(vertices[0]):
        print("Hamiltonian Cycle found:")
        print(" -> ".join(path))
    else:
        print("Hamiltonian Cycle NOT found")
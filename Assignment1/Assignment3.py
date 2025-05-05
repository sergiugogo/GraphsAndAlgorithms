import heapq
import time
import math
from Lab01 import Graph

def euclidean_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def greedy_best_first_search(graph, start, goal, positions):
    """
    Greedy Best-First Search using Euclidean heuristic from positions.

    Parameters:
        graph: Graph object
        start, goal: vertex identifiers
        positions: dict of vertex → (x, y) position

    Returns:
            "path": list of vertices or None,
            "time": ms,
            "metrics": { "h.calculations": count, "pq.push": count, "pq.pop": count }
    """
    start_time = time.time()

    frontier = []
    heapq.heappush(frontier, (euclidean_distance(positions[start], positions[goal]), start, [start]))

    visited = set()
    counters = {"h.calculations": 1, "pq.push": 1, "pq.pop": 0}

    while frontier:
        heuristic, current, path = heapq.heappop(frontier)
        counters["pq.pop"] += 1

        if current == goal:
            return {
                "path": path,
                "time": (time.time() - start_time) * 1000,
                "metrics": counters
            }

        if current in visited:
            continue
        visited.add(current)

        for neighbor in graph.out_adj_list[current]:
            if neighbor not in visited:
                h = euclidean_distance(positions[neighbor], positions[goal])
                counters["h.calculations"] += 1
                heapq.heappush(frontier, (h, neighbor, path + [neighbor]))
                counters["pq.push"] += 1

    return {
        "path": None,
        "time": (time.time() - start_time) * 1000,
        "metrics": counters
    }

def bellman_ford(graph, start, goal):
    """
    Bellman-Ford algorithm.

    Parameters:
        graph: an instance of Graph.
        start: the starting vertex.
        goal: the goal vertex.

    Returns:
        A dictionary with keys:
         - "cost": total cost from start to goal
         - "path": list of vertices representing the path
         - "time": execution time in milliseconds (float)
         - "metrics": a dictionary containing:
             * "g.cost": number of edge cost evaluations

    Overall time complexity: O(V * E), where V is the number of vertices and E the number of edges.
    """
    start_time = time.time()

    vertices = graph.get_vertices()
    dist = {v: float("inf") for v in vertices}
    pred = {v: None for v in vertices}
    dist[start] = 0

    counters = {"g.cost": 0}
    V = len(vertices)
    updated = True
    i = 0;
    while updated: #this makes sure we go at max v-1 steps
        updated = False
        for u in graph.out_adj_list:#this goes through every vertex
            for v in graph.out_adj_list[u]: #This goes through every neighbor of the vertex u
                counters["g.cost"] += 1
                edge_cost = graph.get_weight(u, v) if graph.weighted else 1
                if dist[u] + edge_cost < dist[v]:
                    dist[v] = dist[u] + edge_cost
                    pred[v] = u
                    updated = True
        if(i == V): break
        i+=1
    end_time = time.time()

    # Reconstruct the path from start to goal.
    path = []
    if dist[goal] == float("inf"):
        path = None
    else:
        current = goal
        while current is not None:
            path.append(current)
            current = pred[current]
        path.reverse()

    return {
        "cost": dist[goal],
        "path": path,
        "time": (end_time - start_time) * 1000,
        "metrics": counters
    }
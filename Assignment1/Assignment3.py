import heapq
import time
from Lab01 import Graph


def uniform_cost_search(graph, start, goal):
    """
    Uniform Cost Search (UCS) to find the minimum cost walk from start to goal.

    Parameters:
        graph: an instance of Graph.
        start: the starting vertex.
        goal: the goal vertex.

    Returns:
        A dictionary with keys:
         - "cost": total cost of the found path (float; infinity if no path found)
         - "path": list of vertices from start to goal (or None)
         - "time": execution time in milliseconds (float)
         - "metrics": a dictionary containing counters:
             * "g.cost": number of edge cost evaluations
             * "pq.push": number of push operations on the priority queue
             * "pq.pop": number of pop operations from the priority queue

    Overall time complexity: O((V + E) * log V) due to the heap operations.

    """
    start_time = time.time()

    # Priority queue entries: (cumulative_cost, current_vertex, path_so_far)
    frontier = []
    heapq.heappush(frontier, (0, start, [start]))

    # Maintain best cost found so far per vertex.
    best_cost = {start: 0}

    # Counters for metrics
    counters = {"g.cost": 0, "pq.push": 1, "pq.pop": 0}

    while frontier:
        current_cost, current_vertex, path = heapq.heappop(frontier)
        counters["pq.pop"] += 1

        # If the goal is reached, finish and return result.
        if current_vertex == goal:
            end_time = time.time()
            return {
                "cost": current_cost,
                "path": path,
                "time": (end_time - start_time) * 1000,
                "metrics": counters
            }

        # Expand neighbors.
        for neighbor in graph.out_adj_list[current_vertex]:
            counters["g.cost"] += 1
            edge_cost = graph.get_weight(current_vertex, neighbor) if graph.weighted else 1
            new_cost = current_cost + edge_cost

            # Update if a cheaper path is found.
            if neighbor not in best_cost or new_cost < best_cost[neighbor]:
                best_cost[neighbor] = new_cost
                new_path = path + [neighbor]
                heapq.heappush(frontier, (new_cost, neighbor, new_path))
                counters["pq.push"] += 1

    end_time = time.time()
    # If no path was found, return an infinite cost and None for the path.
    return {
        "cost": float("inf"),
        "path": None,
        "time": (end_time - start_time) * 1000,
        "metrics": counters
    }


def bellman_ford(graph, start, goal):
    """
    Bellman-Ford algorithm to find the minimum cost walk from start to goal.

    Parameters:
        graph: an instance of Graph.
        start: the starting vertex.
        goal: the goal vertex.

    Returns:
        A dictionary with keys:
         - "cost": total cost from start to goal (float; infinity if no path exists)
         - "path": list of vertices representing the path (or None)
         - "time": execution time in milliseconds (float)
         - "metrics": a dictionary containing:
             * "g.cost": count of edge relaxations (cost evaluations)

    Overall time complexity: O(V * E), where V is the number of vertices and E the number of edges.
    """
    start_time = time.time()

    vertices = graph.get_vertices()
    dist = {v: float("inf") for v in vertices}
    pred = {v: None for v in vertices}
    dist[start] = 0

    counters = {"g.cost": 0}
    V = len(vertices)

    # Relax all edges V-1 times.
    for i in range(V - 1):
        updated = False
        for u in graph.out_adj_list:
            for v in graph.out_adj_list[u]:
                counters["g.cost"] += 1
                edge_cost = graph.get_weight(u, v) if graph.weighted else 1
                if dist[u] + edge_cost < dist[v]:
                    dist[v] = dist[u] + edge_cost
                    pred[v] = u
                    updated = True
        # Early exit if no update occurs in this full iteration.
        if not updated:
            break

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
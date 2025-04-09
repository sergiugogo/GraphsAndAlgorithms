import heapq
import time
from Lab01 import Graph


class UCSIterator:
    """
    Uniform Cost Search (UCS) implemented as an iterator.
    Each call to __next__ expands one vertex from the frontier and returns a tuple:
      (current_vertex, current_cost, path_so_far)

    Note:
    - The iterator yields intermediate expansion states. When the goal is reached,
      you might choose to stop iteration (or you can continue yielding intermediate states).
    - This implementation counts calls to the edge cost function (g.cost) and
      priority queue push/pop operations if desired (counters can be added similar
      to the non-iterator version).

    Overall time complexity remains O((V+E) * log V) (due to heap operations).
    """

    def __init__(self, graph, start, goal):
        if start not in graph.out_adj_list:
            raise ValueError("Start vertex does not exist in the graph.")
        self.graph = graph
        self.goal = goal
        self.frontier = []  # priority queue: (cost, vertex, path)
        heapq.heappush(self.frontier, (0, start, [start]))
        self.best_cost = {start: 0}
        self.finished = False  # flag to indicate when goal is reached

    def __iter__(self):
        return self

    def __next__(self):
        if not self.frontier or self.finished:
            raise StopIteration

        current_cost, current_vertex, path = heapq.heappop(self.frontier)

        # If goal is reached, mark finished and return final state.
        if current_vertex == self.goal:
            self.finished = True
            return (current_vertex, current_cost, path)

        # Expand neighbors.
        for neighbor in self.graph.out_adj_list[current_vertex]:
            cost_to_neighbor = self.graph.get_weight(current_vertex, neighbor) if self.graph.weighted else 1
            new_cost = current_cost + cost_to_neighbor
            # Only update if we found a cheaper path.
            if neighbor not in self.best_cost or new_cost < self.best_cost[neighbor]:
                self.best_cost[neighbor] = new_cost
                new_path = path + [neighbor]
                heapq.heappush(self.frontier, (new_cost, neighbor, new_path))
        return (current_vertex, current_cost, path)


class BellmanFordIterator:
    """
    Bellman-Ford algorithm implemented as an iterator.
    This iterator yields the state of the algorithm after each full iteration of edge relaxations.
    Each yielded tuple contains:
      (iteration_number, dist, pred)
    where:
      - dist is the dictionary of current best distances from the start.
      - pred is the dictionary of predecessors.

    Overall time complexity is O(V * E). Each iteration over all edges is one step.
    """

    def __init__(self, graph, start):
        self.graph = graph
        self.start = start
        self.vertices = graph.get_vertices()
        self.dist = {v: float("inf") for v in self.vertices}
        self.pred = {v: None for v in self.vertices}
        self.dist[start] = 0
        self.iteration = 0
        self.V = graph.get_v()
        self.finished = False

    def __iter__(self):
        return self

    def __next__(self):
        if self.finished:
            raise StopIteration

        updated = False
        # Relax all edges.
        for u in self.graph.out_adj_list:
            for v in self.graph.out_adj_list[u]:
                cost_uv = self.graph.get_weight(u, v) if self.graph.weighted else 1
                if self.dist[u] + cost_uv < self.dist[v]:
                    self.dist[v] = self.dist[u] + cost_uv
                    self.pred[v] = u
                    updated = True

        self.iteration += 1
        # Yield the state after this full pass.
        current_state = (self.iteration, self.dist.copy(), self.pred.copy())

        # If no updates were made or we have done V-1 iterations, stop.
        if not updated or self.iteration >= self.V - 1:
            self.finished = True

        return current_state


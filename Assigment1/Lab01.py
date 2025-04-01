import collections


class Graph:
    def __init__(self, directed=True, weighted=False):
        """
        Initialize an empty graph.

        Parameters:
            directed (bool): True if graph is directed, False if undirected.
            weighted (bool): True if edges have weights, False otherwise.

        Time complexity: O(1)
        """
        self.directed = directed
        self.weighted = weighted
        self.out_adj_list = {}
        self.in_adj_list = {}
        self.edge_count = 0
        self.weights = {}

    def add_vertex(self, vertex):
        """
        Add a new vertex to the graph.

        Time complexity: O(1) average
        """
        if vertex in self.out_adj_list:
            raise ValueError("Vertex already exists.")
        self.out_adj_list[vertex] = set()
        self.in_adj_list[vertex] = set()

    def add_edge(self, u, v, weight=0):
        """
        Add an edge from vertex u to vertex v.

        For directed graphs, adds a one-way edge.
        If weighted, records the weight.

        Time complexity: O(1) average
        """
        if u not in self.out_adj_list or v not in self.out_adj_list:
            raise ValueError("One or both vertices do not exist.")

        if self.directed:
            if v in self.out_adj_list[u]:
                raise ValueError("Edge already exists.")
            self.out_adj_list[u].add(v)
            self.in_adj_list[v].add(u)
            self.edge_count += 1
            if self.weighted:
                self.weights[(u, v)] = weight
        else:
            if v in self.out_adj_list[u] or u in self.out_adj_list[v]:
                raise ValueError("Edge already exists.")
            self.out_adj_list[u].add(v)
            self.out_adj_list[v].add(u)
            self.in_adj_list[u].add(v)
            self.in_adj_list[v].add(u)
            self.edge_count += 1
            if self.weighted:
                key = frozenset({u, v})
                self.weights[key] = weight

    def remove_edge(self, u, v):
        """
        Remove the edge between vertices u and v.

        For directed graphs, removes the edge from u to v.
        For undirected graphs, removes the edge from both directions.

        Time complexity: O(1) average
        """
        if self.directed:
            if u not in self.out_adj_list or v not in self.out_adj_list[u]:
                raise ValueError("Edge does not exist.")
            self.out_adj_list[u].remove(v)
            self.in_adj_list[v].remove(u)
            self.edge_count -= 1
            if self.weighted:
                del self.weights[(u, v)]
        else:
            if u not in self.out_adj_list or v not in self.out_adj_list[u]:
                raise ValueError("Edge does not exist.")
            self.out_adj_list[u].remove(v)
            self.out_adj_list[v].remove(u)
            self.in_adj_list[u].remove(v)
            self.in_adj_list[v].remove(u)
            self.edge_count -= 1
            if self.weighted:
                key = frozenset({u, v})
                del self.weights[key]

    def remove_vertex(self, vertex):
        """
        Remove a vertex and all its incident edges from the graph.

        Time complexity: O(d) where d is the degree of the vertex,
        worst-case O(V) in a dense graph.
        """
        if vertex not in self.out_adj_list:
            raise ValueError("Vertex does not exist.")

        if self.directed:
            for neighbor in list(self.out_adj_list[vertex]):
                self.in_adj_list[neighbor].remove(vertex)
                if self.weighted:
                    del self.weights[(vertex, neighbor)]
                self.edge_count -= 1

            for neighbor in list(self.in_adj_list[vertex]):
                self.out_adj_list[neighbor].remove(vertex)
                if self.weighted:
                    del self.weights[(neighbor, vertex)]
                self.edge_count -= 1
        else:
            for neighbor in list(self.out_adj_list[vertex]):
                self.out_adj_list[neighbor].remove(vertex)
                self.in_adj_list[neighbor].remove(vertex)
                if self.weighted:
                    key = frozenset({vertex, neighbor})
                    if key in self.weights:
                        del self.weights[key]
                self.edge_count -= 1
        del self.out_adj_list[vertex]
        del self.in_adj_list[vertex]

    def get_v(self):
        """
        Return the number of vertices in the graph.

        Time complexity: O(1)
        """
        return len(self.out_adj_list)

    def get_e(self):
        """
        Return the number of edges in the graph.

        Time complexity: O(1)
        """
        return self.edge_count

    def is_edge(self, u, v):
        """
        Check if there is an edge between vertices u and v.

        Time complexity: O(1)
        """
        if u not in self.out_adj_list or v not in self.out_adj_list:
            raise ValueError("One or both vertices do not exist.")
        if self.directed:
            return v in self.out_adj_list[u]
        else:
            return v in self.out_adj_list[u]

    def out_neighbors(self, vertex):
        """
        Return a list of vertices that are outgoing neighbors of the given vertex.

        Time complexity: O(d) where d is the number of neighbors.
        """
        if vertex not in self.out_adj_list:
            raise ValueError("Vertex does not exist.")
        return list(self.out_adj_list[vertex])

    def in_neighbors(self, vertex):
        """
        Return a list of vertices that are incoming neighbors of the given vertex.

        Time complexity: O(d) where d is the number of neighbors.
        """
        if vertex not in self.in_adj_list:
            raise ValueError("Vertex does not exist.")
        return list(self.in_adj_list[vertex])

    def get_vertices(self):
        """
        Return a list of all vertices in the graph.

        Time complexity: O(V)
        """
        return list(self.out_adj_list.keys())

    def __str__(self):
        """
        Return a string representation of the graph.

        Time complexity: O(V + E)
        """
        header = ("directed" if self.directed else "undirected") + " "
        header += ("weighted" if self.weighted else "unweighted")
        lines = [header]
        printed_edges = set()

        if self.directed:
            for u in self.out_adj_list:
                if not self.out_adj_list[u]:
                    lines.append(str(u))
                for v in self.out_adj_list[u]:
                    if self.weighted:
                        weight = self.weights.get((u, v), 0)
                        lines.append(f"{u} {v} {weight}")
                    else:
                        lines.append(f"{u} {v}")
        else:
            for u in self.out_adj_list:
                if not self.out_adj_list[u]:
                    lines.append(str(u))
                for v in self.out_adj_list[u]:
                    key = frozenset({u, v})
                    if key in printed_edges:
                        continue
                    printed_edges.add(key)
                    if self.weighted:
                        weight = self.weights.get(key, 0)
                        lines.append(f"{u} {v} {weight}")
                    else:
                        lines.append(f"{u} {v}")
        return "\n".join(lines)

    def change_directed(self, new_directed):
        """
        Change the graph between directed and undirected.

        When converting:
          - Directed to undirected: merge incoming and outgoing neighbor sets.
          - Undirected to directed: create two directed edges for each undirected edge.

        Time complexity: O(V + E)
        """
        if new_directed == self.directed:
            return

        if not new_directed:
            # Converting from directed to undirected.
            new_adj = {}
            for vertex in self.out_adj_list:
                new_adj[vertex] = self.out_adj_list[vertex] | self.in_adj_list[vertex]
            self.out_adj_list = new_adj.copy()
            self.in_adj_list = new_adj.copy()
            counted = set()
            new_edge_count = 0
            for u in self.out_adj_list:
                for v in self.out_adj_list[u]:
                    key = frozenset({u, v})
                    if key not in counted:
                        counted.add(key)
                        new_edge_count += 1
            self.edge_count = new_edge_count
            if self.weighted:
                new_weights = {}
                counted = set()
                for u in self.out_adj_list:
                    for v in self.out_adj_list[u]:
                        key = frozenset({u, v})
                        if key not in counted:
                            counted.add(key)
                            weight = 0
                            if (u, v) in self.weights:
                                weight = self.weights[(u, v)]
                            elif (v, u) in self.weights:
                                weight = self.weights[(v, u)]
                            new_weights[key] = weight
                self.weights = new_weights
        else:
            new_out = {}
            new_in = {}
            for vertex in self.out_adj_list:
                new_out[vertex] = set()
                new_in[vertex] = set()
            new_edge_count = 0
            if self.weighted:
                new_weights = {}
            for u in self.out_adj_list:
                for v in self.out_adj_list[u]:
                    if v not in new_out[u]:
                        new_out[u].add(v)
                        new_in[v].add(u)
                        new_edge_count += 1
                        if self.weighted:
                            key = frozenset({u, v})
                            weight = self.weights.get(key, 0)
                            new_weights[(u, v)] = weight
                    if u not in new_out[v]:
                        new_out[v].add(u)
                        new_in[u].add(v)
                        new_edge_count += 1
                        if self.weighted:
                            key = frozenset({u, v})
                            weight = self.weights.get(key, 0)
                            new_weights[(v, u)] = weight
            self.out_adj_list = new_out
            self.in_adj_list = new_in
            self.edge_count = new_edge_count
            if self.weighted:
                self.weights = new_weights

        self.directed = new_directed

    def change_weighted(self, new_weighted):
        """
        Change the graph between weighted and unweighted.

        When converting from weighted to unweighted, remove all weights.
        When converting from unweighted to weighted, assign default weight 0.

        Time complexity: O(V + E) when converting to weighted.
        """
        if new_weighted == self.weighted:
            return

        if not new_weighted:
            self.weights = {}
            self.weighted = False
        else:
            self.weighted = True
            if self.directed:
                for u in self.out_adj_list:
                    for v in self.out_adj_list[u]:
                        if (u, v) not in self.weights:
                            self.weights[(u, v)] = 0
            else:
                counted = set()
                for u in self.out_adj_list:
                    for v in self.out_adj_list[u]:
                        key = frozenset({u, v})
                        if key not in counted:
                            counted.add(key)
                            self.weights[key] = 0

    def set_weight(self, u, v, weight):
        """
        Set the weight for an edge between u and v.

        Time complexity: O(1)
        """
        if not self.weighted:
            raise ValueError("Graph is not weighted.")
        if self.directed:
            if (u, v) not in self.weights:
                raise ValueError("Edge does not exist.")
            self.weights[(u, v)] = weight
        else:
            key = frozenset({u, v})
            if key not in self.weights:
                raise ValueError("Edge does not exist.")
            self.weights[key] = weight

    def get_weight(self, u, v):
        """
        Get the weight for an edge between u and v.

        Time complexity: O(1)
        """
        if not self.weighted:
            raise ValueError("Graph is unweighted.")
        if self.directed:
            if (u, v) not in self.weights:
                raise ValueError("Edge does not exist.")
            return self.weights[(u, v)]
        else:
            key = frozenset({u, v})
            if key not in self.weights:
                raise ValueError("Edge does not exist.")
            return self.weights[key]

    @staticmethod
    def create_from_file(filename):
        """
        Create and return a graph from a file.

        File format:
          - First line: two words (e.g., "directed weighted").
          - Subsequent lines: either a single vertex or an edge.
            * For unweighted graphs: "u v"
            * For weighted graphs: "u v w"

        Time complexity: O(n) where n is the number of lines
        """
        with open(filename, "r") as f:
            lines = f.readlines()
        if not lines:
            raise ValueError("Empty file.")
        first_line = lines[0].strip().split()
        if len(first_line) != 2:
            raise ValueError("First line must contain two words indicating graph type.")
        directed_flag = (first_line[0].lower() == "directed")
        weighted_flag = (first_line[1].lower() == "weighted")
        g = Graph(directed=directed_flag, weighted=weighted_flag)
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) == 1:
                vertex = parts[0]
                if vertex not in g.out_adj_list:
                    g.add_vertex(vertex)
            elif len(parts) == 2:
                u, v = parts
                if u not in g.out_adj_list:
                    g.add_vertex(u)
                if v not in g.out_adj_list:
                    g.add_vertex(v)
                g.add_edge(u, v)
            elif len(parts) == 3:
                u, v, w = parts
                if u not in g.out_adj_list:
                    g.add_vertex(u)
                if v not in g.out_adj_list:
                    g.add_vertex(v)
                try:
                    w_val = int(w)
                except ValueError:
                    w_val = float(w)
                g.add_edge(u, v, w_val)
            else:
                raise ValueError("Invalid line format in file.")
        return g


class BFSIterator:
    """
    Breadth First Search (BFS) iterator for Graph.

    Initialization Time complexity: O(1)
    __next__: O(1)
    Total traversal: O(V + E)
    """

    def __init__(self, graph, start):
        if start not in graph.out_adj_list:
            raise ValueError("Start vertex does not exist in the graph.")
        self.graph = graph
        self.queue = collections.deque()
        self.visited = set()
        self.queue.append((start, 0))
        self.visited.add(start)

    def __iter__(self):
        return self

    def __next__(self):
        if not self.queue:
            raise StopIteration
        vertex, dist = self.queue.popleft()
        for neighbor in self.graph.out_adj_list[vertex]:
            if neighbor not in self.visited:
                self.visited.add(neighbor)
                self.queue.append((neighbor, dist + 1))
        return (vertex, dist)


class DFSIterator:
    """
    Depth First Search (DFS) iterator for Graph.

    Initialization Time complexity: O(1)
    __next__: O(1)
    Total traversal: O(V + E)
    """

    def __init__(self, graph, start):
        if start not in graph.out_adj_list:
            raise ValueError("Start vertex does not exist in the graph.")
        self.graph = graph
        self.stack = []
        self.visited = set()
        self.stack.append((start, 0))

    def __iter__(self):
        return self

    def __next__(self):
        while self.stack:
            vertex, depth = self.stack.pop()
            if vertex in self.visited:
                continue
            self.visited.add(vertex)
            for neighbor in sorted(self.graph.out_adj_list[vertex], reverse=True):
                if neighbor not in self.visited:
                    self.stack.append((neighbor, depth + 1))
            return (vertex, depth)
        raise StopIteration


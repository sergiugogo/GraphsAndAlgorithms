from Lab01 import Graph
from collections import defaultdict, deque


def kruskal_mst(graph):
    '''
    Complexity O(ElogE) where e is the number of edges in the graph
    '''
    parent = {}
    rank = {} #this refers to the rank of the tree so far. Basically if the rank of the node is 0 it means is the highest in the tree.

    def find(v): #uses path compression
        while parent[v] != v:
            parent[v] = parent[parent[v]] # we find the root of the node v and mark all the vertices above to node to that root
            v = parent[v]
        return v

    def union(u, v):
        root_u = find(u)
        root_v = find(v)
        if root_u == root_v:
            return False  # Already connected
        if rank[root_u] < rank[root_v]:
            parent[root_u] = root_v
        else:
            parent[root_v] = root_u
            if rank[root_u] == rank[root_v]:
                rank[root_u] += 1
        return True

    for v in graph.get_vertices():
        parent[v] = v
        rank[v] = 0

    # Sort edges by weight
    edges = []
    for u in graph.out_adj_list:
        for v in graph.out_adj_list[u]:
            if graph.weighted:
                w = graph.get_weight(u, v)
            else:
                w = 1
            if (v, u) not in edges: #make sure to not take the same edge twice(undirected graphs)
                edges.append((u, v, w))

    edges.sort(key=lambda x: x[2])#soprting edges by weight

    # Build MST
    mst = Graph(directed=False, weighted=True)
    for v in graph.get_vertices():
        mst.add_vertex(v)

    for u, v, w in edges:
        if union(u, v):
            mst.add_edge(u, v, w)

    return mst


def count_leaf_nodes(tree, root):
    '''
    This is basically a BFS of the tree and each time we reach a neighbor without any new neighbors, we count him as a leaf node.
    Complexity O(V+E)
    '''
    visited = set()
    queue = deque([root])
    visited.add(root)
    leaf_count = 0

    while queue:
        node = queue.popleft()
        neighbors = set(tree.out_neighbors(node)) | set(tree.in_neighbors(node))
        unvisited = [n for n in neighbors if n not in visited]

        if not unvisited:
            leaf_count += 1
        else:
            for n in unvisited:
                visited.add(n)
                queue.append(n)

    return leaf_count


def mst_leaf_count_kruskal(graph, root):
    if graph.directed:
        raise ValueError("Graph must be undirected for Kruskal's algorithm.")

    mst = kruskal_mst(graph)
    return count_leaf_nodes(mst, root)

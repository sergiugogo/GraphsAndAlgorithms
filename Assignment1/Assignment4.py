from collections import deque

def compute_tree_height(graph, root):
    """
    Computes the height of a tree starting from the given root.
    """
    visited = set()
    queue = deque([(root, 0)])  # (node, depth)
    visited.add(root)
    max_depth = 0

    while queue:
        node, depth = queue.popleft()
        max_depth = max(max_depth, depth)

        neighbors = set(graph.out_neighbors(node)) | set(graph.in_neighbors(node))#GETTING ALL NEIGHBORS (set so we don't have duplicates)
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, depth + 1))

    return max_depth

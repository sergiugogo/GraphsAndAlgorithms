from Assignment3 import bellman_ford, greedy_best_first_search

def compare_algorithms(graph, start, goal, positions):
    # Run GBFS (only if positions are available)
    if not positions or start not in positions or goal not in positions:
        return "Error: Position data missing or incomplete for Greedy Best-First Search."

    result_gbfs = greedy_best_first_search(graph, start, goal, positions)
    result_bf   = bellman_ford(graph, start, goal)

    # Format times
    gbfs_time = int(round(result_gbfs["time"]))
    bf_time   = int(round(result_bf["time"]))

    # Format paths
    gbfs_path = ", ".join(result_gbfs["path"]) if result_gbfs["path"] else "None"
    bf_path   = ", ".join(result_bf["path"]) if result_bf["path"] else "None"

    output = f"Minimum cost walk {start} to {goal}:\n"
    output += f"Greedy BFS:     time: {gbfs_time}ms, path: {gbfs_path}\n"
    output += f"Bellman-Ford:  time: {bf_time}ms, cost: {result_bf['cost']}, path: {bf_path}\n\n"
    output += "Comparison:\n"
    output += "                h.calcs   pq.push   pq.pop\n"

    gbfs_metrics = result_gbfs["metrics"]
    bf_metrics   = result_bf["metrics"]

    output += f"Greedy BFS      {gbfs_metrics.get('h.calculations', 0):<10} {gbfs_metrics.get('pq.push', 0):<9} {gbfs_metrics.get('pq.pop', 0)}\n"
    output += f"Bellman-Ford    {bf_metrics.get('g.cost', 0):<10} -         -\n"

    return output

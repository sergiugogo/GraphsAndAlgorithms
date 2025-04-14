from Assignment3 import *

def compare_algorithms(graph, start, goal):
    # Run both algorithms:
    result_ucs = uniform_cost_search(graph, start, goal)
    result_bf  = bellman_ford(graph, start, goal)

    # Format the times (in ms) as integers:
    ucs_time = int(round(result_ucs["time"]))
    bf_time  = int(round(result_bf["time"]))

    # Create comma-separated path strings:
    ucs_path = ", ".join(result_ucs["path"]) if result_ucs["path"] is not None else "None"
    bf_path  = ", ".join(result_bf["path"]) if result_bf["path"] is not None else "None"

    # Build the output:
    output = f"Minimum cost walk {start} to {goal}:\n"
    output += f"UCS: time: {ucs_time}ms, cost: {result_ucs['cost']}, path: {ucs_path}\n"
    output += f"Bellman-Ford: time: {bf_time}ms, cost: {result_bf['cost']}, path: {bf_path}\n\n"
    output += "Comparison:\n"
    output += "       g.cost   pq.push   pq.pop\n"

    ucs_g_cost  = result_ucs["metrics"].get("g.cost", 0)
    ucs_pq_push = result_ucs["metrics"].get("pq.push", 0)
    ucs_pq_pop  = result_ucs["metrics"].get("pq.pop", 0)
    bf_g_cost   = result_bf["metrics"].get("g.cost", 0)

    output += f"UCS          {ucs_g_cost}       {ucs_pq_push}       {ucs_pq_pop}\n"
    output += f"Bellman-Ford {bf_g_cost}       -         -\n"
    return output

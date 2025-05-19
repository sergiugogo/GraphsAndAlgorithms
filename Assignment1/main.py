import time
from Lab01 import Graph, BFSIterator, DFSIterator
from AlgorithmComparison import compare_algorithms
from Assignment4 import *
from Assignment5 import *
from Assignment6 import *

import csv

def load_positions_from_csv(filename):
    """
    Loads vertex positions from a CSV file into a dictionary.

    The CSV must have headers: vertex_name, position_x, position_y

    Returns:
        A dictionary mapping vertex names (as strings) to (x, y) coordinate tuples.
    """
    positions = {}
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            vertex = row['vertex_name'].strip()
            x = float(row['position_x'])
            y = float(row['position_y'])
            positions[vertex] = (x, y)
    return positions

def print_menu():
    print("\n--- Graph Algorithms Menu ---")
    print("1. Display the graph")
    print("2. Add a vertex")
    print("3. Add an edge")
    print("4. Remove an edge")
    print("5. Remove a vertex")
    print("6. Show number of vertices")
    print("7. Show number of edges")
    print("8. Check if an edge exists")
    print("9. Show outgoing neighbors of a vertex")
    print("10. Show inbound neighbors of a vertex")
    print("11. List all vertices")
    print("12. Change graph mode (directed/undirected)")
    print("13. Change graph weighting (weighted/unweighted)")
    print("14. Set weight for an edge")
    print("15. Get weight for an edge")
    print("16. BFS traversal from a vertex")
    print("17. DFS traversal from a vertex")
    print("18. Create graph from file")
    print("19. Compare UCS and Bellman-Ford")
    print("20. Numbers of leafs in a spanning tree with a given root")
    print("21. Exit.")
    print("22. Check if graph is homeomorphic to complete or complete bipartite")
    print("23. Find a Hamiltonian cycle")

def main():
    # Create a default graph.
    # Adjust default properties as needed.
    g = Graph(directed=True, weighted=False)

    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            print("\nGraph representation:")
            print(g)
        elif choice == "2":
            vertex = input("Enter vertex: ").strip()
            try:
                g.add_vertex(vertex)
                print(f"Vertex '{vertex}' added.")
            except ValueError as e:
                print(e)
        elif choice == "3":
            u = input("Enter initial vertex: ").strip()
            v = input("Enter terminal vertex: ").strip()
            weight = 0
            if g.weighted:
                try:
                    weight = float(input("Enter weight for the edge (default 0): ") or 0)
                except ValueError:
                    print("Invalid weight input. Using default weight 0.")
                    weight = 0
            try:
                g.add_edge(u, v, weight)
                print(f"Edge from '{u}' to '{v}' added.")
            except ValueError as e:
                print(e)
        elif choice == "4":
            u = input("Enter initial vertex: ").strip()
            v = input("Enter terminal vertex: ").strip()
            try:
                g.remove_edge(u, v)
                print(f"Edge from '{u}' to '{v}' removed.")
            except ValueError as e:
                print(e)
        elif choice == "5":
            vertex = input("Enter vertex to remove: ").strip()
            try:
                g.remove_vertex(vertex)
                print(f"Vertex '{vertex}' removed.")
            except ValueError as e:
                print(e)
        elif choice == "6":
            print(f"Number of vertices: {g.get_v()}")
        elif choice == "7":
            print(f"Number of edges: {g.get_e()}")
        elif choice == "8":
            u = input("Enter first vertex: ").strip()
            v = input("Enter second vertex: ").strip()
            try:
                exists = g.is_edge(u, v)
                print(f"Edge between '{u}' and '{v}' exists: {exists}")
            except ValueError as e:
                print(e)
        elif choice == "9":
            vertex = input("Enter vertex: ").strip()
            try:
                neighbors = g.out_neighbors(vertex)
                print(f"Outgoing neighbors of '{vertex}': {neighbors}")
            except ValueError as e:
                print(e)
        elif choice == "10":
            vertex = input("Enter vertex: ").strip()
            try:
                neighbors = g.in_neighbors(vertex)
                print(f"Inbound neighbors of '{vertex}': {neighbors}")
            except ValueError as e:
                print(e)
        elif choice == "11":
            print("Vertices in the graph:", g.get_vertices())
        elif choice == "12":
            mode = input("Enter 'd' for directed or 'u' for undirected: ").strip().lower()
            if mode == "d":
                new_directed = True
            elif mode == "u":
                new_directed = False
            else:
                print("Invalid input.")
                continue
            # Note: use change_directed if available in your Graph class.
            g.change_directed(new_directed)
            print(f"Graph mode changed to {'directed' if new_directed else 'undirected'}.")
        elif choice == "13":
            weighting = input("Enter 'w' for weighted or 'u' for unweighted: ").strip().lower()
            if weighting == "w":
                new_weighted = True
            elif weighting == "u":
                new_weighted = False
            else:
                print("Invalid input.")
                continue
            # Note: use change_weighted if available in your Graph class.
            g.change_weighted(new_weighted)
            print(f"Graph weighting changed to {'weighted' if new_weighted else 'unweighted'}.")
        elif choice == "14":
            if not g.weighted:
                print("Graph is not weighted.")
            else:
                u = input("Enter initial vertex: ").strip()
                v = input("Enter terminal vertex: ").strip()
                try:
                    weight = float(input("Enter new weight: ") or 0)
                except ValueError:
                    print("Invalid weight input.")
                    continue
                try:
                    g.set_weight(u, v, weight)
                    print(f"Weight for edge from '{u}' to '{v}' set to {weight}.")
                except ValueError as e:
                    print(e)
        elif choice == "15":
            if not g.weighted:
                print("Graph is not weighted.")
            else:
                u = input("Enter initial vertex: ").strip()
                v = input("Enter terminal vertex: ").strip()
                try:
                    weight = g.get_weight(u, v)
                    print(f"Weight for edge from '{u}' to '{v}' is {weight}.")
                except ValueError as e:
                    print(e)
        elif choice == "16":
            start_v = input("Enter starting vertex for BFS: ").strip()
            try:
                print("BFS traversal (vertex, distance):")
                for vertex, dist in BFSIterator(g, start_v):
                    print(f"{vertex}: distance {dist}")
            except ValueError as e:
                print(e)
        elif choice == "17":
            start_v = input("Enter starting vertex for DFS: ").strip()
            try:
                print("DFS traversal (vertex, depth):")
                for vertex, depth in DFSIterator(g, start_v):
                    print(f"{vertex}: depth {depth}")
            except ValueError as e:
                print(e)
        elif choice == "18":
            filename = input("Enter filename to load graph from: ").strip()
            try:
                g = Graph.create_from_file(filename)
                print("Graph loaded from file:")
                print(g)
            except Exception as e:
                print("Error loading graph from file:", e)
        elif choice == "19":
                positions_file = input("Enter the filename for vertex positions CSV: ").strip()
                try:
                    positions = load_positions_from_csv(positions_file)
                    print(f"Loaded {len(positions)} positions.")
                except Exception as e:
                    print("Failed to load positions:", e)
                    continue

                start = input("Start vertex: ").strip()
                goal = input("Goal vertex: ").strip()
                print(compare_algorithms(g, start, goal, positions))
        elif choice == "20":
            root = input("Enter the root vertex: ")
            mst = kruskal_mst(g)
            print("\nMinimum Spanning Tree (Edges with Weights):")
            for u in mst.out_adj_list:
                for v in mst.out_adj_list[u]:
                    if not mst.directed and u > v:
                        continue  # Skip duplicate edges in undirected graph
                    w = mst.get_weight(u, v)
                    print(f"{u} -- {v}  [weight = {w}]")
            try:
                leaf_count = mst_leaf_count_kruskal(g, root)
                print(f"Number of leaf nodes in the MST: {leaf_count}")
            except Exception as e:
                print("Error:", e)

        elif choice == "21":
            print("Exiting the program.")
            break
        elif choice == "22":
            try:
                if g.directed:
                    print("This check is only valid for undirected graphs.")
                else:
                    result = is_homeomorphic_to_complete_or_bipartite(g)
                    if result:
                        print("The graph is homeomorphic to a complete or complete bipartite graph.")
                    else:
                        print("The graph is NOT homeomorphic to a complete or complete bipartite graph.")
            except Exception as e:
                print("Error:", e)

        elif choice == "23":
            print(f"{Hamiltonian(g)}")

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

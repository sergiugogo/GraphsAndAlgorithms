from Lab01 import Graph, BFSIterator, DFSIterator
from Assignment3 import UCSIterator, BellmanFordIterator


def print_menu():
    print("\nWelcome to the Graph Algorithms Menu. Choose an option:")
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
    print("19. Exit")
    print("20. Run Uniform Cost Search (UCS)")
    print("21. Run Bellman-Ford Algorithm")


def main():
    # Create a default graph: directed and unweighted initially.
    g = Graph(directed=True, weighted=False)

    while True:
        print_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            print("\nGraph representation:")
            print(g)
        elif choice == "2":
            vertex = input("Enter vertex: ")
            try:
                g.add_vertex(vertex)
                print(f"Vertex '{vertex}' added.")
            except ValueError as e:
                print(e)
        elif choice == "3":
            u = input("Enter initial vertex: ")
            v = input("Enter terminal vertex: ")
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
            u = input("Enter initial vertex: ")
            v = input("Enter terminal vertex: ")
            try:
                g.remove_edge(u, v)
                print(f"Edge from '{u}' to '{v}' removed.")
            except ValueError as e:
                print(e)
        elif choice == "5":
            vertex = input("Enter vertex to remove: ")
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
            u = input("Enter first vertex: ")
            v = input("Enter second vertex: ")
            try:
                exists = g.is_edge(u, v)
                print(f"Edge between '{u}' and '{v}' exists: {exists}")
            except ValueError as e:
                print(e)
        elif choice == "9":
            vertex = input("Enter vertex: ")
            try:
                neighbors = g.out_neighbors(vertex)
                print(f"Outgoing neighbors of '{vertex}': {neighbors}")
            except ValueError as e:
                print(e)
        elif choice == "10":
            vertex = input("Enter vertex: ")
            try:
                neighbors = g.in_neighbors(vertex)
                print(f"Inbound neighbors of '{vertex}': {neighbors}")
            except ValueError as e:
                print(e)
        elif choice == "11":
            print("Vertices in the graph:", g.get_vertices())
        elif choice == "12":
            print("Current graph mode is", "directed" if g.directed else "undirected")
            new_mode = input("Enter 'd' for directed or 'u' for undirected: ").strip().lower()
            if new_mode == "d":
                new_directed = True
            elif new_mode == "u":
                new_directed = False
            else:
                print("Invalid input.")
                continue
            g.change_if_directed(new_directed)
            print(f"Graph mode changed to {'directed' if new_directed else 'undirected'}.")
        elif choice == "13":
            print("Current weighting is", "weighted" if g.weighted else "unweighted")
            new_weighted_input = input("Enter 'w' for weighted or 'u' for unweighted: ").strip().lower()
            if new_weighted_input == "w":
                new_weighted = True
            elif new_weighted_input == "u":
                new_weighted = False
            else:
                print("Invalid input.")
                continue
            g.change_if_weighted(new_weighted)
            print(f"Graph weighting changed to {'weighted' if new_weighted else 'unweighted'}.")
        elif choice == "14":
            if not g.weighted:
                print("Graph is not weighted.")
            else:
                u = input("Enter initial vertex: ")
                v = input("Enter terminal vertex: ")
                try:
                    weight = float(input("Enter new weight: "))
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
                u = input("Enter initial vertex: ")
                v = input("Enter terminal vertex: ")
                try:
                    weight = g.get_weight(u, v)
                    print(f"Weight for edge from '{u}' to '{v}' is {weight}.")
                except ValueError as e:
                    print(e)
        elif choice == "16":
            start = input("Enter starting vertex for BFS: ")
            try:
                print("BFS traversal (vertex, distance):")
                for vertex, dist in BFSIterator(g, start):
                    print(f"{vertex}: distance {dist}")
            except ValueError as e:
                print(e)
        elif choice == "17":
            start = input("Enter starting vertex for DFS: ")
            try:
                print("DFS traversal (vertex, depth):")
                for vertex, depth in DFSIterator(g, start):
                    print(f"{vertex}: depth {depth}")
            except ValueError as e:
                print(e)
        elif choice == "18":
            filename = input("Enter filename to load graph from: ")
            try:
                g = Graph.create_from_file(filename)
                print("Graph loaded from file:")
                print(g)
            except Exception as e:
                print("Error loading graph from file:", e)
        elif choice == "20":
            start_vertex = input("Enter start vertex for UCS: ")
            goal_vertex = input("Enter goal vertex for UCS: ")
            result = UCSIterator(g, start_vertex, goal_vertex)
            print("\nUniform Cost Search (UCS) result:")
            print(f"Cost: {result['cost']}, Path: {result['path']}, Time: {result['time']:.2f} ms")
            print("Metrics:", result["metrics"])
        elif choice == "21":
            start_vertex = input("Enter start vertex for Bellman-Ford: ")
            goal_vertex = input("Enter goal vertex for Bellman-Ford: ")
            result = BellmanFordIterator(g, start_vertex, goal_vertex)
            print("\nBellman-Ford result:")
            print(f"Cost: {result['cost']}, Path: {result['path']}, Time: {result['time']:.2f} ms")
            print("Metrics:", result["metrics"])
        elif choice == "19":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

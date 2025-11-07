# ospf.py
import networkx as nx
import heapq

def dijkstra(graph, start_node):
    # {node: cost}
    distances = {node: float('inf') for node in graph.nodes()}
    # {node: previous_node_in_path}
    previous_nodes = {node: None for node in graph.nodes()}
    distances[start_node] = 0
    
    # Priority queue: (cost, node)
    pq = [(0, start_node)]
    
    while pq:
        current_cost, current_node = heapq.heappop(pq)
        
        if current_cost > distances[current_node]:
            continue
            
        for neighbor in graph.neighbors(current_node):
            cost = graph.edges[current_node, neighbor]['cost']
            new_cost = distances[current_node] + cost
            
            if new_cost < distances[neighbor]:
                distances[neighbor] = new_cost
                previous_nodes[neighbor] = current_node
                heapq.heappush(pq, (new_cost, neighbor))
                
    return distances, previous_nodes

def get_routing_table(start_node, distances, previous_nodes):
    table = {}
    for dest in previous_nodes:
        if dest == start_node:
            table[dest] = {'next_hop': '-', 'cost': 0}
            continue
            
        if distances[dest] == float('inf'):
            table[dest] = {'next_hop': '-', 'cost': 'inf'}
            continue

        # Trace back to find the first hop from the start_node
        curr = dest
        next_hop = None
        while curr != start_node:
            if previous_nodes[curr] == start_node:
                next_hop = curr
                break
            curr = previous_nodes[curr]
            
        table[dest] = {'next_hop': next_hop, 'cost': distances[dest]}
    return table

def print_table(router_name, table):
    print(f"--- OSPF Routing Table for {router_name} ---")
    print(f"{'Destination':<12} | {'Next Hop':<10} | {'Cost':<5}")
    print("-" * 37)
    for dest, info in sorted(table.items()):
        print(f"{dest:<12} | {info['next_hop']:<10} | {info['cost']:<5}")
    print("\n")

def create_topology():
    G = nx.Graph()
    edges = [
        ('A', 'B', 5), ('A', 'C', 2), ('B', 'D', 1),
        ('B', 'E', 6), ('C', 'D', 4), ('C', 'F', 8),
        ('D', 'E', 3), ('E', 'F', 2)
    ]
    # Add costs as edge attributes
    for u, v, cost in edges:
        G.add_edge(u, v, cost=cost)
    return G

# --- Main Simulation ---
if __name__ == "__main__":
    # 1. Create network topology
    G = create_topology()
    all_nodes = list(G.nodes())

    # 2. Simulate LSA flooding by giving every router the full map
    # 3. Each router computes its own shortest path tree
    print("--- Simulating OSPF ---")
    print("Each router builds its Link-State Database (assumed complete) and runs Dijkstra.")
    print("\n")

    for node in all_nodes:
        # Run Dijkstra from this node's perspective
        distances, previous_nodes = dijkstra(G, node)
        
        # Build the routing table
        routing_table = get_routing_table(node, distances, previous_nodes)
        
        # 4. Display the table
        print_table(node, routing_table)

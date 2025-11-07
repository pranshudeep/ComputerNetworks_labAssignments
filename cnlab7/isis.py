# isis.py
import networkx as nx
import heapq

# This simulation focuses on the link-state (Dijkstra) aspect of IS-IS,
# which is conceptually similar to OSPF as per the lab requirements.

def dijkstra(graph, start_node):
    distances = {node: float('inf') for node in graph.nodes()}
    previous_nodes = {node: None for node in graph.nodes()}
    distances[start_node] = 0
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
    print(f"--- IS-IS Routing Table for {router_name} ---")
    print(f"{'Destination':<12} | {'Next Hop':<10} | {'Cost':<5}")
    print("-" * 37)
    for dest, info in sorted(table.items()):
        print(f"{dest:<12} | {info['next_hop']:<10} | {info['cost']:<5}")
    print("\n")

def create_topology():
    G = nx.Graph()
    # Using a different topology for variety
    edges = [
        ('R1', 'R2', 10), ('R1', 'R3', 10),
        ('R2', 'R4', 20), ('R3', 'R4', 5),
        ('R3', 'R5', 10), ('R4', 'R5', 5)
    ]
    for u, v, cost in edges:
        G.add_edge(u, v, cost=cost)
    return G

# --- Main Simulation ---
if __name__ == "__main__":
    G = create_topology()
    all_nodes = list(G.nodes())

    print("--- Simulating IS-IS (Link-State Algorithm) ---")
    print("Each router builds its topology database (assumed complete) and runs Dijkstra.")
    print("\n")

    for node in all_nodes:
        distances, previous_nodes = dijkstra(G, node)
        routing_table = get_routing_table(node, distances, previous_nodes)
        print_table(node, routing_table)

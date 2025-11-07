# rip.py
import networkx as nx

class RipRouter:
    def __init__(self, name):
        self.name = name
        self.neighbors = []
        # Routing table: {destination: {'next_hop': 'X', 'cost': 99}}
        self.routing_table = {}

    def initialize_table(self, all_nodes):
        # Initialize table with infinity to all, 0 to self
        for node in all_nodes:
            self.routing_table[node] = {'next_hop': None, 'cost': 99}
        self.routing_table[self.name] = {'next_hop': self.name, 'cost': 0}

    def update_table(self, neighbor_name, neighbor_table):
        # Bellman-Ford logic
        table_changed = False
        for dest, info in neighbor_table.items():
            new_cost = 1 + info['cost'] # RIP cost is 1 hop
            
            if new_cost < self.routing_table[dest]['cost']:
                self.routing_table[dest]['cost'] = new_cost
                self.routing_table[dest]['next_hop'] = neighbor_name
                table_changed = True
        return table_changed

    def print_table(self):
        print(f"--- RIP Routing Table for {self.name} ---")
        print(f"{'Destination':<12} | {'Next Hop':<10} | {'Cost':<5}")
        print("-" * 37)
        for dest, info in sorted(self.routing_table.items()):
            cost = info['cost']
            next_hop = info['next_hop'] if info['next_hop'] is not None else '-'
            print(f"{dest:<12} | {next_hop:<10} | {cost:<5}")
        print("\n")

def create_topology():
    G = nx.Graph()
    edges = [
        ('A', 'B'), ('B', 'C'), ('C', 'D'), 
        ('A', 'C'), ('B', 'D')
    ]
    G.add_edges_from(edges)
    return G

# --- Main Simulation ---
if __name__ == "__main__":
    G = create_topology()
    all_nodes = list(G.nodes())
    routers = {node: RipRouter(node) for node in all_nodes}

    # Set neighbors for each router
    for node in all_nodes:
        routers[node].neighbors = list(G.neighbors(node))
        routers[node].initialize_table(all_nodes)

    # --- Simulation Loop ---
    converged = False
    iteration = 0
    while not converged:
        iteration += 1
        print(f"*** Iteration {iteration} ***")
        converged = True # Assume convergence until proven otherwise
        
        # Routers exchange tables simultaneously (in rounds)
        # Create a snapshot of tables to exchange
        current_tables = {name: router.routing_table.copy() for name, router in routers.items()}

        for name, router in routers.items():
            for neighbor_name in router.neighbors:
                neighbor_table = current_tables[neighbor_name]
                if router.update_table(neighbor_name, neighbor_table):
                    converged = False # A change occurred, not converged yet
        
        if iteration > len(all_nodes) * 2:
            print("Warning: Possible count-to-infinity loop or slow convergence.")
            break

    print("--- Simulation Converged ---")
    for name, router in routers.items():
        router.print_table()

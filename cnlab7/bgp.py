# bgp.py
import networkx as nx

class BgpRouter:
    def __init__(self, name):
        self.name = name # AS number (e.g., 'AS1')
        self.neighbors = []
        # Route Information Base (RIB): {prefix: {'path': ['AS1', ...], 'next_hop': 'AS2'}}
        self.rib = {}

    def initialize_rib(self):
        # A router knows how to reach itself
        self.rib[self.name] = {'path': [self.name], 'next_hop': 'self'}

    def process_update(self, neighbor_name, neighbor_rib):
        table_changed = False
        
        for prefix, info in neighbor_rib.items():
            # 1. Loop Prevention
            if self.name in info['path']:
                continue # Skip this route, it causes a loop
            
            new_path = [self.name] + info['path']
            
            # 2. Path Selection
            if prefix not in self.rib or (len(new_path) < len(self.rib[prefix]['path'])):
                self.rib[prefix] = {
                    'path': new_path,
                    'next_hop': neighbor_name
                }
                table_changed = True
        return table_changed

    def print_rib(self):
        print(f"--- BGP RIB for {self.name} ---")
        print(f"{'Prefix':<10} | {'Next Hop':<10} | {'AS Path'}")
        print("-" * 40)
        for prefix, info in sorted(self.rib.items()):
            path_str = " -> ".join(info['path'])
            print(f"{prefix:<10} | {info['next_hop']:<10} | {path_str}")
        print("\n")

def create_as_topology():
    G = nx.Graph()
    # Nodes are ASes
    edges = [
        ('AS1', 'AS2'), ('AS1', 'AS3'),
        ('AS2', 'AS4'), ('AS3', 'AS4'),
        ('AS4', 'AS5')
    ]
    G.add_edges_from(edges)
    return G

# --- Main Simulation ---
if __name__ == "__main__":
    G = create_as_topology()
    all_nodes = list(G.nodes())
    routers = {node: BgpRouter(node) for node in all_nodes}

    for node in all_nodes:
        routers[node].neighbors = list(G.neighbors(node))
        routers[node].initialize_rib()

    # --- Simulation Loop ---
    converged = False
    iteration = 0
    while not converged:
        iteration += 1
        print(f"*** BGP Iteration {iteration} ***")
        converged = True
        
        current_ribs = {name: router.rib.copy() for name, router in routers.items()}

        for name, router in routers.items():
            for neighbor_name in router.neighbors:
                # Receive UPDATE from neighbor
                if router.process_update(neighbor_name, current_ribs[neighbor_name]):
                    converged = False
        
        if iteration > len(all_nodes) * 2:
            print("Warning: Possible BGP convergence issue.")
            break

    print("--- BGP Simulation Converged ---")
    for name, router in routers.items():
        router.print_rib()

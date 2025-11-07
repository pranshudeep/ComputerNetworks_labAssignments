from ip_utils import ip_to_binary, get_network_prefix

class Router:
    
    def __init__(self, routes: list):
        
        # This list will store our processed, optimized forwarding table
        # We will store tuples of: (binary_prefix, prefix_length, output_link)
        self.forwarding_table = []
        
        # Call the private helper method to build the table
        self._build_forwarding_table(routes)

    def _build_forwarding_table(self, routes: list):
        print("Building forwarding table...")
        for cidr, link in routes:
            # Convert the CIDR string (e.g., "223.1.1.0/24")
            # into its binary prefix (e.g., "11011111...")
            binary_prefix = get_network_prefix(cidr)
            
            # Get the length of the prefix
            prefix_len = len(binary_prefix)
            
            # Add the processed route to our internal table
            self.forwarding_table.append((binary_prefix, prefix_len, link))
            print(f'  Added route: {cidr} -> {link} (Prefix: {binary_prefix})')
            
        # CRUCIAL STEP: Sort the table by prefix length, from longest to shortest.
        # This makes the routing algorithm simple: the first match we find
        # will always be the longest (most specific) match.
        # We use `reverse=True` to sort in descending order.
        self.forwarding_table.sort(key=lambda route: route[1], reverse=True)
        
        print("\nSorted Forwarding Table (Longest prefix first):")
        for prefix, length, link in self.forwarding_table:
            print(f'  Len: {length:<2} | Prefix: {prefix:<24} | Link: {link}')

    def route_packet(self, dest_ip: str) -> str:
        # (a) Convert the destination IP to its 32-bit binary representation
        binary_dest_ip = ip_to_binary(dest_ip)
        
        # (b) Iterate through the sorted internal forwarding table
        for prefix, length, link in self.forwarding_table:
            
            # (c) Check if the binary destination IP *starts with* the binary prefix
            # Example:
            #   binary_dest_ip: 11011111000000010000000101100100  ("223.1.1.100")
            #   prefix:         110111110000000100000001        ("223.1.1.0/24")
            #   This is a match.
            if binary_dest_ip.startswith(prefix):
                
                # (d) First match is the longest match, so we return the link.
                return link
                
        # If the loop finishes without finding any match, return the default route.
        return "Default Gateway"

# --- Test Case ---
if __name__ == "__main__":
    print("\n--- Testing Part 2: Router (Longest Prefix Match) ---")
    
    # Initialize the Router with the test routes from the PDF
    routes_list = [
        ("223.1.1.0/24", "Link 0"),
        ("223.1.2.0/24", "Link 1"),
        ("223.1.3.0/24", "Link 2"),
        ("223.1.0.0/16", "Link 4 (ISP)")
    ]
    
    my_router = Router(routes_list)
    
    # --- Verification ---
    print("\n--- Running Test Cases ---")
    
    # Test 1
    ip1 = "223.1.1.100"
    link1 = my_router.route_packet(ip1)
    print(f'route_packet("{ip1}") -> "{link1}" (Expected: "Link 0")')

    # Test 2
    ip2 = "223.1.2.5"
    link2 = my_router.route_packet(ip2)
    print(f'route_packet("{ip2}") -> "{link2}" (Expected: "Link 1")')
    
    # Test 3
    ip3 = "223.1.250.1"
    link3 = my_router.route_packet(ip3)
    print(f'route_packet("{ip3}") -> "{link3}" (Expected: "Link 4 (ISP)")')

    # Test 4
    ip4 = "198.51.100.1"
    link4 = my_router.route_packet(ip4)

    print(f'route_packet("{ip4}") -> "{link4}" (Expected: "Default Gateway")')

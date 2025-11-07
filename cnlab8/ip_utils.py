def ip_to_binary(ip_address: str) -> str:
    
    # Split the IP address into its four octets
    octets = ip_address.split('.')
    
    # List to hold the 8-bit binary representation of each octet
    binary_octets = []
    
    for octet in octets:
        # Convert the string octet to an integer
        int_octet = int(octet)
        
        # Convert the integer to a binary string and pad with leading zeros to ensure it's 8 bits long
        # The format string f'{number:08b}' means:
        # 0: Pad with zeros
        # 8: Total width is 8 characters
        # b: Convert to binary
        binary_octet = f'{int_octet:08b}'
        binary_octets.append(binary_octet)
        
    # Join all four 8-bit strings to create the final 32-bit string
    return "".join(binary_octets)

def get_network_prefix(ip_cidr: str) -> str:
    
    # Split the CIDR string into the IP address and the prefix length
    ip_address, prefix_len_str = ip_cidr.split('/')
    
    # Convert the prefix length to an integer
    prefix_len = int(prefix_len_str)
    
    # Use our function from Part 1 to get the full 32-bit binary IP
    full_binary_ip = ip_to_binary(ip_address)
    
    # Slice the binary string to get only the prefix
    # e.g., "1100...01"[0:23]
    network_prefix = full_binary_ip[:prefix_len]
    
    return network_prefix

# --- Test Cases ---
if __name__ == "__main__":
    print("--- Testing Part 1: IP Utilities ---")
    
    # Test ip_to_binary
    ip1 = "192.168.1.1"
    binary_ip1 = ip_to_binary(ip1)
    print(f'ip_to_binary("{ip1}"):')
    print(f'  Expected: 11000000101010000000000100000001')
    print(f'  Actual:   {binary_ip1}')
    
    ip2 = "200.23.16.0"
    binary_ip2 = ip_to_binary(ip2)
    print(f'\nip_to_binary("{ip2}"):')
    print(f'  Expected: 11001000000101110001000000000000')
    print(f'  Actual:   {binary_ip2}')
    
    # Test get_network_prefix
    cidr = "200.23.16.0/23"
    prefix = get_network_prefix(cidr)
    print(f'\nget_network_prefix("{cidr}"):')
    print(f'  Expected: 11001000000101110001000')

    print(f'  Actual:   {prefix}')

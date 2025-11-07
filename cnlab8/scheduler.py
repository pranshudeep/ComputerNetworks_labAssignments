from dataclasses import dataclass

@dataclass  # <-- FIX: Removed order=True from here to resolve the TypeError
class Packet:
    priority: int  # We define this first to make default sorting easy
    source_ip: str
    dest_ip: str
    payload: str
    
    # We redefine __lt__ (less than) to *only* compare priority.
    # This helps if using queue.PriorityQueue as hinted in the PDF.
    def __lt__(self, other):
        return self.priority < other.priority

def fifo_scheduler(packet_list: list) -> list:
    # FCFS means the first packet in is the first packet out.
    # Since the input list is already in arrival order,
    # we just return a copy of it.
    return packet_list[:]

def priority_scheduler(packet_list: list) -> list:
    # We use Python's built-in `sorted` function.
    # The `key` argument tells `sorted` *what* to use for comparison.
    # `lambda p: p.priority` is a small, anonymous function that
    # takes a packet `p` and returns its `priority` attribute.
    # `sorted` will then order the packets based on this number,
    # from smallest to largest.
    return sorted(packet_list, key=lambda p: p.priority)

# --- Test Case ---
if __name__ == "__main__":
    print("\n--- Testing Part 3: Schedulers ---")
    
    # Create the list of Packet objects from the PDF
    # Note: I've added dummy IPs. The payload and priority are the important parts.
    packets_in_arrival_order = [
        Packet(source_ip="10.1.1.2", dest_ip="192.168.1.1", payload="Data Packet 1", priority=2),
        Packet(source_ip="10.1.1.3", dest_ip="192.168.1.2", payload="Data Packet 2", priority=2),
        Packet(source_ip="20.2.2.2", dest_ip="192.168.1.3", payload="VOIP Packet 1", priority=0),
        Packet(source_ip="30.3.3.3", dest_ip="192.168.1.4", payload="Video Packet 1", priority=1),
        Packet(source_ip="20.2.2.3", dest_ip="192.168.1.5", payload="VOIP Packet 2", priority=0),
    ]

    print("Arrival Order:")
    for pkt in packets_in_arrival_order:
        print(f'  Payload: "{pkt.payload}", Priority: {pkt.priority}')
        
    # --- Verify fifo_scheduler ---
    print("\n--- Testing FIFO Scheduler ---")
    fifo_output = fifo_scheduler(packets_in_arrival_order)
    
    # Extract payloads for easy comparison
    fifo_payloads = [p.payload for p in fifo_output]
    print(f'  Output Order: {fifo_payloads}')
    
    expected_fifo = [
        "Data Packet 1", "Data Packet 2", "VOIP Packet 1",
        "Video Packet 1", "VOIP Packet 2"
    ]
    print(f'  Expected Order: {expected_fifo}')
    assert fifo_payloads == expected_fifo
    print("  FIFO Test: PASSED")

    # --- Verify priority_scheduler ---
    print("\n--- Testing Priority Scheduler ---")
    priority_output = priority_scheduler(packets_in_arrival_order)
    
    # Extract payloads for easy comparison
    priority_payloads = [p.payload for p in priority_output]
    print(f'  Output Order: {priority_payloads}')
    
    expected_priority = [
        "VOIP Packet 1", "VOIP Packet 2",  # Priority 0
        "Video Packet 1",                # Priority 1
        "Data Packet 1", "Data Packet 2"  # Priority 2
    ]
    print(f'  Expected Order: {expected_priority}')
    assert priority_payloads == expected_priority

    print("  Priority Test: PASSED")

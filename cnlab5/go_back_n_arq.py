import random

def go_back_n_arq(total_frames, window_size, loss_prob):
    """
    Simulates the Go-Back-N ARQ sliding window protocol.

    Args:
        total_frames (int): The total number of frames to transmit.
        window_size (int): The size of the sender's window (N).
        loss_prob (float): The probability of a frame being lost.
    """
    print(f"--- Starting Go-Back-N ARQ Simulation ---")
    print(f"Total Frames: {total_frames}, Window Size: {window_size}, Loss Probability: {loss_prob}\n")

    base = 0
    next_seq_num = 0
    
    while base < total_frames:
        # Send all frames in the current window
        print(f"Sending frames {base} to {min(base + window_size - 1, total_frames - 1)}...")
        
        for i in range(next_seq_num, min(base + window_size, total_frames)):
            print(f"  - Sent Frame {i}")
        
        # Simulate receiver's response
        ack_to_receive = base
        
        for i in range(base, min(base + window_size, total_frames)):
            # Check if the frame is lost
            if random.random() < loss_prob:
                print(f"\n! Frame {i} lost, receiver expects Frame {base}.") # [cite: 38]
                print(f"  Receiver discards all subsequent frames until Frame {base} is received.")
                print("  Sender will time out and retransmit the window.")
                break # All subsequent frames in the window are effectively lost
            else:
                # Frame received successfully
                print(f"  - Received Frame {i}, sending ACK {i+1}")
                ack_to_receive = i + 1
        
        # Sender receives the cumulative ACK
        if ack_to_receive > base:
            print(f"\n-> ACK {ack_to_receive-1} received.") # [cite: 37, 39]
            base = ack_to_receive
            next_seq_num = base
            print(f"   Window slides. New base is {base}.\n") # [cite: 40]
        else:
            # This simulates a timeout
            print(f"\n-> No ACK received for Frame {base}. Timeout.")
            print(f"   Retransmitting all frames from {base}...\n") # [cite: 33]
            next_seq_num = base # Reset next_seq_num to start of window

    print("--- Simulation Complete ---")


if __name__ == "__main__":
    # Adjustable parameters 
    TOTAL_FRAMES = 15
    WINDOW_SIZE = 4
    LOSS_PROBABILITY = 0.15 # 15% chance of losing a frame

    go_back_n_arq(TOTAL_FRAMES, WINDOW_SIZE, LOSS_PROBABILITY)

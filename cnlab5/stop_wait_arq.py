import random
import time

def stop_and_wait_arq(total_frames, loss_prob):
    """
    Simulates the Stop-and-Wait ARQ protocol.

    Args:
        total_frames (int): The total number of frames to transmit.
        loss_prob (float): The probability of a frame or ACK being lost (0.0 to 1.0).
    """
    print("--- Starting Stop-and-Wait ARQ Simulation ---")
    
    timeout = 2.0  # seconds
    frame_to_send = 0
    
    while frame_to_send < total_frames:
        print(f"Sending Frame {frame_to_send}") # [cite: 17, 19]
        
        # Simulate transmission and wait for ACK
        ack_received = False
        start_time = time.time()
        
        while not ack_received:
            # Check for timeout
            if time.time() - start_time > timeout:
                print(f"Timeout for Frame {frame_to_send}. Retransmitting...")
                print(f"Sending Frame {frame_to_send}")
                start_time = time.time() # Reset timer on retransmission
            
            # Simulate potential loss of frame or ACK
            if random.random() < loss_prob:
                # Frame is "lost", so we just wait for a timeout
                time.sleep(0.5) # Simulate processing delay
                continue

            # Frame is successfully received, and ACK is sent back
            # Simulate ACK loss
            if random.random() < loss_prob:
                print(f"ACK for Frame {frame_to_send} lost. Waiting for timeout...")
                time.sleep(timeout) # Wait for sender to timeout
                continue

            # ACK is successfully received
            print(f"ACK {frame_to_send} received") # [cite: 18, 21]
            ack_received = True
            frame_to_send += 1

    print("\n--- Simulation Complete ---")

if __name__ == "__main__":
    # Parameters for the simulation
    NUM_FRAMES = 8
    LOSS_PROBABILITY = 0.2 # 20% chance of losing a frame or ACK
    
    stop_and_wait_arq(NUM_FRAMES, LOSS_PROBABILITY)

import matplotlib.pyplot as plt
import random

def tcp_congestion_control(rounds, ssthresh_initial, loss_prob):
    """
    Simulates TCP Congestion Control phases: Slow Start and Congestion Avoidance.

    Args:
        rounds (int): The number of transmission rounds to simulate.
        ssthresh_initial (int): The initial slow start threshold.
        loss_prob (float): The probability of packet loss in a round.
    """
    print("--- Starting TCP Congestion Control Simulation ---")
    
    cwnd = 1
    ssthresh = ssthresh_initial
    
    # Lists to store data for plotting
    transmission_rounds = []
    cwnd_sizes = []
    
    print(f"Initial State: cwnd = {cwnd}, ssthresh = {ssthresh}")

    for i in range(1, rounds + 1):
        transmission_rounds.append(i)
        cwnd_sizes.append(cwnd)
        
        print(f"\nRound {i}: cwnd = {cwnd}")
        
        # Simulate packet loss (timeout)
        if random.random() < loss_prob:
            print(f"  -> Packet Loss Detected (Timeout)!")
            # Multiplicative Decrease [cite: 49]
            ssthresh = max(cwnd // 2, 2) # Threshold is halved, with a floor of 2
            cwnd = 1 # Reset cwnd to 1
            print(f"  -> New State: ssthresh = {ssthresh}, cwnd = {cwnd} (Entering Slow Start)")
            continue

        # On successful ACK, increase cwnd [cite: 48]
        if cwnd < ssthresh:
            # Slow Start Phase: exponential growth [cite: 47]
            cwnd *= 2
            print(f"  -> ACK Received. In Slow Start, cwnd doubles to {cwnd}")
        else:
            # Congestion Avoidance Phase: linear growth [cite: 47]
            cwnd += 1
            print(f"  -> ACK Received. In Congestion Avoidance, cwnd increments to {cwnd}")
            
    # Plotting the results 
    plt.figure(figsize=(12, 6))
    plt.plot(transmission_rounds, cwnd_sizes, marker='o', linestyle='-')
    plt.title('TCP Congestion Window (cwnd) Simulation')
    plt.xlabel('Transmission Round')
    plt.ylabel('Congestion Window Size (cwnd)')
    plt.grid(True)
    plt.xticks(transmission_rounds)
    
    # Save the plot to a file [cite: 55]
    output_filename = 'cwnd_plot.png'
    plt.savefig(output_filename)
    
    print(f"\n--- Simulation Complete ---")
    print(f"Plot saved as '{output_filename}'")
    plt.show()


if __name__ == "__main__":
    # Parameters for the simulation
    TOTAL_ROUNDS = 50
    INITIAL_SSTHRESH = 32
    PACKET_LOSS_PROB = 0.08 # 8% chance of packet loss per round
    
    # Before running, make sure you have matplotlib installed:
    # pip install matplotlib
    
    tcp_congestion_control(TOTAL_ROUNDS, INITIAL_SSTHRESH, PACKET_LOSS_PROB)

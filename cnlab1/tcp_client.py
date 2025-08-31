import socket

client_name = "Client of PRANSHU DEEP"
server_host = "localhost"
server_port = 9999

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_host, server_port))
print(f"[✓] Connected to server on port {server_port}")

# prompt for valid integer
while True:
    try:
        num = int(input("Enter an integer (1-100): "))
        if 1 <= num <= 100:
            break
        print("Number must be between 1 and 100.")
    except ValueError:
        print("Please enter a valid integer.")

# send as "name,number"
message = f"{client_name},{num}\n"
client_socket.sendall(message.encode())

# receive reply
reply = client_socket.recv(1024).decode().strip()
if reply:
    try:
        server_name, server_int = reply.split(",")
        server_int = int(server_int)

        print("\n--- RESULT ---")
        print(f"Client Name   : {client_name}")
        print(f"Server Name   : {server_name}")
        print(f"Client Integer: {num}")
        print(f"Server Integer: {server_int}")
        print(f"Sum           : {num + server_int}")
    except Exception:
        print("[!] Invalid reply from server.")

client_socket.close()

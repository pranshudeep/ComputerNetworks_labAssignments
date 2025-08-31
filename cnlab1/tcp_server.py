import socket, sys

server_name = "Server of PRANSHU DEEP"
server_int = 42   # choose between 1–100
server_port = 9999

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', server_port))
server_socket.listen(1)

print(f"[✓] {server_name} listening on port {server_port}")

conn, addr = server_socket.accept()
print(f"[+] Connected by {addr}")

data = conn.recv(1024).decode().strip()
if not data:
    print("[!] No data received.")
    conn.close()
    sys.exit()

try:
    client_name, client_int_str = data.split(",")
    client_int = int(client_int_str)
except Exception:
    print("[!] Invalid client message format.")
    conn.close()
    server_socket.close()
    sys.exit()

print(f"Client Name   : {client_name}")
print(f"Server Name   : {server_name}")
print(f"Client Integer: {client_int}")
print(f"Server Integer: {server_int}")

# terminate if client integer out of range
if not (1 <= client_int <= 100):
    print("[X] Out-of-range client integer. Shutting down.")
    conn.close()
    server_socket.close()
    sys.exit()

total = client_int + server_int
print(f"Sum           : {total}")

# reply as "server_name,server_int"
reply = f"{server_name},{server_int}\n"
conn.sendall(reply.encode())

conn.close()
server_socket.close()

import socket

HOST = "127.0.0.1"
PORT = 9090

def handle_client(conn):
    request = conn.recv(1024).decode("utf-8")
    print("----- Request -----")
    print(request)

    headers = {}
    for line in request.split("\r\n")[1:]:
        if ": " in line:
            key, value = line.split(": ", 1)
            headers[key] = value

    response_body = ""
    response_headers = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n"

    if "Cookie" in headers:
        cookie_value = headers["Cookie"]
        response_body = f"<h1>Welcome back! Your cookie: {cookie_value}</h1>"
    else:
        cookie_value = "User123"
        response_headers += f"Set-Cookie: {cookie_value}\r\n"
        response_body = "<h1>Hello, new user! Cookie has been set.</h1>"

    response_headers += f"Content-Length: {len(response_body)}\r\n\r\n"
    response = response_headers + response_body

    conn.sendall(response.encode("utf-8"))
    conn.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"Server running on http://{HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        handle_client(conn)

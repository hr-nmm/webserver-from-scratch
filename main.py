import socket

with open("index.html", "r") as file:
    html_content = file.read()
content_length, content_type = len(html_content.encode("utf-8")), "text/html"

response = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\nContent-Length: {content_length}\n\r\n{html_content}"


def main():
    print("logs appear here...")
    while True:
        server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
        conn, conn_address = server_socket.accept()
        with conn:
            print(f"Connection from: {conn_address}")
            request = conn.recv(1024)
            if request.decode()[:6] == "GET / ":
                conn.send(response.encode())
            else:
                conn.send(("HTTP/1.1 404 Not Found\r\n\r\n").encode())


if __name__ == "__main__":
    main()

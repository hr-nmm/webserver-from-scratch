import socket
import threading


def client_thread(ip, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, port))
        sock.sendall(message.encode())
        response = sock.recv(1024).decode()
        print(f"Received from server: {response}")


if __name__ == "__main__":
    HOST, PORT = "localhost", 4221
    messages = [
        "GET /echo/abc HTTP/1.1\r\nHost: localhost:4221\r\nUser-Agent: curl/7.64.1\r\nAccept: */*\r\n\r\n",
        "GET / HTTP/1.1\r\nHost: localhost:4221\r\nUser-Agent: curl/7.64.1\r\nAccept: */*\r\n\r\n",
        "GET /user-agent HTTP/1.1\r\nHost: localhost:4221\r\nUser-Agent: foobar/1.2.3\r\nAccept: */*\r\n\r\n",
        "GET /echo/yolofunz HTTP/1.1\r\nHost: localhost:4221\r\nUser-Agent: curl/7.64.1\r\nAccept: */*\r\n\r\n",
        "GET /echo/naother-message HTTP/1.1\r\nHost: localhost:4221\r\nUser-Agent: curl/7.64.1\r\nAccept: */*\r\n\r\n",
    ]

    threads = []
    for message in messages:
        thread = threading.Thread(target=client_thread, args=(HOST, PORT, message))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

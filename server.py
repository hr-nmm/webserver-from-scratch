import socket

CRLF = "\r\n"


class ResponseHandler:
    http_ver = "HTTP/1.1"
    success_code = "200"
    success_text = "OK"
    failure_code = "404"
    failure_text = "Not Found"

    def create_status_line(self, http_ver, code, text):
        return f"{http_ver} {code} {text}" + CRLF

    def create_response_headers(self, headers):
        if not headers:
            return ""
        headers_str: list[str] = []
        for key in headers:
            val = headers[key]
            str_repr = f"{key}: {val}"
            headers_str.append(str_repr)
        return f"{CRLF}".join(headers_str) + CRLF + CRLF

    def create_response(self, http_ver, code, text, headers, body):
        status_line = self.create_status_line(http_ver, code, text)
        response_headers = self.create_response_headers(headers)
        resp = status_line + response_headers
        if body:
            resp += body
            resp = self.end_response(resp)
        return resp

    def create_success_response(self, headers={}, body=None):
        return self.create_response(
            self.http_ver, self.success_code, self.success_text, headers, body
        )

    def create_failure_response(self, headers={}, body=None):
        return self.create_response(
            self.http_ver, self.failure_code, self.failure_text, headers, body
        )

    def end_response(self, response):
        return response + CRLF


class RequestHandler:
    def __init__(self, request):
        self.parse_request(request)

    def parse_request(self, request):
        req, self.body = request.decode().split(CRLF * 2)
        status_line, *headers_str = req.split(CRLF)
        self.method, self.path, self.version = status_line.split(" ")
        self.headers: dict[str, str] = {}
        for string in headers_str:
            key, val = string.split(": ")
            self.headers[key] = val

    def get_body(self):
        return self.body

    def get_headers(self):
        return self.headers

    def get_status_line(self):
        return self.method, self.path, self.version


def get_file_content(file_name):
    with open(file_name, "r") as file:
        return file.read()


def handle_request(path):
    resp_handler = ResponseHandler()
    if path == "/":
        body = get_file_content("index.html")
        headers = {
            "Content-Type": "text/html",
            "Content-Length": f"{len(body.encode('utf-8'))}",
        }
        return resp_handler.create_success_response(headers, body)
    elif path == "/style.css":
        body = get_file_content("style.css")
        headers = {
            "Content-Type": "text/css",
            "Content-Length": f"{len(body.encode('utf-8'))}",
        }
        return resp_handler.create_success_response(headers, body)
    elif path.startswith("/echo"):
        body = path.split("/echo/")[1]
        headers = {"Content-Type": "text/plain", "Content-Length": f"{len(body)}"}
        return resp_handler.create_success_response(headers, body)
    else:
        return resp_handler.create_failure_response()


def main():
    print("logs appear here...")
    while True:
        server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
        conn, conn_address = server_socket.accept()  # wait for client
        with conn:
            print(f"CLIENT ADDRESS => Connection from: {conn_address}")
            request = conn.recv(2048)
            req_handler = RequestHandler(request)
            _, path, _ = req_handler.get_status_line()
            conn.send(handle_request(path).encode())


if __name__ == "__main__":
    main()

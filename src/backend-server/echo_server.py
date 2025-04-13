from http.server import HTTPServer
from echo_handler import EchoHandler


def run_server(port: int = 8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, EchoHandler)
    print(f"Backend Serving on port {port}...")
    httpd.serve_forever()


if __name__ == '__main__':
    run_server(8000)

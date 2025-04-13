from functools import partial
from http.server import HTTPServer, ThreadingHTTPServer
from proxy_handler import ReverseProxyHandler

TARGET_HOST = "127.0.0.1"
TARGET_PORT = 8000


def run_server(host, port):
    print(f"Starting reverse proxy on {host}:{port}, forwarding to {TARGET_HOST}:{TARGET_PORT}")
    server_address = (host, port)
    handler_with_params = partial(
        ReverseProxyHandler,
        upstream_host='0.0.0.0',
        upstream_port=8000)
    httpd = ThreadingHTTPServer(server_address, handler_with_params)
    httpd.serve_forever()


if __name__ == "__main__":
    run_server("0.0.0.0", 8001)

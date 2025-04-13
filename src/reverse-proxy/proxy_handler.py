import socket
from http.server import BaseHTTPRequestHandler
from request_utils import prepare_forwarding_request, read_response, filter_headers, parse_headers

CHUNK_SIZE = 4096
EXCLUDED_HEADERS = {"connection", "host"}


class ReverseProxyHandler(BaseHTTPRequestHandler):

    upstream_host: str
    upstream_port: int

    def __init__(self, *args, upstream_host, upstream_port, **kwargs):
        self.upstream_host = upstream_host
        self.upstream_port = upstream_port
        super().__init__(*args, **kwargs)

    def do_GET(self):
        self.proxy_request()

    def do_POST(self):
        self.proxy_request()

    def do_PUT(self):
        self.proxy_request()

    def do_DELETE(self):
        self.proxy_request()

    def do_HEAD(self):
        self.proxy_request()

    def do_OPTIONS(self):
        self.proxy_request()

    def do_PATCH(self):
        self.proxy_request()

    def proxy_request(self) -> None:
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length else b''

        request_data = prepare_forwarding_request(
            self.headers,
            body,
            self.path,
            self.command,
            self.upstream_host,
            self.upstream_port
        )

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_sock:
            try:
                proxy_sock.connect((self.upstream_host, self.upstream_port))
                proxy_sock.sendall(request_data)
                self.send_response_to_client(proxy_sock)
            except socket.timeout:
                self.send_error(504, "Gateway Timeout")
            except Exception as e:
                self.send_error(502, f"Bad Gateway: {e}")

    def _process_header_for_status(self, status_header):
        # Parse the status line
        # Example: HTTP/1.1 200 OK -> version="HTTP/1.1", status_code="200", reason="OK"
        parts = status_header.split(b" ", 2)
        if len(parts) < 2:
            self.send_error(502, "Bad response from upstream server.")
            return None
        try:
            status_code = int(parts[1])
            reason = parts[2].decode() if len(parts) > 2 else ""
            return status_code, reason
        except ValueError:
            self.send_error(502, "Bad status code from upstream server.")
            return None

    def send_response_to_client(self, proxy_sock):
        header_section, remainder = read_response(proxy_sock)
        status_header, raw_headers = filter_headers(header_section)

        status_code, reason = self._process_header_for_status(status_header)
        if not status_code:
            return

        # Send the status code to the client
        self.send_response(status_code, reason)

        # Send headers
        for raw_header in raw_headers:
            header_key, header_value = parse_headers(raw_header)
            if not header_key:
                continue
            if header_key.lower() in EXCLUDED_HEADERS:
                continue
            self.send_header(header_key, header_value)
        # End headers
        self.end_headers()

        # Write the remainder of the body we already read
        self.wfile.write(remainder)

        # Read the rest of the response in chunks and forward it
        while True:
            chunk = proxy_sock.recv(CHUNK_SIZE)
            if not chunk:
                break
            self.wfile.write(chunk)
        self.wfile.flush()

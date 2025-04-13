import json
from http.server import BaseHTTPRequestHandler


class EchoHandler(BaseHTTPRequestHandler):

    def _echo_body(self, method: str):
        content_length = int(self.headers.get('Content-Length', 0))
        request_body = self.rfile.read(content_length)
        response_body = json.dumps({"method": method, "body": request_body.decode("utf-8")})
        self.send_response(200)
        self.end_headers()
        self.wfile.write(response_body.encode("utf-8"))

    def do_GET(self):
        self._echo_body("GET")

    def do_POST(self):
        self._echo_body("POST")

    def do_PUT(self):
        self._echo_body("PUT")

    def do_DELETE(self):
        self._echo_body("DELETE")

    def do_PATCH(self):
        self._echo_body("PATCH")

    def do_OPTIONS(self):
        self._echo_body("OPTIONS")

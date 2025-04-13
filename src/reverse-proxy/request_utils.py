from urllib.parse import urlparse


def prepare_forwarding_request(in_headers, body, target_path, command, target_host, target_port):
    url_components = urlparse(target_path)
    path_and_query = url_components.path
    if url_components.query:
        path_and_query += f"?{url_components.query}"
    request_line = f"{command} {path_and_query} HTTP/1.1\r\n"

    # Build the headers to forward to the target, excluding some
    headers = ""
    for key, value in in_headers.items():
        if key.lower() not in ["connection", "host"]:  # These two not required
            headers += f"{key}: {value}\r\n"

    # Setting the Host header for the target server
    headers += f"Host: {target_host}:{target_port}\r\n"
    headers += "Connection: close\r\n"
    request_data = (request_line + headers + "\r\n").encode("utf-8") + body
    return request_data


def read_response(proxy_sock):
    response_buffer = b""
    # Read until we get the full header section (terminated by b"\r\n\r\n")
    while b"\r\n\r\n" not in response_buffer:
        chunk = proxy_sock.recv(4096)
        if not chunk:
            break
        response_buffer += chunk
    header_section, remainder = response_buffer.split(b"\r\n\r\n", 1)
    return header_section, remainder


def filter_headers(headers):
    header_lines = headers.split(b"\r\n")
    status_header = header_lines[0]  # e.g. b"HTTP/1.1 200 OK"
    raw_headers = header_lines[1:]
    return status_header, raw_headers


def parse_headers(raw_header):
    # Example: b"Content-Type: text/plain"
    decoded_line = raw_header.decode("latin-1")
    if not decoded_line.strip():
        return None
    # We can parse key/value by splitting the first ":"
    split_index = decoded_line.find(":")
    if split_index == -1:
        return None
    header_key = decoded_line[:split_index].strip()
    header_value = decoded_line[split_index + 1:].strip()
    return header_key, header_value

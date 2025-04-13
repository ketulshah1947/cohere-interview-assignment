import json
import requests

PROXY_BASE_URL = "http://0.0.0.0:8001"
ECHO_PATH = "/"


def test_get_request():
    response = requests.get(f"{PROXY_BASE_URL}{ECHO_PATH}")
    assert response.status_code == 200, "Expected HTTP 200 for GET request"

    data = response.json()
    assert data.get("method") == "GET", "Echoed method should be GET"
    assert data.get("body") == "", "Echoed body should be empty for GET"


def test_post_request():
    payload = {"name": "c", "price": 20}
    response = requests.post(f"{PROXY_BASE_URL}{ECHO_PATH}", json=payload)
    assert response.status_code == 200, "Expected HTTP 200 for POST request"

    data = response.json()
    assert data.get("method") == "POST", "Echoed method should be POST"

    body_str = data.get("body", "")
    echoed_payload = json.loads(body_str)
    assert echoed_payload == payload, "Echoed payload does not match the sent payload"


def test_put_request():
    payload = {"update": True, "value": 123}
    response = requests.put(f"{PROXY_BASE_URL}{ECHO_PATH}", json=payload)
    assert response.status_code == 200, "Expected HTTP 200 for PUT request"

    data = response.json()
    assert data.get("method") == "PUT", "Echoed method should be PUT"

    body_str = data.get("body", "")
    echoed_payload = json.loads(body_str)
    assert echoed_payload == payload, "Echoed payload does not match the sent payload"


def test_delete_request():
    response = requests.delete(f"{PROXY_BASE_URL}{ECHO_PATH}")
    assert response.status_code == 200, "Expected HTTP 200 for DELETE request"

    data = response.json()
    assert data.get("method") == "DELETE", "Echoed method should be DELETE"
    assert data.get("body") == "", "Echoed body should be empty for DELETE"

# cohere-interview-assignment

## Assignment questions
### 1. How could someone get started with your codebase?
* Clone or download this repository.
* Install Python 3.7+ (any modern Python 3 version should work).
* Optionally, configure the target host/port and proxy host/port. If not changed, backend runs at 8000 and proxy runs at 8001.
* Run backend server first by running below command:
  ```shell
    python3 src/backend-server/echo_server.py
  ```
* Run proxy server by running below command:
  ```shell
    python3 src/reverse-proxy/proxy_server.py
  ```
* Send test requests to the proxy. For example:
  ```shell
    curl -i http://0.0.0.0:8081/
  ```
  Proxy will call the backend and get the response back to you.

### 2. What resources did you use to build your implementation?
I have used below IDE:
* Pycharm

I have used below libraries:
* ThreadingHTTPServer instead of HTTPServer to allow multi-threading.
* socket
* urllib

I have used below resources:
* Googling
* Stackoverflow
* Python documentations

### 3. Explain any design decisions you made, including limitations of the system.
* ***Multi-threaded***: The use of HTTPServer allows only single-threaded server. Hence, I used ThreadingHTTPServer which is also a part of the standard library. I could have also used asyncio to handle concurrent requests better. But the limitation on 3rd party libraries restricts it. For this small example, HTTPServer would have worked just fine.
* ***Headers***: We are blindly passing headers but in real world, more robust HTTP proxies will handle more complex cases to handle chunked data.
* ***Minimal error handling***: This example attempts to handle upstream errors by sending 502 or 504 to the client. In a production environment, I might want more comprehensive error handling or logging.
* ***No caching, no load balancing***: This is a simple pass-through example. Real reverse proxies often include caching or load balancing features.
* ***Lack of TLS***: This example does not support HTTPS endpoints directly. Adding HTTPS termination would require additional steps, such as using ssl and wrapping the socket.

### 4. How would you scale this?
* ***Horizontal scaling***: I would run multiple instances of this proxy behind a load balancer. Each instance can handle a certain slice of the traffic.
* ***Connection pooling***: Instead of opening a new connection to the target on every request, I can use a connection pool.
* ***Monitoring & Logging***: I would add logs and monitoring to watch for performance bottlenecks.

### 5. How would you make it more secure?
* ***HTTPS/TLS support***: I would use ssl from the Python standard library to wrap the socket and enable TLS for inbound connections.
* ***Access Control / Authentication***: I can restrict which clients can connect to the proxy, or require authentication headers/tokens for requests. RBAC is also latest option and widely used.
* ***Rate limiting***: I would implement request counting and rate-limiting logic, either in code or behind an upstream firewall/load balancer.
* ***Error handling***: I would provide clear but not overly detailed error responses (to avoid leaking sensitive info).

### 6. What resources (including programming tool assistants) did you use to build your implementation?
I think this question is by mistake as it is duplicate of question-2.

## Running tests
* Install any dependencies
  ```shell
  pip3 install -r requirements.txt
  ```
* Right click on test file and click run tests.


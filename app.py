import os
from routes import ROUTES
from utils.request import parse_query, parse_cookies
from utils.response import text

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

def match_route(method, path):
    for m, p, handler in ROUTES:
        if m == method and p == path:
            return handler
    return None

def serve_static(path):
    rel = path.replace("/static/", "", 1)
    file_path = os.path.join(STATIC_DIR, rel)
    if not os.path.isfile(file_path):
        return text("Not Found", status="404 Not Found")

    # basic content-type
    ctype = "text/plain"
    if file_path.endswith(".css"):
        ctype = "text/css"
    elif file_path.endswith(".js"):
        ctype = "application/javascript"

    with open(file_path, "rb") as f:
        body = f.read()
    return "200 OK", [("Content-Type", ctype)], [body]

def application(environ, start_response):
    method = environ.get("REQUEST_METHOD", "GET").upper()
    path = environ.get("PATH_INFO", "/")

    if path.startswith("/static/"):
        status, headers, body = serve_static(path)
        start_response(status, headers)
        return body

    handler = match_route(method, path)
    if not handler:
        status, headers, body = text("Not Found", status="404 Not Found")
        start_response(status, headers)
        return body

    req = {
        "environ": environ,
        "method": method,
        "path": path,
        "query": parse_query(environ),
        "cookies": parse_cookies(environ),
    }

    status, headers, body = handler(req)
    start_response(status, headers)
    return body

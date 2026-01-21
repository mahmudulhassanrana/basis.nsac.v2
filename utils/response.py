import os

def response(body: bytes, status="200 OK", headers=None):
    headers = headers or []
    headers = [("Content-Type", "text/html; charset=utf-8")] + headers
    return status, headers, [body]

def text(msg: str, status="200 OK", headers=None):
    return response(msg.encode("utf-8"), status=status, headers=headers)

def redirect(location: str):
    return "302 Found", [("Location", location)], [b""]

def set_cookie(headers, key, value, path="/", http_only=True):
    cookie = f"{key}={value}; Path={path}"
    if http_only:
        cookie += "; HttpOnly"
    headers.append(("Set-Cookie", cookie))

def clear_cookie(headers, key, path="/"):
    headers.append(("Set-Cookie", f"{key}=; Path={path}; Max-Age=0"))

def _load_template(name: str) -> str:
    base_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
    with open(os.path.join(base_dir, name), "r", encoding="utf-8") as f:
        return f.read()

def render_page(body_template: str, context: dict):
    body_html = _load_template(body_template)
    for k, v in context.items():
        body_html = body_html.replace("{{ " + k + " }}", str(v))

    layout = _load_template("layout.html")
    page = layout.replace("{{ body }}", body_html)
    page = page.replace("{{ title }}", str(context.get("title", "Hackathon Portal")))
    page = page.replace("{{ extra_head }}", str(context.get("extra_head", "")))
    return page

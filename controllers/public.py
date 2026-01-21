from db.database import query_one, execute
from auth.security import hash_password, verify_password, sign
from auth.sessions import create_session, destroy_session
from utils.response import response, redirect, render_template, set_cookie, clear_cookie, text
from utils.request import parse_form

def home(req):
    html = render_template("home.html", {"title": "Hackathon Portal"})
    return response(html.encode())

def login_get(req):
    html = render_template("login.html", {"error": ""})
    return response(html.encode())

def login_post(req):
    data, _ = parse_form(req["environ"])
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    user = query_one("SELECT * FROM users WHERE email=%s AND status='active'", (email,))
    if not user or not verify_password(password, user["password_hash"]):
        html = render_template("login.html", {"error": "Invalid email or password"})
        return response(html.encode(), status="401 Unauthorized")

    token = create_session(user["id"])
    headers = []
    set_cookie(headers, "session", sign(token))
    # redirect by role
    role = user["role"]
    if role == "admin":
        return "302 Found", headers + [("Location", "/admin/dashboard")], [b""]
    if role == "judge":
        return "302 Found", headers + [("Location", "/judge/dashboard")], [b""]
    if role == "volunteer":
        return "302 Found", headers + [("Location", "/volunteer/dashboard")], [b""]
    return "302 Found", headers + [("Location", "/participant/dashboard")], [b""]

def register_get(req):
    html = render_template("register.html", {"error": ""})
    return response(html.encode())

def register_post(req):
    data, _ = parse_form(req["environ"])
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    role = (data.get("role") or "participant").strip()

    if role not in ("participant", "judge", "volunteer"):
        role = "participant"  # only admin can create admin

    if not name or not email or not password:
        html = render_template("register.html", {"error": "All fields are required"})
        return response(html.encode(), status="400 Bad Request")

    exists = query_one("SELECT id FROM users WHERE email=%s", (email,))
    if exists:
        html = render_template("register.html", {"error": "Email already registered"})
        return response(html.encode(), status="409 Conflict")

    execute(
        "INSERT INTO users (name,email,password_hash,role) VALUES (%s,%s,%s,%s)",
        (name, email, hash_password(password), role),
    )
    return redirect("/login")

def logout(req):
    # if session exists, delete it
    from utils.request import parse_cookies
    from auth.security import unsign

    cookies = parse_cookies(req["environ"])
    signed = cookies.get("session")
    if signed:
        token = unsign(signed)
        if token:
            destroy_session(token)

    headers = []
    clear_cookie(headers, "session")
    return "302 Found", headers + [("Location", "/")], [b""]

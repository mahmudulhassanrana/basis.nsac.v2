from utils.response import redirect, text
from utils.request import get_current_user

def login_required(handler):
    def wrapped(req):
        user = get_current_user(req)
        if not user:
            return redirect("/login")
        req["user"] = user
        return handler(req)
    return wrapped

def role_required(*roles):
    def deco(handler):
        def wrapped(req):
            user = req.get("user") or get_current_user(req)
            if not user:
                return redirect("/login")
            if user["role"] not in roles:
                return text("Forbidden", status="403 Forbidden")
            req["user"] = user
            return handler(req)
        return wrapped
    return deco

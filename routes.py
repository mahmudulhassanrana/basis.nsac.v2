from controllers.public import home, login_get, login_post, register_get, register_post, logout
from controllers.participant import participant_dashboard
from controllers.admin import admin_dashboard
from controllers.judge import judge_dashboard
from controllers.volunteer import volunteer_dashboard

ROUTES = [
    ("GET",  "/", home),
    ("GET",  "/login", login_get),
    ("POST", "/login", login_post),
    ("GET",  "/register", register_get),
    ("POST", "/register", register_post),
    ("GET",  "/logout", logout),

    ("GET",  "/participant/dashboard", participant_dashboard),
    ("GET",  "/admin/dashboard", admin_dashboard),
    ("GET",  "/judge/dashboard", judge_dashboard),
    ("GET",  "/volunteer/dashboard", volunteer_dashboard),
]

from auth.decorators import login_required, role_required
from utils.response import response, render_template

@login_required
@role_required("admin")
def admin_dashboard(req):
    user = req["user"]
    html = render_template(
        "dashboard.html",
        {
            "title": "Admin Dashboard",
            "name": user["name"],
            "role": user["role"],
            "content": "Next: manage applications, rooms, assignments, users, config deadlines, publish results.",
        },
    )
    return response(html.encode("utf-8"))

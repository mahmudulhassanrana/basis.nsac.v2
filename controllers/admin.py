from auth.decorators import login_required, role_required
from utils.response import response, render_page

@login_required
@role_required("admin")
def admin_dashboard(req):
    user = req["user"]
    html = render_page(
        "dashboard.html",
        {
            "title": "Admin Dashboard",
            "name": user["name"],
            "role": user["role"],
            "content": "Admin panel coming next (applications, deadlines, rooms, results).",
        },
    )
    return response(html.encode("utf-8"))


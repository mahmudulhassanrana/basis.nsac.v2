from auth.decorators import login_required, role_required
from utils.response import response, render_page

@login_required
@role_required("volunteer")
def volunteer_dashboard(req):
    user = req["user"]
    html = render_page(
        "dashboard.html",
        {
            "title": "Volunteer Dashboard",
            "name": user["name"],
            "role": user["role"],
            "content": "Volunteer assignments & coordination coming next.",
        },
    )
    return response(html.encode("utf-8"))


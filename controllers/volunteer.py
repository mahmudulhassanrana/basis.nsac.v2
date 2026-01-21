from auth.decorators import login_required, role_required
from utils.response import response, render_template

@login_required
@role_required("volunteer")
def volunteer_dashboard(req):
    user = req["user"]
    html = render_template("dashboard.html", {
        "title": "Volunteer Dashboard",
        "name": user["name"],
        "role": user["role"],
        "content": "Next: view assigned teams/projects and coordination tools."
    })
    return response(html.encode())

from auth.decorators import login_required, role_required
from utils.response import response, render_template

@login_required
@role_required("judge")
def judge_dashboard(req):
    user = req["user"]
    html = render_template("dashboard.html", {
        "title": "Judge Dashboard",
        "name": user["name"],
        "role": user["role"],
        "content": "Next: view assigned projects + evaluate & score."
    })
    return response(html.encode())

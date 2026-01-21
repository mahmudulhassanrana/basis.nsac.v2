from auth.decorators import login_required, role_required
from utils.response import response, render_page

@login_required
@role_required("judge")
def judge_dashboard(req):
    user = req["user"]
    html = render_page(
        "dashboard.html",
        {
            "title": "Judge Dashboard",
            "name": user["name"],
            "role": user["role"],
            "content": "Judge assignments & evaluation coming next.",
        },
    )
    return response(html.encode("utf-8"))


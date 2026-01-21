from auth.decorators import login_required, role_required
from utils.response import response, render_template

@login_required
@role_required("participant")
def participant_dashboard(req):
    user = req["user"]
    html = render_template(
        "dashboard.html",
        {
            "title": "Participant Dashboard",
            "name": user["name"],
            "role": user["role"],
            "content": "Next: application form, project info, submission upload, status pages.",
        },
    )
    return response(html.encode("utf-8"))

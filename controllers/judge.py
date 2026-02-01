from auth.decorators import login_required, role_required
from utils.response import response, render_partial, render_with_layout, render_html

JUDGE_EXTRA_HEAD = """
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"/>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
<style>
  .sidebar-link.active {
    background-color: #2563eb;
    color: white;
    box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.2);
  }
</style>
"""

def _judge_base(user, page_title: str):
    avatar_name = (user.get("name") or "Judge").replace(" ", "+")
    return {
        "title": "Judge | NASA Space Apps BD",
        "extra_head": JUDGE_EXTRA_HEAD,

        "judge_name": user.get("name", "Judge"),
        "judge_role_label": "Judge",
        "judge_avatar_url": f"https://ui-avatars.com/api/?name={avatar_name}&background=2563EB&color=fff",

        "page_title": page_title,

        "nav_dashboard_active": "",
        "nav_assigned_active": "",
        "nav_scores_active": "",
        "nav_inactive": "text-slate-500 hover:bg-slate-50 hover:text-blue-600",
    }

def _judge_set_active(ctx, active: str):
    if active == "dashboard":
        ctx["nav_dashboard_active"] = "active"
    elif active == "assigned":
        ctx["nav_assigned_active"] = "active"
    elif active == "scores":
        ctx["nav_scores_active"] = "active"

def _render_judge(req, page_title: str, active: str, page_tpl: str, page_ctx: dict):
    user = req["user"]
    base = _judge_base(user, page_title)
    _judge_set_active(base, active)

    # content only page
    content_html = render_partial(page_tpl, page_ctx)

    # wrap with judge layout
    judge_full = render_with_layout("judge/layout.html", content_html, base)

    # wrap with global layout (tailwind loaded)
    final_html = render_html(
        judge_full,
        title=base.get("title", "Judge"),
        extra_head=base.get("extra_head", "")
    )
    return response(final_html.encode("utf-8"))

@login_required
@role_required("judge")
def judge_dashboard(req):
    # change content anytime
    return _render_judge(
        req,
        "Dashboard",
        "dashboard",
        "judge/dashboard.html",
        {
            "welcome_text": "Judge assignments & evaluation coming next."
        }
    )

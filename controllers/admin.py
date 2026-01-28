import json
from auth.decorators import login_required, role_required
from utils.response import response, render_partial, render_with_layout, render_html
from db.database import query_one, query_all

ADMIN_EXTRA_HEAD = """
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

def _admin_base(user, page_title: str):
    avatar_name = (user.get("name") or "Admin").replace(" ", "+")
    return {
        "title": "Admin | NASA Space Apps BD",
        "extra_head": ADMIN_EXTRA_HEAD,

        "admin_name": user.get("name", "Admin"),
        "admin_role_label": "Super Admin",
        "admin_avatar_url": f"https://ui-avatars.com/api/?name={avatar_name}&background=0D8ABC&color=fff",

        "page_title": page_title,

        "nav_dashboard_active": "",
        "nav_applications_active": "",
        "nav_rooms_active": "",
        "nav_jv_active": "",
        "nav_control_active": "",
        "nav_inactive": "text-slate-500 hover:bg-slate-50 hover:text-blue-600",
    }

def _set_active(ctx, active: str):
    if active == "dashboard":
        ctx["nav_dashboard_active"] = "active"
    elif active == "applications":
        ctx["nav_applications_active"] = "active"
    elif active == "rooms":
        ctx["nav_rooms_active"] = "active"
    elif active == "jv":
        ctx["nav_jv_active"] = "active"
    elif active == "control":
        ctx["nav_control_active"] = "active"

def _render_admin(req, page_title: str, active: str, page_tpl: str, page_ctx: dict):
    """
    Render admin page with:
      content page -> admin/layout.html -> global templates/layout.html
    """
    user = req["user"]
    base = _admin_base(user, page_title)
    _set_active(base, active)

    # 1) render content-only page (inside templates/admin/..)
    content_html = render_partial(page_tpl, page_ctx)

    # 2) inject into admin/layout.html (sidebar/menu)
    admin_full = render_with_layout("admin/layout.html", content_html, base)

    # 3) wrap into global layout.html (loads Tailwind + head assets)
    final_html = render_html(
        admin_full,
        title=base.get("title", "Admin"),
        extra_head=base.get("extra_head", "")
    )

    return response(final_html.encode("utf-8"))

@login_required
@role_required("admin")
def admin_dashboard(req):
    # ---------------------------
    # KPI: Total Teams
    # ---------------------------
    # Count unique participant applications (latest state doesn't matter for count)
    total_teams_row = query_one("SELECT COUNT(*) AS c FROM participant_applications")
    total_teams = int((total_teams_row or {}).get("c") or 0)

    # ---------------------------
    # KPI: Rooms Occupied
    # ---------------------------
    rooms_total_row = query_one("SELECT COUNT(*) AS c FROM rooms")
    rooms_total = int((rooms_total_row or {}).get("c") or 0)

    rooms_occupied_row = query_one("""
        SELECT COUNT(DISTINCT room_id) AS c
        FROM room_projects
    """)
    rooms_occupied = int((rooms_occupied_row or {}).get("c") or 0)

    rooms_percent = 0
    if rooms_total > 0:
        rooms_percent = int(round((rooms_occupied / rooms_total) * 100))

    # ---------------------------
    # KPI: Active Judges (and Volunteer note)
    # ---------------------------
    judges_row = query_one("SELECT COUNT(*) AS c FROM users WHERE role='judge' AND status='active'")
    active_judges = int((judges_row or {}).get("c") or 0)

    volunteers_row = query_one("SELECT COUNT(*) AS c FROM users WHERE role='volunteer' AND status='active'")
    active_volunteers = int((volunteers_row or {}).get("c") or 0)

    # ---------------------------
    # KPI: Submissions (and completion rate note)
    # ---------------------------
    submissions_row = query_one("SELECT COUNT(*) AS c FROM projects where  not (title IS NULL OR title = '')")
    submissions = int((submissions_row or {}).get("c") or 0)

    completion_rate = 0
    if total_teams > 0:
        completion_rate = int(round((submissions / total_teams) * 100))

    # ---------------------------
    # Recent Applications
    # ---------------------------
    apps = query_all("""
        SELECT pa.id, pa.status, pa.data_json, pa.created_at,
               u.name AS leader_name, u.email AS leader_email
        FROM participant_applications pa
        JOIN users u ON u.id = pa.user_id
        ORDER BY pa.created_at DESC
        LIMIT 8
    """)

    def safe_json(val):
        if not val:
            return {}
        try:
            return json.loads(val) if isinstance(val, str) else (val or {})
        except Exception:
            return {}

    def badge_html(status):
        s = (status or "").lower()
        if s == "approved":
            return '<span class="px-3 py-1 bg-green-50 text-green-600 rounded-full text-[10px] font-black uppercase">Approved</span>'
        if s == "rejected":
            return '<span class="px-3 py-1 bg-red-50 text-red-600 rounded-full text-[10px] font-black uppercase">Rejected</span>'
        return '<span class="px-3 py-1 bg-orange-50 text-orange-600 rounded-full text-[10px] font-black uppercase">Pending</span>'

    recent_rows_list = []
    for row in apps:
        data = safe_json(row.get("data_json"))
        team_name = data.get("team_name", "—")
        location = data.get("location", "—")
        university = data.get("university", "—")
        leader = data.get("leader_name") or row.get("leader_name") or "—"
        status = row.get("status", "pending")

        recent_rows_list.append(f"""
        <tr class="border-b border-slate-50">
            <td class="py-5 font-bold">{team_name}</td>
            <td class="py-5">{location}, {university}</td>
            <td class="py-5">{leader}</td>
            <td class="py-5">{badge_html(status)}</td>
            <td class="py-5">
              <a href="/admin/applications" class="text-slate-400 hover:text-blue-600" title="View">
                <i class="fa-solid fa-ellipsis"></i>
              </a>
            </td>
        </tr>
        """)

    recent_rows = "\n".join(recent_rows_list) if recent_rows_list else """
    <tr>
      <td class="py-6 text-slate-400" colspan="5">No applications found.</td>
    </tr>
    """

    # Notes (you can change the text anytime)
    kpi_total_teams_note = f"{total_teams} registered teams"
    kpi_active_judges_note = f"{active_volunteers} active volunteers"
    kpi_submissions_note = f"{completion_rate}% completion rate"

    page_ctx = {
        "kpi_total_teams": str(total_teams),
        "kpi_total_teams_note": kpi_total_teams_note,

        "kpi_rooms": f"{rooms_occupied}/{rooms_total}",
        "kpi_rooms_percent": str(rooms_percent),

        "kpi_active_judges": str(active_judges),
        "kpi_active_judges_note": kpi_active_judges_note,

        "kpi_submissions": str(submissions),
        "kpi_submissions_note": kpi_submissions_note,

        "recent_rows": recent_rows,
    }

    return _render_admin(req, "Overview Summary", "dashboard", "admin/dashboard.html", page_ctx)

@login_required
@role_required("admin")
def admin_applications(req):
    return _render_admin(
        req, "All Applications", "applications",
        "admin/application/index.html",
        {"content_block": "Applications page loaded ✅"}
    )

@login_required
@role_required("admin")
def admin_rooms(req):
    return _render_admin(
        req, "Location / Room", "rooms",
        "admin/room/index.html",
        {"content_block": "Rooms page loaded ✅"}
    )

@login_required
@role_required("admin")
def admin_judges_volunteers(req):
    return _render_admin(
        req, "Judge & Volunteer", "jv",
        "admin/judges_volunteers/index.html",
        {"content_block": "Judges & Volunteers page loaded ✅"}
    )

@login_required
@role_required("admin")
def admin_control(req):
    return _render_admin(
        req, "App Control", "control",
        "admin/control/index.html",
        {"content_block": "App Control page loaded ✅"}
    )

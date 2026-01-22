from auth.decorators import login_required, role_required
from utils.response import response, render_page

# Extra head assets for Admin UI (Tailwind is already loaded via layout.html)
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

@login_required
@role_required("admin")
def admin_dashboard(req):
    user = req["user"]

    # Temporary table rows (we’ll make dynamic from DB next step)
    recent_rows = """
    <tr class="border-b border-slate-50">
      <td class="py-5 font-bold">Space Voyagers</td>
      <td class="py-5">Dhaka, DIU</td>
      <td class="py-5">Asif Ahmed</td>
      <td class="py-5">
        <span class="px-3 py-1 bg-green-50 text-green-600 rounded-full text-[10px] font-black uppercase">Approved</span>
      </td>
      <td class="py-5">
        <button class="text-slate-400 hover:text-blue-600" type="button">
          <i class="fa-solid fa-ellipsis"></i>
        </button>
      </td>
    </tr>
    <tr class="border-b border-slate-50">
      <td class="py-5 font-bold">Galactic Coders</td>
      <td class="py-5">Chittagong, CU</td>
      <td class="py-5">Sultana Razia</td>
      <td class="py-5">
        <span class="px-3 py-1 bg-orange-50 text-orange-600 rounded-full text-[10px] font-black uppercase">Pending</span>
      </td>
      <td class="py-5">
        <button class="text-slate-400 hover:text-blue-600" type="button">
          <i class="fa-solid fa-ellipsis"></i>
        </button>
      </td>
    </tr>
    """

    avatar_name = (user.get("name") or "Admin").replace(" ", "+")
    admin_avatar_url = f"https://ui-avatars.com/api/?name={avatar_name}&background=0D8ABC&color=fff"

    html = render_page(
        "admin_dashboard.html",
        {
            "title": "Admin Dashboard | NASA Space Apps BD",
            "extra_head": ADMIN_EXTRA_HEAD,

            # Sidebar profile
            "admin_name": user.get("name", "Admin"),
            "admin_role_label": "Super Admin",
            "admin_avatar_url": admin_avatar_url,

            # Header title
            "page_title": "Overview Summary",

            # Nav active classes
            "nav_dashboard_active": "active",
            "nav_applications_active": "",
            "nav_rooms_active": "",
            "nav_jv_active": "",
            "nav_control_active": "",
            "nav_inactive": "text-slate-500 hover:bg-slate-50 hover:text-blue-600",

            # KPI placeholders (we will make dynamic next step)
            "kpi_total_teams": "—",
            "kpi_total_teams_note": "Coming soon",
            "kpi_rooms": "—/—",
            "kpi_rooms_percent": "0",
            "kpi_active_judges": "—",
            "kpi_active_judges_note": "Coming soon",
            "kpi_submissions": "—",
            "kpi_submissions_note": "Coming soon",

            # Recent applications
            "recent_rows": recent_rows,
        },
    )

    return response(html.encode("utf-8"))

from controllers.public import home, login_get, login_post, register_get, register_post, logout
from controllers.participant import participant_dashboard, save_team_members, save_project
from controllers.admin import admin_dashboard,admin_applications,admin_application_view,admin_application_edit,admin_application_delete,admin_application_status,admin_applications_export,admin_rooms,admin_room_create,admin_room_edit,admin_room_assign,admin_room_delete,admin_room_unassign, admin_judges_volunteers, admin_control
from controllers.judge import judge_dashboard
from controllers.volunteer import volunteer_dashboard

ROUTES = [
    ("GET",  "/", home),
    ("GET",  "/login", login_get),
    ("POST", "/login", login_post),
    ("GET",  "/register", register_get),
    ("POST", "/register", register_post),
    ("GET",  "/logout", logout),

    # Participant Routes
    ("GET",  "/participant/dashboard", participant_dashboard),
    ("POST", "/participant/team-members", save_team_members),
    ("POST", "/participant/project", save_project),

    # Admin Routes
    ("GET", "/admin/dashboard", admin_dashboard),
    #applications
    ("GET", "/admin/applications", admin_applications),
    ("GET",  "/admin/applications/view", admin_application_view),
    ("GET",  "/admin/applications/edit", admin_application_edit),
    ("POST", "/admin/applications/edit", admin_application_edit),
    ("GET",  "/admin/applications/delete", admin_application_delete),
    ("POST", "/admin/applications/status", admin_application_status),
    ("GET",  "/admin/applications/export", admin_applications_export),
    #rooms
    ("GET",  "/admin/rooms", admin_rooms),
    ("GET",  "/admin/rooms/create", admin_room_create),
    ("POST", "/admin/rooms/create", admin_room_create),
    ("GET",  "/admin/rooms/edit", admin_room_edit),
    ("POST", "/admin/rooms/edit", admin_room_edit),
    ("GET",  "/admin/rooms/assign", admin_room_assign),
    ("POST", "/admin/rooms/assign", admin_room_assign),
    ("POST", "/admin/rooms/delete", admin_room_delete),
    ("POST", "/admin/rooms/unassign", admin_room_unassign),


    ("GET", "/admin/judges-volunteers", admin_judges_volunteers),
    ("GET", "/admin/control", admin_control),

    #Judge Routes
    ("GET",  "/judge/dashboard", judge_dashboard),

    # Volunteer Routes
    ("GET",  "/volunteer/dashboard", volunteer_dashboard),

]

from werkzeug.serving import run_simple
from app import application
from db.migrations import migrate

if __name__ == "__main__":
    migrate()

    host, port = "127.0.0.1", 8000
    print(f"✅ Server running: http://{host}:{port}")

    run_simple(
        hostname=host,
        port=port,
        application=application,
        use_reloader=True,   # 👈 auto restart on file change
        use_debugger=True    # 👈 interactive debugger
    )


from wsgiref.simple_server import make_server
from app import application
from db.migrations import migrate

if __name__ == "__main__":
    # Run migrations on start (safe because IF NOT EXISTS)
    migrate()

    host, port = "127.0.0.1", 8000
    print(f"✅ Server running: http://{host}:{port}")
    with make_server(host, port, application) as httpd:
        httpd.serve_forever()

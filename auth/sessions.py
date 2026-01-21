from datetime import datetime, timedelta
import secrets
from db.database import execute, query_one

SESSION_DAYS = 7

def create_session(user_id: int) -> str:
    token = secrets.token_hex(32)
    expires = datetime.utcnow() + timedelta(days=SESSION_DAYS)
    execute(
        "INSERT INTO sessions (user_id, session_token, expires_at) VALUES (%s,%s,%s)",
        (user_id, token, expires.strftime("%Y-%m-%d %H:%M:%S"))
    )
    return token

def get_user_by_session(token: str):
    row = query_one("""
      SELECT u.id, u.name, u.email, u.role
      FROM sessions s
      JOIN users u ON u.id = s.user_id
      WHERE s.session_token=%s AND s.expires_at > UTC_TIMESTAMP()
    """, (token,))
    return row

def destroy_session(token: str):
    execute("DELETE FROM sessions WHERE session_token=%s", (token,))

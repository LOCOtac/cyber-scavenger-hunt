import os
import psycopg2
from urllib.parse import urlparse

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    with get_connection() as conn:
        with conn.cursor() as c:
            c.execute('''
                CREATE TABLE IF NOT EXISTS leaderboard (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    score INTEGER DEFAULT 0,
                    flags TEXT
                )
            ''')
            conn.commit()

def save_submission(user_id, name, score, flags):
    with get_connection() as conn:
        with conn.cursor() as c:
            c.execute("SELECT id FROM leaderboard WHERE id = %s", (user_id,))
            row = c.fetchone()
            flags_str = ",".join(flags)

            if row:
                c.execute("UPDATE leaderboard SET name = %s, score = %s, flags = %s WHERE id = %s", (name, score, flags_str, user_id))
            else:
                c.execute("INSERT INTO leaderboard (id, name, score, flags) VALUES (%s, %s, %s, %s)", (user_id, name, score, flags_str))
            conn.commit()

def get_leaderboard():
    try:
        with get_connection() as conn:
            with conn.cursor() as c:
                c.execute("SELECT name, score, flags FROM leaderboard ORDER BY score DESC")
                rows = c.fetchall()
                return [{"name": r[0], "score": r[1], "solved": r[2].split(",") if r[2] else []} for r in rows]
    except Exception as e:
        print(f"[get_leaderboard ERROR] {e}")
        return []

def reset_leaderboard():
    with get_connection() as conn:
        with conn.cursor() as c:
            c.execute("DELETE FROM leaderboard")
            conn.commit()

def get_player_by_id(user_id):
    with get_connection() as conn:
        with conn.cursor() as c:
            c.execute("SELECT name, score, flags FROM leaderboard WHERE id = %s", (user_id,))
            row = c.fetchone()
            if row:
                return {
                    "name": row[0],
                    "score": row[1],
                    "solved": row[2].split(",") if row[2] else []
                }
            return None

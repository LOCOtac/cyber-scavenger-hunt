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
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    score INTEGER DEFAULT 0,
                    flags TEXT
                )
            ''')
            conn.commit()

def save_submission(name, score, flags):
    with get_connection() as conn:
        with conn.cursor() as c:
            c.execute("SELECT id FROM leaderboard WHERE name = %s", (name,))
            row = c.fetchone()
            flags_str = ",".join(flags)

            if row:
                c.execute("UPDATE leaderboard SET score = %s, flags = %s WHERE name = %s", (score, flags_str, name))
            else:
                c.execute("INSERT INTO leaderboard (name, score, flags) VALUES (%s, %s, %s)", (name, score, flags_str))
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


def get_player_by_name(name):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT score, flags FROM leaderboard WHERE name = %s", (name,))
            row = cur.fetchone()
            if row:
                return {"score": row[0], "solved": row[1].split(",") if row[1] else []}
            return None

import sqlite3

DB_NAME = "leaderboard.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS leaderboard (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                score INTEGER DEFAULT 0,
                flags TEXT
            )
        ''')
        conn.commit()

def save_submission(name, score, flags):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT id FROM leaderboard WHERE name = ?", (name,))
        row = c.fetchone()
        flags_str = ",".join(flags)

        if row:
            c.execute("UPDATE leaderboard SET score = ?, flags = ? WHERE name = ?", (score, flags_str, name))
        else:
            c.execute("INSERT INTO leaderboard (name, score, flags) VALUES (?, ?, ?)", (name, score, flags_str))
        conn.commit()

def get_leaderboard():
    try:
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute("SELECT name, score, flags FROM leaderboard ORDER BY score DESC")
            rows = c.fetchall()
            return [{"name": r[0], "score": r[1], "solved": r[2].split(",") if r[2] else []} for r in rows]
    except Exception as e:
        print(f"[get_leaderboard ERROR] {e}")
        return []


def reset_leaderboard():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM leaderboard")
        conn.commit()


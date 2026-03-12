import sqlite3
from flask import Flask, request

app = Flask(__name__)


def init_db() -> None:
    conn = sqlite3.connect("example.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
    cur.execute("INSERT OR IGNORE INTO users (id, name) VALUES (1, 'alice')")
    conn.commit()
    conn.close()


@app.get("/safe-search")
def safe_search_user():
    name = request.args.get("name", "")

    # False positive candidate: tainted input exists, but query is parameterized.
    query = "SELECT id, name FROM users WHERE name = ?"

    conn = sqlite3.connect("example.db")
    cur = conn.cursor()
    cur.execute(query, (name,))
    rows = cur.fetchall()
    conn.close()

    return {"rows": rows}


if __name__ == "__main__":
    init_db()
    app.run(port=5011)

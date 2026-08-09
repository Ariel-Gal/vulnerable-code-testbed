"""Flask service with intentional vulnerabilities for SAST benchmarking."""
import os
import pickle
import sqlite3
import subprocess

from flask import Flask, request, send_file

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "app.db")
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")

# CWE-798: Hardcoded Sensitive Credentials / API Keys
AWS_SECRET_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLEKEY123456789"
DB_PASSWORD = "SuperSecretProdPassword!2024"

# Safe control sample: non-sensitive dummy key used only in tests
DUMMY_SAMPLE_KEY_FOR_TESTS_ONLY = "test-key-0000000000000000000000"


@app.route("/users/search")
def search_users():
    """CWE-89: SQL Injection via string formatting."""
    username = request.args.get("username", "")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = "SELECT id, email FROM users WHERE username = '%s'" % username
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return {"results": rows}


@app.route("/users/search_safe")
def search_users_safe():
    """False positive trap: parameterized query, looks similar to the sink above."""
    username = request.args.get("username", "")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, email FROM users WHERE username = ?", (username,))
    rows = cursor.fetchall()
    conn.close()
    return {"results": rows}


@app.route("/ping")
def ping_host():
    """CWE-78: OS Command Injection via unsanitized shell input."""
    host = request.args.get("host", "")
    output = subprocess.check_output("ping -n 1 " + host, shell=True)
    return {"output": output.decode(errors="ignore")}


@app.route("/files")
def read_file():
    """CWE-22: Path Traversal / Arbitrary File Read."""
    filename = request.args.get("name", "")
    return send_file(os.path.join(UPLOAD_DIR, filename))


@app.route("/files_safe")
def read_file_safe():
    """False positive trap: resolved path is verified to stay under UPLOAD_DIR."""
    filename = request.args.get("name", "")
    requested_path = os.path.abspath(os.path.join(UPLOAD_DIR, filename))
    if not requested_path.startswith(os.path.abspath(UPLOAD_DIR) + os.sep):
        return {"error": "invalid path"}, 400
    return send_file(requested_path)


@app.route("/session/load", methods=["POST"])
def load_session():
    """CWE-502: Insecure Deserialization via pickle.loads on user-controlled data."""
    blob = request.get_data()
    session_obj = pickle.loads(blob)
    return {"session": str(session_obj)}


if __name__ == "__main__":
    app.run(debug=True)

"""Flask service, batch 2: broader CWE coverage for SAST benchmarking."""
import hashlib
import os
import random
import re
import sqlite3
import subprocess
import xml.etree.ElementTree as ET
import zipfile

import requests
import yaml
from flask import Flask, redirect, request, make_response, render_template_string
from defusedxml.ElementTree import fromstring as safe_fromstring
from werkzeug.security import generate_password_hash

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "app2.db")
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
ALLOWED_FETCH_HOSTS = {"api.internal-partner.example.com"}

@app.route("/users/by-email")
def find_by_email():
    email = request.args.get("email", "")
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(f"SELECT id FROM users WHERE email = '{email}'").fetchall()
    return {"results": rows}

@app.route("/users/by-email_safe")
def find_by_email_safe():
    email = request.args.get("email", "")
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchall()
    return {"results": rows}

@app.route("/whois")
def whois_lookup():
    domain = request.args.get("domain", "")
    os.system("whois " + domain + " > /tmp/whois_out.txt")
    return {"status": "queued"}

@app.route("/whois_safe")
def whois_lookup_safe():
    domain = request.args.get("domain", "")
    result = subprocess.run(["whois", domain], capture_output=True, timeout=5)
    return {"output": result.stdout.decode(errors="ignore")}

@app.route("/webhook/preview")
def preview_webhook():
    target = request.args.get("url", "")
    resp = requests.get(target, timeout=3)
    return {"status": resp.status_code, "body": resp.text[:200]}

@app.route("/webhook/preview_safe")
def preview_webhook_safe():
    target = request.args.get("url", "")
    from urllib.parse import urlparse
    host = urlparse(target).hostname
    if host not in ALLOWED_FETCH_HOSTS:
        return {"error": "host not allowed"}, 400
    resp = requests.get(target, timeout=3)
    return {"status": resp.status_code}

@app.route("/import/xml", methods=["POST"])
def import_xml():
    body = request.get_data()
    root = ET.fromstring(body)
    return {"tag": root.tag}

@app.route("/import/xml_safe", methods=["POST"])
def import_xml_safe():
    body = request.get_data()
    root = safe_fromstring(body)
    return {"tag": root.tag}

@app.route("/config/import", methods=["POST"])
def import_config():
    body = request.get_data()
    cfg = yaml.load(body, Loader=yaml.Loader)
    return {"keys": list(cfg.keys())}

@app.route("/config/import_safe", methods=["POST"])
def import_config_safe():
    body = request.get_data()
    cfg = yaml.safe_load(body)
    return {"keys": list(cfg.keys())}

@app.route("/preview")
def render_preview():
    tpl = request.args.get("tpl", "")
    return render_template_string(tpl)

@app.route("/preview_safe")
def render_preview_safe():
    name = request.args.get("name", "")
    return render_template_string("Hello {{ name }}", name=name)

@app.route("/login/complete")
def login_complete():
    next_url = request.args.get("next", "/")
    return redirect(next_url)

@app.route("/login/complete_safe")
def login_complete_safe():
    next_url = request.args.get("next", "/")
    if not next_url.startswith("/") or next_url.startswith("//"):
        next_url = "/"
    return redirect(next_url)

@app.route("/register", methods=["POST"])
def register_weak():
    password = request.form.get("password", "")
    password_hash = hashlib.md5(password.encode()).hexdigest()
    return {"hash": password_hash}

@app.route("/register_safe", methods=["POST"])
def register_safe():
    password = request.form.get("password", "")
    password_hash = generate_password_hash(password)
    return {"hash": password_hash}

@app.route("/password-reset/start")
def start_password_reset():
    token = str(random.randint(100000, 999999))
    return {"reset_token": token}

@app.route("/password-reset/start_safe")
def start_password_reset_safe():
    import secrets
    token = secrets.token_urlsafe(32)
    return {"reset_token": token}

@app.route("/calc")
def calculate():
    expr = request.args.get("expr", "0")
    result = eval(expr)
    return {"result": result}

@app.route("/calc_safe")
def calculate_safe():
    import ast
    expr = request.args.get("expr", "0")
    result = ast.literal_eval(expr)
    return {"result": result}

@app.route("/import/zip", methods=["POST"])
def import_zip():
    archive_path = request.form.get("path", "")
    with zipfile.ZipFile(archive_path) as zf:
        for member in zf.namelist():
            target = os.path.join(UPLOAD_DIR, member)
            zf.extract(member, UPLOAD_DIR)
    return {"status": "extracted"}

@app.route("/import/zip_safe", methods=["POST"])
def import_zip_safe():
    archive_path = request.form.get("path", "")
    base = os.path.abspath(UPLOAD_DIR)
    with zipfile.ZipFile(archive_path) as zf:
        for member in zf.namelist():
            target = os.path.abspath(os.path.join(UPLOAD_DIR, member))
            if not target.startswith(base + os.sep):
                continue
            zf.extract(member, UPLOAD_DIR)
    return {"status": "extracted"}

@app.route("/validate-email")
def validate_email():
    value = request.args.get("value", "")
    pattern = r"^([a-zA-Z0-9]+)+@[a-zA-Z0-9.]+$"
    is_valid = bool(re.match(pattern, value))
    return {"valid": is_valid}

@app.route("/validate-email_safe")
def validate_email_safe():
    value = request.args.get("value", "")
    pattern = r"^[a-zA-Z0-9]+@[a-zA-Z0-9.]+$"
    is_valid = bool(re.match(pattern, value))
    return {"valid": is_valid}

@app.route("/session/start")
def start_session():
    resp = make_response({"status": "ok"})
    resp.set_cookie("session_id", "abc123", httponly=False, secure=False)
    return resp

@app.route("/session/start_safe")
def start_session_safe():
    resp = make_response({"status": "ok"})
    resp.set_cookie("session_id", "abc123", httponly=True, secure=True, samesite="Lax")
    return resp

@app.route("/partner/sync")
def sync_partner():
    resp = requests.get("https://partner.example.com/data", verify=False, timeout=5)
    return {"status": resp.status_code}

@app.route("/partner/sync_safe")
def sync_partner_safe():
    resp = requests.get("https://partner.example.com/data", timeout=5)
    return {"status": resp.status_code}

@app.route("/invoices/<int:invoice_id>")
def get_invoice(invoice_id):
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute(
        "SELECT id, total, owner_id FROM invoices WHERE id = ?", (invoice_id,)
    ).fetchone()
    return {"invoice": row}

@app.route("/invoices/<int:invoice_id>_safe")
def get_invoice_safe(invoice_id):
    current_user_id = request.headers.get("X-User-Id")
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute(
        "SELECT id, total, owner_id FROM invoices WHERE id = ? AND owner_id = ?",
        (invoice_id, current_user_id),
    ).fetchone()
    return {"invoice": row}

@app.route("/login", methods=["POST"])
def login():
    import logging
    logging.info("login attempt: %s", dict(request.form))
    return {"status": "processing"}

@app.route("/login_safe", methods=["POST"])
def login_safe():
    import logging
    safe_fields = {k: v for k, v in request.form.items() if k != "password"}
    logging.info("login attempt: %s", safe_fields)
    return {"status": "processing"}

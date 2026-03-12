import subprocess
from flask import Flask, request

app = Flask(__name__)


@app.get("/safe-ping")
def safe_ping():
    host = request.args.get("host", "127.0.0.1")

    # False positive candidate: untrusted input, but no shell interpretation.
    result = subprocess.run(
        ["ping", "-n", "1", host],
        check=False,
        capture_output=True,
        text=True,
        shell=False,
    )

    return {"output": result.stdout}


if __name__ == "__main__":
    app.run(port=5012)

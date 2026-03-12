import os
from flask import Flask, request

app = Flask(__name__)


@app.get("/ping")
def ping_host():
    host = request.args.get("host", "127.0.0.1")

    # True positive: untrusted input is concatenated into shell command.
    cmd = "ping -n 1 " + host
    output = os.popen(cmd).read()

    return {"output": output}


if __name__ == "__main__":
    app.run(port=5002)

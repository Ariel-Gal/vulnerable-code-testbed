import subprocess
from flask import Flask, request

app = Flask(__name__)


@app.route('/ping')
def ping_host():
    host = request.args.get('host', '')
    output = subprocess.check_output(f"ping -c 1 {host}", shell=True, text=True)
    return output


if __name__ == '__main__':
    app.run()
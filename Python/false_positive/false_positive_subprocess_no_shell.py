import subprocess
from flask import Flask, request

app = Flask(__name__)


@app.route('/dns_lookup')
def dns_lookup():
    host = request.args.get('host', '')
    result = subprocess.run(['nslookup', host], capture_output=True, text=True, shell=False, check=False)
    return result.stdout or result.stderr


if __name__ == '__main__':
    app.run()
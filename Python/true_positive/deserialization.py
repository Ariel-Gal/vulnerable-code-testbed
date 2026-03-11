import pickle
import base64
from flask import Flask, request

app = Flask(__name__)

@app.route('/load')
def load_data():
    data = request.args.get('data')
    if data:
        decoded_data = base64.b64decode(data)
        obj = pickle.loads(decoded_data)
        return str(obj)
    return "No data"

if __name__ == '__main__':
    app.run()
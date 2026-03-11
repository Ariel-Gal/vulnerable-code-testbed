from flask import Flask, request

app = Flask(__name__)


@app.route('/read')
def read_file():
    filename = request.args.get('filename', '')
    path = f"uploads/{filename}"
    with open(path, 'r', encoding='utf-8') as file_handle:
        return file_handle.read()


if __name__ == '__main__':
    app.run()
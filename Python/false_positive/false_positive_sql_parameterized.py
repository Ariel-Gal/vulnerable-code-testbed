import sqlite3
from flask import Flask, request

app = Flask(__name__)


@app.route('/user_safe')
def get_user_safe():
    username = request.args.get('username', '')
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    return str(user) if user else 'Not found'


if __name__ == '__main__':
    app.run()
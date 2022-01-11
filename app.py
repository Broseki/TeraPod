from flask import Flask, send_from_directory, render_template, request

import config
import helpers.csrf_guard
from helpers.csrf_guard import validate_csrf

app = Flask(__name__)
app.config['SECRET_KEY'] = config.APP_SECRET
app.jinja_env.globals.update(csrf_token=helpers.csrf_guard.csrf_token)


@app.route('/dist/<path:path>', methods=['GET'])
def get_static_assets(path):
    return send_from_directory('static/dist', path)


@app.route('/login', methods=['GET'])
def get_login():  # put application's code here
    return render_template("login.html")


@app.route('/login', methods=['POST'])
@validate_csrf
def post_login():
    username = request.form['username']
    password = request.form['password']
    print("{} - {}".format(username, password))
    return "TEST"


if __name__ == '__main__':
    app.run()

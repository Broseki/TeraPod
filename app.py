from flask import Flask, send_from_directory, render_template, request, redirect, flash, Blueprint
from flask_login import login_user, login_required, LoginManager, login_manager

import config
import helpers.csrf_guard
from helpers.csrf_guard import validate_csrf
import helpers.authentication
from helpers.db import Database

app = Flask(__name__)
app.config['SECRET_KEY'] = config.APP_SECRET
app.jinja_env.globals.update(csrf_token=helpers.csrf_guard.csrf_token)
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "get_login"


@login_manager.user_loader
def load_user(user_uuid):
    with Database() as db:
        return helpers.authentication.User(user_uuid)


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
    remember = request.form.get('remember_me')
    if remember:
        remember = True
    else:
        remember = False
    if helpers.authentication.verify_user_login(username, password):
        with Database() as db:
            user_data = db.get_user_by_username(username)
            login_user(helpers.authentication.User(user_data['user_uuid']), remember)
            return redirect("/dashboard")
    flash("Incorrect username and/or password", "danger")
    return redirect("/login")


@app.route('/dashboard', methods=['GET'])
@login_required
def get_dashboard():
    return "HELLO"


if __name__ == '__main__':
    app.run()

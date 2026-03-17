from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import UserMixin, login_user, logout_user, login_required

from app.extensions import login_manager

auth_bp = Blueprint("auth", __name__)

class OwnerUser(UserMixin):
    def __init__(self, user_id: str):
        self.id = user_id

@login_manager.user_loader
def load_user(user_id):
    if user_id == "owner":
        return OwnerUser("owner")
    return None

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        expected_username = current_app.config["OWNER_USERNAME"]
        expected_password = current_app.config["OWNER_PASSWORD"]

        if username == expected_username and password == expected_password:
            user = OwnerUser("owner")
            login_user(user)
            return redirect(url_for("main.dashboard"))

        flash("Invalid username or password", "error")

    return render_template("login.html")

@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

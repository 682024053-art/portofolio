from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from config import Config

login_bp = Blueprint("login", __name__, url_prefix="/admin")


@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("admin_logged_in"):
        return redirect(url_for("dashboard.dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        if email == Config.ADMIN_EMAIL and password == Config.ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            session["admin_email"] = email
            flash("Login berhasil.", "success")
            return redirect(url_for("dashboard.dashboard"))

        flash("Email atau password salah.", "error")
        return redirect(url_for("login.login"))

    return render_template("admin/login.html")


@login_bp.route("/logout")
def logout():
    session.clear()
    flash("Berhasil logout.", "success")
    return redirect(url_for("login.login"))

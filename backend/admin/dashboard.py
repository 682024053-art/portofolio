from flask import Blueprint, render_template, session, redirect, url_for
from model import get_connection

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/admin")


def admin_is_logged_in():
    return session.get("admin_logged_in")


@dashboard_bp.route("/dashboard")
def dashboard():
    if not admin_is_logged_in():
        return redirect(url_for("login.login"))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) AS total FROM profiles")
    total_profiles = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM skills")
    total_skills = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM experiences")
    total_experiences = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM projects")
    total_projects = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM contacts")
    total_contacts = cursor.fetchone()["total"]

    cursor.close()
    conn.close()

    return render_template(
        "admin/dashboard.html",
        total_profiles=total_profiles,
        total_skills=total_skills,
        total_experiences=total_experiences,
        total_projects=total_projects,
        total_contacts=total_contacts
    )

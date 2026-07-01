from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from model import get_connection

experiences_bp = Blueprint("experiences", __name__, url_prefix="/admin/experiences")


def admin_required():
    return session.get("admin_logged_in")


@experiences_bp.route("/")
def index():
    if not admin_required():
        return redirect(url_for("login.login"))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM experiences ORDER BY id DESC")
    experiences = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("admin/experiences.html", experiences=experiences)


@experiences_bp.route("/create", methods=["POST"])
def create():
    if not admin_required():
        return redirect(url_for("login.login"))

    position = request.form.get("position")
    company = request.form.get("company")
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")
    description = request.form.get("description")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO experiences (position, company, start_date, end_date, description)
        VALUES (%s, %s, %s, %s, %s)
    """, (position, company, start_date, end_date, description))
    cursor.close()
    conn.close()

    flash("Experience berhasil ditambahkan.", "success")
    return redirect(url_for("experiences.index"))


@experiences_bp.route("/update/<int:id>", methods=["POST"])
def update(id):
    if not admin_required():
        return redirect(url_for("login.login"))

    position = request.form.get("position")
    company = request.form.get("company")
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")
    description = request.form.get("description")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE experiences
        SET position=%s, company=%s, start_date=%s, end_date=%s, description=%s
        WHERE id=%s
    """, (position, company, start_date, end_date, description, id))
    cursor.close()
    conn.close()

    flash("Experience berhasil diperbarui.", "success")
    return redirect(url_for("experiences.index"))


@experiences_bp.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    if not admin_required():
        return redirect(url_for("login.login"))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM experiences WHERE id=%s", (id,))
    cursor.close()
    conn.close()

    flash("Experience berhasil dihapus.", "success")
    return redirect(url_for("experiences.index"))

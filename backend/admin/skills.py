from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from model import get_connection

skills_bp = Blueprint("skills", __name__, url_prefix="/admin/skills")


def admin_required():
    return session.get("admin_logged_in")


@skills_bp.route("/")
def index():
    if not admin_required():
        return redirect(url_for("login.login"))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM skills ORDER BY id DESC")
    skills = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("admin/skills.html", skills=skills)


@skills_bp.route("/create", methods=["POST"])
def create():
    if not admin_required():
        return redirect(url_for("login.login"))

    name = request.form.get("name")
    level = request.form.get("level") or 0
    icon = request.form.get("icon")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO skills (name, level, icon)
        VALUES (%s, %s, %s)
    """, (name, level, icon))
    cursor.close()
    conn.close()

    flash("Skill berhasil ditambahkan.", "success")
    return redirect(url_for("skills.index"))


@skills_bp.route("/update/<int:id>", methods=["POST"])
def update(id):
    if not admin_required():
        return redirect(url_for("login.login"))

    name = request.form.get("name")
    level = request.form.get("level") or 0
    icon = request.form.get("icon")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE skills
        SET name=%s, level=%s, icon=%s
        WHERE id=%s
    """, (name, level, icon, id))
    cursor.close()
    conn.close()

    flash("Skill berhasil diperbarui.", "success")
    return redirect(url_for("skills.index"))


@skills_bp.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    if not admin_required():
        return redirect(url_for("login.login"))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM skills WHERE id=%s", (id,))
    cursor.close()
    conn.close()

    flash("Skill berhasil dihapus.", "success")
    return redirect(url_for("skills.index"))

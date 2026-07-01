from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from model import get_connection
from backend.admin.upload import upload_to_cloudinary, delete_from_cloudinary

projects_bp = Blueprint("projects", __name__, url_prefix="/admin/projects")


def admin_required():
    return session.get("admin_logged_in")


@projects_bp.route("/")
def index():
    if not admin_required():
        return redirect(url_for("login.login"))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects ORDER BY id DESC")
    projects = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("admin/projects.html", projects=projects)


@projects_bp.route("/create", methods=["POST"])
def create():
    if not admin_required():
        return redirect(url_for("login.login"))

    title = request.form.get("title")
    description = request.form.get("description")
    tech_stack = request.form.get("tech_stack")
    github_url = request.form.get("github_url")
    demo_url = request.form.get("demo_url")
    image = request.files.get("image")

    upload_result = upload_to_cloudinary(image, "portfolio/projects") if image and image.filename else None
    image_url = upload_result["url"] if upload_result else None
    image_public_id = upload_result["public_id"] if upload_result else None

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO projects
        (title, description, tech_stack, image_url, image_public_id, github_url, demo_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (title, description, tech_stack, image_url, image_public_id, github_url, demo_url))
    cursor.close()
    conn.close()

    flash("Project berhasil ditambahkan.", "success")
    return redirect(url_for("projects.index"))


@projects_bp.route("/update/<int:id>", methods=["POST"])
def update(id):
    if not admin_required():
        return redirect(url_for("login.login"))

    title = request.form.get("title")
    description = request.form.get("description")
    tech_stack = request.form.get("tech_stack")
    github_url = request.form.get("github_url")
    demo_url = request.form.get("demo_url")
    image = request.files.get("image")

    conn = get_connection()
    cursor = conn.cursor()

    if image and image.filename != "":
        cursor.execute("SELECT image_public_id FROM projects WHERE id=%s", (id,))
        old_data = cursor.fetchone()
        if old_data:
            delete_from_cloudinary(old_data.get("image_public_id"))

        upload_result = upload_to_cloudinary(image, "portfolio/projects")
        cursor.execute("""
            UPDATE projects
            SET title=%s, description=%s, tech_stack=%s,
                image_url=%s, image_public_id=%s,
                github_url=%s, demo_url=%s
            WHERE id=%s
        """, (
            title, description, tech_stack,
            upload_result["url"], upload_result["public_id"],
            github_url, demo_url, id
        ))
    else:
        cursor.execute("""
            UPDATE projects
            SET title=%s, description=%s, tech_stack=%s,
                github_url=%s, demo_url=%s
            WHERE id=%s
        """, (title, description, tech_stack, github_url, demo_url, id))

    cursor.close()
    conn.close()

    flash("Project berhasil diperbarui.", "success")
    return redirect(url_for("projects.index"))


@projects_bp.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    if not admin_required():
        return redirect(url_for("login.login"))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT image_public_id FROM projects WHERE id=%s", (id,))
    old_data = cursor.fetchone()
    if old_data:
        delete_from_cloudinary(old_data.get("image_public_id"))

    cursor.execute("DELETE FROM projects WHERE id=%s", (id,))
    cursor.close()
    conn.close()

    flash("Project berhasil dihapus.", "success")
    return redirect(url_for("projects.index"))

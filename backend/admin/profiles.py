from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from model import get_connection
from backend.admin.upload import upload_to_cloudinary, delete_from_cloudinary

profiles_bp = Blueprint("profiles", __name__, url_prefix="/admin/profiles")


def admin_required():
    return session.get("admin_logged_in")


@profiles_bp.route("/")
def index():
    if not admin_required():
        return redirect(url_for("login.login"))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profiles ORDER BY id DESC")
    profiles = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("admin/profiles.html", profiles=profiles)


@profiles_bp.route("/create", methods=["POST"])
def create():
    if not admin_required():
        return redirect(url_for("login.login"))

    name = request.form.get("name")
    title = request.form.get("title")
    description = request.form.get("description")
    email = request.form.get("email")
    phone = request.form.get("phone")
    address = request.form.get("address")
    photo = request.files.get("photo")

    upload_result = upload_to_cloudinary(photo, "portfolio/profiles") if photo and photo.filename else None
    photo_url = upload_result["url"] if upload_result else None
    photo_public_id = upload_result["public_id"] if upload_result else None

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO profiles
        (name, title, description, email, phone, address, photo_url, photo_public_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (name, title, description, email, phone, address, photo_url, photo_public_id))
    cursor.close()
    conn.close()

    flash("Profile berhasil ditambahkan.", "success")
    return redirect(url_for("profiles.index"))


@profiles_bp.route("/update/<int:id>", methods=["POST"])
def update(id):
    if not admin_required():
        return redirect(url_for("login.login"))

    name = request.form.get("name")
    title = request.form.get("title")
    description = request.form.get("description")
    email = request.form.get("email")
    phone = request.form.get("phone")
    address = request.form.get("address")
    photo = request.files.get("photo")

    conn = get_connection()
    cursor = conn.cursor()

    if photo and photo.filename != "":
        cursor.execute("SELECT photo_public_id FROM profiles WHERE id=%s", (id,))
        old_data = cursor.fetchone()
        if old_data:
            delete_from_cloudinary(old_data.get("photo_public_id"))

        upload_result = upload_to_cloudinary(photo, "portfolio/profiles")
        cursor.execute("""
            UPDATE profiles
            SET name=%s, title=%s, description=%s, email=%s, phone=%s, address=%s,
                photo_url=%s, photo_public_id=%s
            WHERE id=%s
        """, (
            name, title, description, email, phone, address,
            upload_result["url"], upload_result["public_id"], id
        ))
    else:
        cursor.execute("""
            UPDATE profiles
            SET name=%s, title=%s, description=%s, email=%s, phone=%s, address=%s
            WHERE id=%s
        """, (name, title, description, email, phone, address, id))

    cursor.close()
    conn.close()

    flash("Profile berhasil diperbarui.", "success")
    return redirect(url_for("profiles.index"))


@profiles_bp.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    if not admin_required():
        return redirect(url_for("login.login"))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT photo_public_id FROM profiles WHERE id=%s", (id,))
    old_data = cursor.fetchone()
    if old_data:
        delete_from_cloudinary(old_data.get("photo_public_id"))

    cursor.execute("DELETE FROM profiles WHERE id=%s", (id,))
    cursor.close()
    conn.close()

    flash("Profile berhasil dihapus.", "success")
    return redirect(url_for("profiles.index"))

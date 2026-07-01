from flask import Blueprint, render_template, redirect, url_for, session, flash
from model import get_connection

contacts_bp = Blueprint("contacts", __name__, url_prefix="/admin/contacts")


def admin_required():
    return session.get("admin_logged_in")


@contacts_bp.route("/")
def index():
    if not admin_required():
        return redirect(url_for("login.login"))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts ORDER BY id DESC")
    contacts = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("admin/contacts.html", contacts=contacts)


@contacts_bp.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    if not admin_required():
        return redirect(url_for("login.login"))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE id=%s", (id,))
    cursor.close()
    conn.close()

    flash("Pesan berhasil dihapus.", "success")
    return redirect(url_for("contacts.index"))

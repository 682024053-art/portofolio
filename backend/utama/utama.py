from flask import Blueprint, render_template, request, redirect, url_for, flash
from model import get_connection
from config import Config
import resend

utama_bp = Blueprint("utama", __name__)


@utama_bp.route("/portfolio")
def index():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM profiles ORDER BY id DESC LIMIT 1")
    profile = cursor.fetchone()

    cursor.execute("SELECT * FROM skills ORDER BY id DESC")
    skills = cursor.fetchall()

    cursor.execute("SELECT * FROM experiences ORDER BY id DESC")
    experiences = cursor.fetchall()

    cursor.execute("SELECT * FROM projects ORDER BY id DESC")
    projects = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "utama/index.html",
        profile=profile,
        skills=skills,
        experiences=experiences,
        projects=projects
    )


@utama_bp.route("/api/contact", methods=["POST"])
def contact():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    subject = request.form.get("subject", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not email or not message:
        flash("Nama, email, dan pesan wajib diisi.", "error")
        return redirect(url_for("utama.index") + "#contact")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO contacts (name, email, subject, message)
        VALUES (%s, %s, %s, %s)
    """, (name, email, subject, message))
    cursor.close()
    conn.close()

    try:
        if Config.RESEND_API_KEY and Config.MAIL_FROM:
            resend.api_key = Config.RESEND_API_KEY
            resend.Emails.send({
                "from": Config.MAIL_FROM,
                "to": [Config.ADMIN_EMAIL],
                "subject": f"Pesan Portfolio: {subject or 'Tanpa Subject'}",
                "html": f"""
                    <h2>Pesan Baru dari Website Portfolio</h2>
                    <p><b>Nama:</b> {name}</p>
                    <p><b>Email:</b> {email}</p>
                    <p><b>Subject:</b> {subject}</p>
                    <p><b>Pesan:</b></p>
                    <p>{message}</p>
                """
            })

        flash("Pesan berhasil dikirim.", "success")

    except Exception as e:
        print("Resend error:", e)
        flash("Pesan tersimpan, tetapi email gagal dikirim. Cek API key Resend.", "error")

    return redirect(url_for("utama.index") + "#contact")

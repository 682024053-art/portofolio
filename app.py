from flask import Flask, redirect, url_for
from config import Config

from backend.utama.utama import utama_bp
from backend.admin.login import login_bp
from backend.admin.dashboard import dashboard_bp
from backend.admin.profiles import profiles_bp
from backend.admin.skills import skills_bp
from backend.admin.experiences import experiences_bp
from backend.admin.projects import projects_bp
from backend.admin.contacts import contacts_bp

app = Flask(
    __name__,
    template_folder="frontend",
    static_folder="frontend"
)

app.secret_key = Config.SECRET_KEY

app.register_blueprint(utama_bp)
app.register_blueprint(login_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(profiles_bp)
app.register_blueprint(skills_bp)
app.register_blueprint(experiences_bp)
app.register_blueprint(projects_bp)
app.register_blueprint(contacts_bp)


@app.route("/")
def home():
    return redirect(url_for("utama.index"))


if __name__ == "__main__":
    app.run(debug=True)

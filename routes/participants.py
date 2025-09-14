import os
from flask import Blueprint, render_template, request, redirect, url_for, current_app,flash
from werkzeug.utils import secure_filename
from extensions import db
from models import Participant

participants_bp = Blueprint("participants", __name__)

UPLOAD_FOLDER = "static/uploads/logos"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@participants_bp.route("/")
def list_participants():
    participants = Participant.query.all()
    return render_template("participants.html", participants=participants)

@participants_bp.route("/add", methods=["POST"])
def add():
    team_name = request.form["team_name"]
    team_category = request.form["team_category"]
    logo_file = request.files.get("team_logo")

    logo_filename = None
    if logo_file and allowed_file(logo_file.filename):
        filename = secure_filename(logo_file.filename)
        logo_path = os.path.join(current_app.root_path, UPLOAD_FOLDER)
        os.makedirs(logo_path, exist_ok=True)
        logo_file.save(os.path.join(logo_path, filename))
        logo_filename = filename

    new_participant = Participant(
        team_name=team_name,
        team_category=team_category,
        team_logo=logo_filename
    )
    db.session.add(new_participant)
    db.session.commit()

    return redirect(url_for("participants.list_participants"))
# --- update route ---
@participants_bp.route("/update/<int:id>", methods=["POST"])
def update(id):
    from app import db
    from models import Participant  # adjust import if needed

    participant = Participant.query.get_or_404(id)

    # update fields
    participant.team_name = request.form["team_name"]
    participant.team_category = request.form["team_category"]

    # handle logo upload
    if "team_logo" in request.files:
        file = request.files["team_logo"]
        if file and file.filename.strip() != "":
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            participant.team_logo = filename  # overwrite old logo

    db.session.commit()
    flash("Participant updated successfully!", "success")
    return redirect(url_for("participants.list_participants"))

@participants_bp.route("/delete/<int:id>")
def delete(id):
    participant = Participant.query.get_or_404(id)
    if participant.team_logo:  # ✅ also remove the logo file if it exists
        logo_path = os.path.join(current_app.root_path, UPLOAD_FOLDER, participant.team_logo)
        if os.path.exists(logo_path):
            os.remove(logo_path)
    db.session.delete(participant)
    db.session.commit()
    return redirect(url_for("participants.list_participants"))

from flask import Blueprint, render_template, request, redirect, url_for
from extensions import db
from models import User

users_bp = Blueprint("users", __name__)

@users_bp.route("/")
def list_users():
    users = User.query.all()
    return render_template("users.html", users=users)

@users_bp.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    role = request.form["role"]

    new_user = User(name=name, role=role)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("users.list_users"))

@users_bp.route("/delete/<int:id>")
def delete(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("users.list_users"))

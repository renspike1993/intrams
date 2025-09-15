from flask import Blueprint, render_template, request, redirect, url_for, flash,session
from extensions import db
from models import User
from werkzeug.security import generate_password_hash,check_password_hash

users_bp = Blueprint("users", __name__)

# ---------------------
# List users
# ---------------------
@users_bp.route("/")
def list_users():
    users = User.query.all()
    return render_template("users.html", users=users)

# ---------------------
# Add user (from admin panel)
# ---------------------
@users_bp.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    role = request.form["role"]
    password = request.form.get("password") or "default123"  # optional default
    status = request.form.get("status") or "active"

    # Check if user already exists
    if User.query.filter_by(name=name).first():
        flash("Username already exists. Choose another.", "danger")
        return redirect(url_for("users.list_users"))

    new_user = User(name=name, role=role, status=status)
    new_user.password = password  # ✅ hashed automatically via property
    db.session.add(new_user)
    db.session.commit()

    flash("User added successfully!", "success")
    return redirect(url_for("users.list_users"))

# ---------------------
# Delete user
# ---------------------
@users_bp.route("/delete/<int:id>")
def delete(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash("User deleted successfully!", "info")
    return redirect(url_for("users.list_users"))


@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(name=username).first()
        if user:
            if user.status != "active":
                flash("Your account is inactive. Contact admin.", "warning")
                return redirect(url_for("users.login"))

            if check_password_hash(user.password_hash, password):
                # Set session
                session["user_id"] = user.id
                session["username"] = user.name
                session["role"] = user.role
                flash("Login successful!", "success")
                return redirect(url_for("index"))
            else:
                flash("Incorrect password.", "danger")
        else:
            flash("User not found.", "danger")

    return render_template("login.html")
# ---------------------
# Registration route (public)
# ---------------------
@users_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")  # e.g., "admin" or "game_manager"
        status = request.form.get("status") or "active"

        # Check if username already exists
        if User.query.filter_by(name=username).first():
            flash("Username already exists. Choose another.", "danger")
            return redirect(url_for("users.register"))

        # Create user with hashed password
        new_user = User(name=username, role=role, status=status)
        new_user.password = password  # ✅ hashed automatically
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! You can now login.", "success")
        return redirect(url_for("users.login"))

    return render_template("register.html")

@users_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("users.login"))

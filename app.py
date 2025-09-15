from flask import Flask, render_template, flash, redirect, url_for, session, request
from extensions import db
from models import Participant, Game, Match, User

# Import blueprints
from routes.participants import participants_bp
from routes.games import games_bp
from routes.matches import matches_bp
from routes.users import users_bp

def protect_blueprint(bp, exclude=[]):
    """Protect all routes in a blueprint except endpoints in exclude list."""
    @bp.before_request
    def require_login():
        # Allow certain endpoints like login/register
        if request.endpoint in exclude:
            return
        if "user_id" not in session:
            flash("Please log in first.", "warning")
            return redirect(url_for("users.login"))

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///intrams.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = "your_super_secret_key_here"  # 🔑 Replace with a strong random string
    db.init_app(app)

    # ======================
    # LOGIN/LOGOUT ROUTES
    # ======================
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            user = User.query.filter_by(name=username).first()
            if user and user.check_password(password):
                session["user_id"] = user.id
                session["username"] = user.name
                session["role"] = user.role
                flash("Login successful!", "success")
                return redirect(url_for("index"))
            else:
                flash("Invalid username or password.", "danger")
        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        flash("You have been logged out.", "info")
        return redirect(url_for("login"))

    # ======================
    # PROTECTED INDEX
    # ======================
    @app.route("/")
    def index():
        if "user_id" not in session:
            return redirect(url_for("users.login"))
        games = Game.query.all()
        return render_template("index.html", games=games)

    # ======================
    # REGISTER BLUEPRINTS
    # ======================
    # Protect all blueprint routes except login/register
    protect_blueprint(participants_bp)
    protect_blueprint(games_bp)
    protect_blueprint(matches_bp)
    protect_blueprint(users_bp, exclude=["users.login", "users.register"])

    app.register_blueprint(participants_bp, url_prefix="/participants")
    app.register_blueprint(games_bp, url_prefix="/games")
    app.register_blueprint(matches_bp, url_prefix="/matches")
    app.register_blueprint(users_bp, url_prefix="/users")

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5002, debug=True)

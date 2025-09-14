from flask import Flask, render_template
from extensions import db
from models import Participant, Game, Match, User

# Import blueprints
from routes.participants import participants_bp
from routes.games import games_bp
from routes.matches import matches_bp
from routes.users import users_bp


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///intrams.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # Add this line:
    app.secret_key = "your_super_secret_key_here"  # 🔑 Replace with a strong random string
    # ✅ Initialize db with app
    db.init_app(app)

    # ✅ Register blueprints
    app.register_blueprint(participants_bp, url_prefix="/participants")
    app.register_blueprint(games_bp, url_prefix="/games")
    app.register_blueprint(matches_bp, url_prefix="/matches")
    app.register_blueprint(users_bp, url_prefix="/users")

    @app.route("/")
    def index():
        return render_template("index.html")

    return app


if __name__ == "__main__":
    app = create_app()

    # ✅ Create database tables if not exist
    with app.app_context():
        db.create_all()


    app.run(host="0.0.0.0", port=5000, debug=True)


from flask import Blueprint, render_template, request, redirect, url_for
from extensions import db
from models import Game, User

games_bp = Blueprint("games", __name__)

@games_bp.route("/")
def list_games():
    games = Game.query.all()
    managers = User.query.filter_by(role="game_manager").all()  # ✅ only managers
    return render_template("games.html", games=games, managers=managers)

@games_bp.route("/add", methods=["POST"])
def add():
    category = request.form["category"]
    game_name = request.form["game_name"]
    game_manager = request.form["game_manager"]
    live_url = request.form.get("live_url")  # ✅ NEW
    new_game = Game(category=category, game_name=game_name,
                    game_manager=game_manager, live_url=live_url)
    db.session.add(new_game)
    db.session.commit()
    return redirect(url_for("games.list_games"))

@games_bp.route("/update/<int:id>", methods=["POST"])
def update(id):
    game = Game.query.get_or_404(id)
    game.category = request.form["category"]
    game.game_name = request.form["game_name"]
    game.game_manager = request.form["game_manager"]
    game.live_url = request.form.get("live_url")
    db.session.commit()
    return redirect(url_for("games.list_games"))


@games_bp.route("/edit/<int:id>", methods=["POST"])
def edit(id):
    game = Game.query.get_or_404(id)
    game.category = request.form["category"]
    game.game_name = request.form["game_name"]
    game.game_manager = request.form["game_manager"]
    game.live_url = request.form.get("live_url")  # ✅ NEW
    db.session.commit()
    return redirect(url_for("games.list_games"))


@games_bp.route("/delete/<int:id>")
def delete(id):
    game = Game.query.get_or_404(id)
    db.session.delete(game)
    db.session.commit()
    return redirect(url_for("games.list_games"))

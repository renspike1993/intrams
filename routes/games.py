from flask import Blueprint, render_template, request, redirect, url_for,flash
from extensions import db
from models import Game, User, Participant, Result

games_bp = Blueprint("games", __name__)

# List all games
@games_bp.route("/")
def list_games():
    games = Game.query.all()
    managers = User.query.filter_by(role="game_manager").all()
    participants = Participant.query.all()
    # preload results for each game
    results = {r.game_id: r for r in Result.query.all()}
    return render_template(
        "games.html",
        games=games,
        managers=managers,
        participants=participants,
        results=results
    )

# Add new game
@games_bp.route("/add", methods=["POST"])
def add():
    category = request.form["category"]
    game_name = request.form["game_name"]
    game_manager = request.form["game_manager"]
    live_url = request.form.get("live_url")
    new_game = Game(category=category, game_name=game_name,
                    game_manager=game_manager, live_url=live_url)
    db.session.add(new_game)
    db.session.commit()
    return redirect(url_for("games.list_games"))

# Update existing game (combine update/edit)
@games_bp.route("/update/<int:id>", methods=["POST"])
def update(id):
    game = Game.query.get_or_404(id)
    game.category = request.form["category"]
    game.game_name = request.form["game_name"]
    game.game_manager = request.form["game_manager"]
    game.live_url = request.form.get("live_url")
    db.session.commit()
    return redirect(url_for("games.list_games"))


@games_bp.route("/delete/<int:id>")
def delete(id):
    game = Game.query.get_or_404(id)

    # delete related results first
    Result.query.filter_by(game_id=game.id).delete()

    db.session.delete(game)
    db.session.commit()
    flash("Game deleted successfully!", "success")
    return redirect(url_for("games.list_games"))

# Update or add game results
@games_bp.route("/update_result/<int:game_id>", methods=["POST"])
def update_result(game_id):
    first = request.form.get("first")
    second = request.form.get("second")
    third = request.form.get("third")

    # check if result exists for this game
    result = Result.query.filter_by(game_id=game_id).first()
    if result:
        result.first = first
        result.second = second
        result.third = third
    else:
        result = Result(game_id=game_id, first=first, second=second, third=third)
        db.session.add(result)

    db.session.commit()
    return redirect(url_for("games.list_games"))


@games_bp.route("/rankings")
def rankings():
    # fetch all participants
    participants = Participant.query.all()
    # fetch all results
    results = Result.query.all()
    # fetch all games
    games = Game.query.all()

    # initialize dictionary to store points
    scores = {p.id: 0 for p in participants}

    # assign points based on results
    for r in results:
        if r.first:
            scores[r.first] += 10
        if r.second:
            scores[r.second] += 5
        if r.third:
            scores[r.third] += 2

    # prepare a list of participants with their scores
    rankings = []
    for p in participants:
        rankings.append({
            "team_name": p.team_name,
            "team_logo": p.team_logo,
            "wins": scores[p.id]
        })

    # sort by wins descending
    rankings = sorted(rankings, key=lambda x: x["wins"], reverse=True)

    # map results by game_id for easy lookup in template
    results_by_game = {r.game_id: r for r in results}

    return render_template(
        "ranking.html",
        rankings=rankings,
        games=games,
        results=results_by_game
    )

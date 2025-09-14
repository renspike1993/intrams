from flask import Blueprint, render_template, request, redirect, url_for
from extensions import db
from models import Match, Game, Participant

matches_bp = Blueprint("matches", __name__)

@matches_bp.route("/")
def list_matches():
    matches = Match.query.all()
    games = Game.query.all()
    participants = Participant.query.all()
    return render_template("matches.html", matches=matches, games=games, participants=participants)

@matches_bp.route("/add", methods=["POST"])
def add():
    game_id = request.form["game_id"]
    player_1 = request.form["player_1"]
    player_2 = request.form["player_2"]
    winner = request.form.get("winner")  # optional
    detail = {}  # you can extend later with JSON details

    new_match = Match(game_id=game_id, player_1=player_1, player_2=player_2, winner=winner, detail=detail)
    db.session.add(new_match)
    db.session.commit()

    return redirect(url_for("matches.list_matches"))

@matches_bp.route("/update_winner/<int:id>", methods=["POST"])
def update_winner(id):
    match = Match.query.get_or_404(id)
    winner_id = request.form.get("winner")
    if winner_id:
        match.winner = int(winner_id)
        # ✅ Only updating the winner, leave game_id/player_1/player_2 untouched
        db.session.commit()
    return redirect(url_for("matches.list_matches"))


@matches_bp.route("/delete/<int:id>")
def delete(id):
    match = Match.query.get_or_404(id)
    db.session.delete(match)
    db.session.commit()
    return redirect(url_for("matches.list_matches"))

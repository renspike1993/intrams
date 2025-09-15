from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash



class Participant(db.Model):
    __tablename__ = "participants"

    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(100), nullable=False)
    team_category = db.Column(db.String(50), nullable=False)
    team_logo = db.Column(db.String(255), nullable=True)  # nullable true ✅

class Game(db.Model):
    __tablename__ = "games"

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    game_name = db.Column(db.String(100), nullable=False)
    game_manager = db.Column(db.String(100), nullable=False)
    live_url = db.Column(db.String(255), nullable=True)


class Match(db.Model):
    __tablename__ = "matches"

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey("games.id"), nullable=False)
    player_1 = db.Column(db.Integer, db.ForeignKey("participants.id"), nullable=False)
    player_2 = db.Column(db.Integer, db.ForeignKey("participants.id"), nullable=False)
    winner = db.Column(db.Integer, db.ForeignKey("participants.id"))
    detail = db.Column(db.JSON)

    # relationships
    game = db.relationship("Game", backref="matches")
    player1 = db.relationship("Participant", foreign_keys=[player_1])
    player2 = db.relationship("Participant", foreign_keys=[player_2])
    winner_rel = db.relationship("Participant", foreign_keys=[winner])


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # "game_manager" or "admin"
    password_hash = db.Column(db.String(255), nullable=False)  # store hashed password
    status = db.Column(db.String(20), nullable=False, default="active")  # active/inactive

    # Write-only password property
    @property
    def password(self):
        raise AttributeError("Password is write-only!")

    @password.setter
    def password(self, plain_password):
        self.password_hash = generate_password_hash(plain_password)

    # Verify password
    def check_password(self, plain_password):
        return check_password_hash(self.password_hash, plain_password)
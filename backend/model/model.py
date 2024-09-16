from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# Define models for Team and Match
class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    registration_date = db.Column(db.Date, nullable=False)
    group_number = db.Column(db.Integer, nullable=False, unique=True)

class Points(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), unique=True, nullable=False)
    points = db.Column(db.Integer, nullable=False)

class Match_Results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_team = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    second_team = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    first_team_score = db.Column(db.Integer, nullable=False)
    second_team_score = db.Column(db.Integer, nullable=False)

from model.model import db, Team, Match_Results, Points
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import logging
def update_match(first_team_name, second_team_name, first_team_score, second_team_score):
    try:
        team1 = Team.query.filter_by(name=first_team_name).one()
        team2 = Team.query.filter_by(name=second_team_name).one()
        team1_id = team1.id
        team2_id = team2.id
        updated_match1 = Match_Results.query.filter_by(first_team=team1_id, second_team=team2.id).one()
        updated_match2 = Match_Results.query.filter_by(first_team=team2_id, second_team=team1.id).one()

        team1_points = Points.query.filter_by(team_id=team1_id).one()
        team2_points = Points.query.filter_by(team_id=team2_id).one()
        # delete initial points
        if updated_match1.first_team_score > updated_match1.second_team_score:
            team1_points.points -= 3
        elif updated_match1.first_team_score < updated_match1.second_team_score:
            team2_points.points -= 3
        else:
            team1_points.points -= 1
            team2_points.points -= 1
        updated_match1.first_team_score = first_team_score
        updated_match1.second_team_score = second_team_score
        updated_match2.first_team_score = second_team_score
        updated_match2.second_team_score = first_team_score
        # add new points
        if first_team_score > second_team_score:
            team1_points.points += 3
        elif first_team_score < second_team_score:
            team2_points.points += 3
        else:
            team1_points.points += 1
            team2_points.points += 1
        db.session.commit()
        logging.info("Updated match")
        return {"isSuccess": True, "status": 200, "message": "Match successfully updated"}
    except IntegrityError as e:
        db.session.rollback()
        logging.error(f"Integrity error occurred ${str(e)}")
        return {"isSuccess": False, "status": 400, "message": "Integrity error occurred: " + str(e)}
    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"Database error occurred ${str(e)}")
        return {"isSuccess": False, "status": 400, "message": "Database error occurred: " + str(e)}
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error occurred ${str(e)}")
        return {"isSuccess": False, "status": 500, "message": "Error occurred: " + str(e)}
    finally:
        db.session.close()



def add_match(first_team_name, second_team_name, first_team_score, second_team_score):
    try:
        team1 = Team.query.filter_by(name=first_team_name).one()
        team2 = Team.query.filter_by(name=second_team_name).one()
        team1_id = team1.id
        team2_id = team2.id
        match1 = Match_Results(
            first_team=team1_id,
            second_team=team2_id,
            first_team_score=first_team_score,
            second_team_score=second_team_score)
        match2 = Match_Results(
            first_team=team2_id,
            second_team=team1_id,
            first_team_score=second_team_score,
            second_team_score=first_team_score)
        db.session.add(match1)
        db.session.add(match2)
        team1_points = Points.query.filter_by(team_id=team1_id).one()
        team2_points = Points.query.filter_by(team_id=team2_id).one()
        if first_team_score > second_team_score:
            team1_points.points += 3
        elif first_team_score < second_team_score:
            team2_points.points += 3
        else: # tie
            team1_points.points += 1
            team2_points.points += 1
        db.session.commit()
        return {"isSuccess": True, "status": 200, "message": "Match successfully added"}
    except IntegrityError as e:
        db.session.rollback()
        return {"isSuccess": False, "status": 400, "message": "Integrity error occurred: " + str(e)}
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"isSuccess": False, "status": 400, "message": "Database error occurred: " + str(e)}
    except Exception as e:
        db.session.rollback()
        return {"isSuccess": False, "status": 500, "message": "Error occurred: " + str(e)}
    finally:
        db.session.close()


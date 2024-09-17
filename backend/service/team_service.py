from model.model import db, Team, Points, Match_Results
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import logging


def update_team(old_name, new_name): # should only be able the change their name
    try:
        updated_team = Team.query.filter_by(name=old_name).one()
        updated_team.name = new_name
        db.session.commit()
        logging.info("Successfully updated team")
        return {"isSuccess": True, "status": 200, "message": "Team successfully updated"}
    except IntegrityError as e:
        db.session.rollback()
        logging.error(f"Error updating team: {str(e)}")
        return {"isSuccess": False, "status": 400, "message": "Integrity error occurred: " + str(e)}
    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"Error updating team: {str(e)}")
        return {"isSuccess": False, "status": 400, "message": "Database error occurred: " + str(e)}
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error updating team: {str(e)}")
        return {"isSuccess": False, "status": 500, "message": "Error occurred: " + str(e)}
    finally:
        db.session.close()


def get_team(name):
    try:
        team = Team.query.filter_by(name=name).one()
        # get matches, played, win count, loss count, rank
        win_count = Match_Results.query.\
            filter_by(first_team=team.id).\
            filter(Match_Results.first_team_score > Match_Results.second_team_score)\
            .count()
        loss_count = Match_Results.query. \
            filter_by(first_team=team.id). \
            filter(Match_Results.first_team_score < Match_Results.second_team_score) \
            .count()
        tie_count = Match_Results.query. \
            filter_by(first_team=team.id). \
            filter(Match_Results.first_team_score == Match_Results.second_team_score) \
            .count()
        db.session.commit()
        team_response = {
            "name": team.name,
            "registration_date": team.registration_date,
            "group_number": team.group_number,
            "win_count": win_count,
            "loss_count": loss_count,
            "tie_count": tie_count
        }
        logging.info("Successfully retrieved team")
        return {"isSuccess": True, "status": 200, "message": "Team successfully fetched", "data": team_response}
    except IntegrityError as e:
        db.session.rollback()
        logging.error(f"Error retrieving team: {str(e)}")
        return {"isSuccess": False, "status": 400, "message": "Integrity error occurred: " + str(e)}
    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"Error retrieving team: {str(e)}")
        return {"isSuccess": False, "status": 400, "message": "Database error occurred: " + str(e)}
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error retrieving team: {str(e)}")
        return {"isSuccess": False, "status": 500, "message": "Error occurred: " + str(e)}
    finally:
        db.session.close()

def add_teams(data):
    try:
        all_teams = []
        all_points = []
        for team in data:
            new_team = Team(
                name=team["name"],
                registration_date=db.func.to_date(team["registration_date"] + "/2024", "DD/MM/YYYY"),
                group_number=team["group_number"])
            all_teams.append(new_team)
        db.session.add_all(all_teams)
        db.session.flush()
        for team in all_teams:
            new_point = Points(team_id=team.id, points=0)
            all_points.append(new_point)
        # when there is a new team, its points table should be initialised to zero
        db.session.add_all(all_points)
        db.session.commit()
        logging.info("Successfully added teams")
        return {"isSuccess": True, "status": 201, "message": "Team successfully added"}
    except IntegrityError as e:
        db.session.rollback()
        logging.error(f"Error adding teams: {str(e)}")
        return {"isSuccess": False, "status": 400, "message": "Integrity error occurred: " + str(e)}
    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"Error adding teams: {str(e)}")
        return {"isSuccess": False, "status": 400, "message": "Database error occurred: " + str(e)}
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error adding teams: {str(e)}")
        return {"isSuccess": False, "status": 500, "message": "Error occurred: " + str(e)}
    finally:
        db.session.close()


from model.model import db, Team, Points, Match_Results
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

def update_team(group_number, new_name): # should only be able the change their name
    try:
        updated_team = Team.query.filter_by(group_number=group_number).one()
        updated_team.name = new_name
        db.session.commit()
        return {"isSuccess": True, "status": 200, "message": "Team successfully updated"}
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


def get_team(group_number):
    try:
        team = Team.query.filter_by(group_number=group_number).one()
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
        return {"isSuccess": True, "status": 200, "message": "Team successfully fetched", "data": team_response}
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

def add_team(team_name, registration_date, group_number):
    try:
        new_team = Team(
            name=team_name,
            registration_date=db.func.to_date(registration_date, "DD/MM/YYYY"),
            group_number=group_number)
        db.session.add(new_team)
        db.session.flush()
        # when there is a new team, its points table should be initialised to zero
        team_points = Points(team_id=new_team.id, points=0)
        db.session.add(team_points)
        db.session.commit()
        return {"isSuccess": True, "status": 201, "message": "Team successfully added"}
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


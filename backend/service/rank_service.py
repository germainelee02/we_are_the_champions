from model.model import db, Team, Match_Results, Points
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import desc, asc

def get_ranking():
    try:
        teams = Points.query\
            .join(Team, Team.id == Points.team_id)\
            .order_by(desc(Points.points), asc(Team.registration_date))\
            .all()
        data = []
        for team in teams:
            data_obj = {
                "team_id": team.team_id,
                "points": team.points,
            }
            data.append(data_obj)
        db.session.commit()
        return {"isSuccess": True, "status": 200, "message": "Ranks successfully retrieved", "data": data}
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

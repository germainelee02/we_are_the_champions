from model.model import db, Team, Match_Results, Points
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import desc, asc
import logging

def clear_all():
    try:
        db.drop_all() # drop all tables
        db.create_all()
        db.session.commit()
        logging.info("All data cleared")
        return {"isSuccess": True, "status": 200, "message": "All data successfully cleared"}
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


def get_ranking(group_number):
    try:
        teams = db.session\
            .query(Team.name, Team.registration_date, Points.points)\
            .join(Points, Team.id == Points.team_id)\
            .where(Team.group_number == group_number)\
            .order_by(desc(Points.points), asc(Team.registration_date))\
            .all()
        data = []
        for team in teams:
            data_obj = {
                "team_name": team.name,
                "registration_date": team.registration_date,
                "points": team.points,
            }
            data.append(data_obj)
        db.session.commit()
        logging.info("Rankings retrieved")
        return {"isSuccess": True, "status": 200, "message": "Ranks successfully retrieved", "data": data}
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

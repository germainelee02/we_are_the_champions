from model.model import db
from model.model import Team
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask import jsonify

def update_team(group_number, new_name): # should only be able the change their name
    try:
        updated_team = Team.query.filter_by(group_number=group_number).one()
        updated_team.name = new_name
        db.session.commit()
        team_response = {
            "name": updated_team.name,
            "registration_date": updated_team.registration_date,
            "group_number": updated_team.group_number
        }
        return jsonify(status=200, message="Team successfully updated", data=team_response)

    except IntegrityError as e:
        db.session.rollback()
        return jsonify(status=400, message="Integrity error occurred: " + str(e))
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify(status=400, message="Database error occurred: " + str(e))
    except Exception as e:
        db.session.rollback()
        return jsonify(status=500, message="Error occurred: " + str(e))
    finally:
        db.session.close()



def get_team(group_number):
    try:
        team = Team.query.filter_by(group_number=group_number).one()
        db.session.commit()
        team_response = {
            "name": team.name,
            "registration_date": team.registration_date,
            "group_number": team.group_number
        }
        return jsonify(status=200, message="Team successfully fetched", data=team_response)
    except IntegrityError as e:
        db.session.rollback()
        return jsonify(status=400, message="Integrity error occurred: " + str(e))
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify(status=400, message="Database error occurred: " + str(e))
    except Exception as e:
        db.session.rollback()
        return jsonify(status=500, message="Error occurred: " + str(e))
    finally:
        db.session.close()

def add_team(team_name, registration_date, group_number):
    try:
        newTeam = Team(
            name=team_name,
            registration_date=db.func.to_date(registration_date, "DD/MM/YYYY"),
            group_number=group_number)
        db.session.add(newTeam)
        db.session.commit()
        return jsonify(status=201, message="Team successfully created")
    except IntegrityError as e:
        db.session.rollback()
        return jsonify(status=400, message="Integrity error occurred: " + str(e))
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify(status=400, message="Database error occurred: " + str(e))
    except Exception as e:
        db.session.rollback()
        return jsonify(status=500, message="Error occurred: " + str(e))
    finally:
        db.session.close()


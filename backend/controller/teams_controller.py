from flask_restful import Resource
from flask import request, jsonify, make_response
from service.team_service import add_teams, get_team, update_team
import logging

class TeamsAPI(Resource):
    def post(self):
        data = request.json["data"]
        logging.info(f'Adding teams: {data}')
        result = add_teams(data)
        return make_response(jsonify(message=result["message"]), result["status"])

    def get(self):
        name = request.args.get("name")
        logging.info(f'Retrieving team {name}')
        result = get_team(name)
        if result["isSuccess"]:
            return make_response(jsonify(message=result["message"], data=result["data"]), result["status"])
        else:
            return make_response(jsonify(message=result["message"]), result["status"])


    def patch(self):
        old_name = request.args.get("name")
        data = request.json
        new_name = data["name"]
        logging.info(f'Updating team name from {old_name} to {new_name}')
        result = update_team(old_name, new_name)
        return make_response(jsonify(message=result["message"]), result["status"])

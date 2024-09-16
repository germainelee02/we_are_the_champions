from flask_restful import Resource
from flask import request, jsonify, make_response
from service.team_service import add_teams, get_team, update_team
import logging

class TeamsAPI(Resource):
    def post(self):
        logging.info("Handling POST request at TeamsAPI")
        data = request.json["data"]
        result = add_teams(data)
        return make_response(jsonify(message=result["message"]), result["status"])

    def get(self):
        logging.info("Handling GET request at TeamsAPI")
        name = request.args.get("name")
        result = get_team(name)
        if result["isSuccess"]:
            return make_response(jsonify(message=result["message"], data=result["data"]), result["status"])
        else:
            return make_response(jsonify(message=result["message"]), result["status"])


    def patch(self):
        logging.info("Handling PATCH request at TeamsAPI")
        # group_number = request.args.get("group_number")
        old_name = request.args.get("name")
        data = request.json
        new_name = data["name"]
        result = update_team(old_name, new_name)
        return make_response(jsonify(message=result["message"]), result["status"])

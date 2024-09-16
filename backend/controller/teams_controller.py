from flask_restful import Resource
from flask import request, jsonify
from service.team_service import add_team, get_team, update_team
import logging

class TeamsAPI(Resource):
    def post(self):
        logging.info("Handling POST request at TeamsAPI")
        data = request.json
        name = data["name"]
        group_number = data["group_number"]
        registration_date = data["registration_date"] + "/2024" # assumption that this is happening in 2024
        result = add_team(name, registration_date, group_number)

        return jsonify(status=result["status"], message=result["message"])

    def get(self):
        logging.info("Handling GET request at TeamsAPI")
        group_number = request.args.get("group_number")
        result = get_team(group_number)
        if result["isSuccess"]:
            return jsonify(status=result["status"], message=result["message"], data=result["data"])
        else:
            return jsonify(status=result["status"], message=result["message"])


    def patch(self):
        logging.info("Handling PATCH request at TeamsAPI")
        group_number = request.args.get("group_number")
        data = request.json
        new_name = data["name"]
        result = update_team(group_number, new_name)
        return jsonify(status=result["status"], message=result["message"])

from flask_restful import Resource
from flask import request, jsonify
from service.team_service import add_team, get_team, update_team

class TeamsAPI(Resource):
    def post(self):
        data = request.json
        name = data["name"]
        group_number = data["group_number"]
        registration_date = data["registration_date"] + "/2024" # assumption that this is happening in 2024
        result = add_team(name, registration_date, group_number)

        return jsonify(status=result["status"], message=result["message"])

    def get(self):
        group_number = request.args.get("group_number")
        result = get_team(group_number)
        return jsonify(status=result["status"], message=result["message"], data=result["data"])

    def patch(self):
        group_number = request.args.get("group_number")
        data = request.json
        new_name = data["name"]
        result = update_team(group_number, new_name)
        return jsonify(status=result["status"], message=result["message"])

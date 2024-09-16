from flask_restful import Resource
from flask import request, jsonify
from service.match_service import add_match, update_match

class MatchAPI(Resource):
    def post(self):
        data = request.json
        first_team_name = data["first_team_name"]
        second_team_name = data["second_team_name"]
        first_team_score = data["first_team_score"]
        second_team_score = data["second_team_score"]
        result = add_match(first_team_name, second_team_name, first_team_score, second_team_score)
        return jsonify(status=result["status"], message=result["message"])

    def patch(self):
        data = request.json
        first_team_name = data["first_team_name"]
        second_team_name = data["second_team_name"]
        first_team_score = data["first_team_score"]
        second_team_score = data["second_team_score"]
        result = update_match(first_team_name, second_team_name, first_team_score, second_team_score)
        return jsonify(status=result["status"], message=result["message"])


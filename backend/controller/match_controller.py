from flask_restful import Resource
from flask import request, jsonify, make_response
from service.match_service import add_matches, update_match
import logging

class MatchAPI(Resource):
    def post(self):
        data = request.json["data"]
        result = add_matches(data)
        logging.info(f'Adding matches: {data}')
        return make_response(jsonify(message=result["message"]), result["status"])

    def patch(self):
        logging.info("Handling PATCH request at MatchAPI")
        data = request.json
        first_team_name = data["first_team_name"]
        second_team_name = data["second_team_name"]
        first_team_score = data["first_team_score"]
        second_team_score = data["second_team_score"]
        logging.info(f'Updating a match: {data}')
        result = update_match(first_team_name, second_team_name, first_team_score, second_team_score)
        return make_response(jsonify(message=result["message"]), result["status"])


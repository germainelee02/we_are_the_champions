from flask_restful import Resource
from flask import request, jsonify, make_response
from service.table_service import get_ranking, clear_all
import logging


class TableAPI(Resource):
    def delete(self):
        logging.info("Clearing all data")
        result = clear_all()
        return make_response(jsonify(message=result["message"]), result["status"])

    def get(self):
        group_number = request.args.get("group_number")
        logging.info(f"Getting rankings for group {group_number}")
        result = get_ranking(group_number)
        if result["isSuccess"]:
            return make_response(jsonify(message=result["message"], data=result["data"]), result["status"])
        else:
            return make_response(jsonify(message=result["message"]), result["status"])




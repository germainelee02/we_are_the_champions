from flask_restful import Resource
from flask import request, jsonify
from service.table_service import get_ranking, clear_all
import logging


class TableAPI(Resource):
    def delete(self):
        logging.info("Handling DELETE request at RankAPI")
        result = clear_all()
        return jsonify(status=result["status"], message=result["message"])

    def get(self):
        logging.info("Handling GET request at RankAPI")
        result = get_ranking()
        if result["isSuccess"]:
            return jsonify(status=result["status"], message=result["message"], data=result["data"])
        else:
            return jsonify(status=result["status"], message=result["message"])




from flask_restful import Resource
from flask import request, jsonify
from service.rank_service import get_ranking
import logging


class RankAPI(Resource):
    def get(self):
        logging.info("Handling GET request at RankAPI")
        result = get_ranking()
        if result["isSuccess"]:
            return jsonify(status=result["status"], message=result["message"], data=result["data"])
        else:
            return jsonify(status=result["status"], message=result["message"])




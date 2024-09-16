from flask_restful import Resource
from flask import request, jsonify
from service.rank_service import get_ranking
class RankAPI(Resource):
    def get(self):
        result = get_ranking()
        if result["isSuccess"]:
            return jsonify(status=result["status"], message=result["message"], data=result["data"])
        else:
            return jsonify(status=result["status"], message=result["message"])




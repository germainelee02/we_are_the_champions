from flask_restful import Resource
from flask import request, jsonify

class TeamsAPI(Resource):
    def post(self):
        data = request.json
        return jsonify(data)

    def get(self):
        return jsonify(request.args)

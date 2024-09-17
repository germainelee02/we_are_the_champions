from flask import Flask
from flask_restful import Api
from controller.teams_controller import TeamsAPI
from controller.match_controller import MatchAPI
from controller.table_controller import TableAPI
from model.model import db
from flask_cors import CORS
import logging
import os

app = Flask(__name__)

# initialise database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
api = Api(app)
db.init_app(app)

CORS(app, resources={r"/*": {"origins": "http://localhost:4000"}})


with app.app_context():
    logging.info("Creating all tables...")
    db.create_all()
    logging.info("Tables created")

api.add_resource(TeamsAPI, '/team')
api.add_resource(MatchAPI, '/match')
api.add_resource(TableAPI, '/all')

@app.after_request
def add_security_headers(response):
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response

if __name__ == "__main__":
    logging.info("Starting application...")
    app.run(host='0.0.0.0', port=3000)

from flask import Flask
from flask_restful import Api
from controller.teams_controller import TeamsAPI
from controller.match_controller import MatchAPI
from controller.rank_controller import RankAPI
from model.model import db
from flask_cors import CORS
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://germaine:govtechtkh@localhost:5432/championship_db' # hide this
api = Api(app)
db.init_app(app)

CORS(app, resources={r"/*": {"origins": "*"}}) # obviously change this


with app.app_context():
    # db.drop_all() # check if this is good practice
    logging.info("Creating all tables...")
    db.create_all()
    logging.info("Tables created")

api.add_resource(TeamsAPI, '/team')
api.add_resource(MatchAPI, '/match')
api.add_resource(RankAPI, '/rank')

if __name__ == "__main__":
    logging.info("Starting application...")
    app.run(port=5000)

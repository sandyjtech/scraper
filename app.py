# app.py
from flask import Flask
from flask_restful import Api
from flask_cors import CORS


from scraper import Scraper


app = Flask(__name__)
CORS(app)
api = Api(app)



api.add_resource(Scraper, "/scaper")
if __name__ == "__main__":
    app.run(debug=True)
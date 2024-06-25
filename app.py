# app.py
from flask import Flask, render_template
from flask_restful import Api
from flask_cors import CORS
from listen import AnalyzeCall
from scraper import Scraper


app = Flask(__name__)
CORS(app)
api = Api(app)

@app.route("/")
def index():
    return render_template("index.html")
    

api.add_resource(AnalyzeCall, '/analyze-call')
api.add_resource(Scraper, "/scaper")

if __name__ == "__main__":
    app.run(debug=True)
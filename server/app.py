# app.py
from flask import Flask, render_template
from flask_restful import Api
from flask_cors import CORS
from listen import AnalyzeCall
from scraper import Scraper
from scraper.server.wordpress import WordpressPage
from scraper.server.get_audio import PlaybackAudioResource, ProcessExcelFile

app = Flask(__name__)
CORS(app)
api = Api(app)

@app.route("/")
@app.route("/<int:id>")
def index(id=0):
    return render_template("index.html")
@app.errorhandler(404)
def not_found(e):
    return render_template("index.html")
    

api.add_resource(AnalyzeCall, '/analyze-call')
api.add_resource(Scraper, "/scaper")
api.add_resource(WordpressPage, '/wordpress-page')

#Get Connex Audio Files
api.add_resource(PlaybackAudioResource, "/audio-file/<string:id>")
api.add_resource(ProcessExcelFile, "/get-connex-audio-files")

if __name__ == "__main__":
    app.run(debug=True)
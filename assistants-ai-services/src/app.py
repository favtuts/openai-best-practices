"""Flask Application"""

# load libraries
from flask import Flask, jsonify
import sys

# load modules
from src.endpoints.blueprint_systeminfo import blueprint_systeminfo
from src.endpoints.blueprint_assistant import blueprint_assistant

# init Flask app
app = Flask(__name__)

# register blueprints, ensure all paths are versioned!
app.register_blueprint(blueprint_systeminfo, url_prefix="/api/v1/systeminfo")
app.register_blueprint(blueprint_assistant, url_prefix="/api/v1/assistant")

# start Flask app
if __name__=="__main__":
    app.run(host='0.0.0.0', debug=True)
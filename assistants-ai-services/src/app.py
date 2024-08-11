"""Flask Application"""

# load libraries
from flask import Flask, jsonify
import sys

# load modules
from src.endpoints.blueprint_systeminfo import blueprint_systeminfo
from src.endpoints.blueprint_assistant import blueprint_assistant
from src.endpoints.blueprint_testing import blueprint_testing
from src.endpoints.swagger import swagger_ui_blueprint, SWAGGER_URL

# init Flask app
app = Flask(__name__)

# register blueprints, ensure all paths are versioned!
app.register_blueprint(blueprint_systeminfo, url_prefix="/api/v1/systeminfo")
app.register_blueprint(blueprint_assistant, url_prefix="/api/v1/assistant")
app.register_blueprint(blueprint_testing, url_prefix="/api/v1/testing")

# register all swagger documented functions here
from src.swagger.api_spec import spec

with app.test_request_context():
    for fn_name in app.view_functions:
        if fn_name == 'static':
            continue
        print(f"Loading swagger docs for function: {fn_name}")
        view_fn = app.view_functions[fn_name]
        spec.path(view=view_fn)

@app.route("/api/swagger.json")
def create_swagger_spec():
    """
    Swagger API definition.
    """
    return jsonify(spec.to_dict())

app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


# start Flask app
if __name__=="__main__":
    app.run(host='0.0.0.0', debug=True)
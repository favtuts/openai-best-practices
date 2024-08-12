"""Flask Application"""

# load libraries
from flask import Flask, jsonify, g, session, request
import sys
import json
import time
from time import strftime
from datetime import datetime

import uuid
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import default_exceptions
import traceback
import src.utils.log_manager as log_manager

# load modules
from src.endpoints.blueprint_systeminfo import blueprint_systeminfo
from src.endpoints.blueprint_assistant import blueprint_assistant
from src.endpoints.blueprint_testing import blueprint_testing
from src.endpoints.swagger import swagger_ui_blueprint, SWAGGER_URL

# init Flask app
app = Flask(__name__)
app.secret_key = "c00de22a8b1e4daa2cabc8b3f82fdb753574293f8b673f9a"

app.logger.info("Staring up Flask application...")
# init App configuratin


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
        app.logger.debug(f"Loading swagger docs for function: {fn_name}")
        view_fn = app.view_functions[fn_name]
        spec.path(view=view_fn)

@app.route("/api/swagger.json")
def create_swagger_spec():
    """
    Swagger API definition.
    """
    return jsonify(spec.to_dict())

app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


# register all Exceptions handlers
@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    
    tb = traceback.format_exc()
    ts = strftime('[%Y-%b-%d %H:%M]')
    if request is not None:
        req_ctx = {}
        if session.get("ctx") is not None:
            req_ctx = session["ctx"]
            
        app.logger.error('%s %s %s %s %s %s SERVER ERROR\n%s',
                  ts,
                  request.remote_addr,
                  request.method,
                  request.scheme,
                  request.full_path,
                  req_ctx,
                  tb)
    else:
        app.logger.error('%s SERVER ERROR\n%s\n%s', ts, req_ctx, tb)
        
    return jsonify(error=str(e)), code

for ex in default_exceptions:
    app.register_error_handler(ex, handle_error)


# register logging for requests
@app.before_request
def start_timer():    
    # start timer
    # ts = strftime('%Y-%m-%d %H:%M:%S.%f')
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    
    g.start = time.time()
    # generate requestID and attach it as session ctx 
    request_id = str(uuid.uuid4())
    session["ctx"] = {"request_id": request_id}
    
    app.logger.debug('Start request: %s %s %s %s %s\nRequest context: %s\nRequest body: %s', 
                    ts, request.remote_addr,  request.method,  request.scheme,  request.full_path, 
                    json.dumps(session["ctx"]), 
                    request.get_data())
    # app.logger.debug('Headers: %s', request.headers)
    # app.logger.debug('Request Body: %s', request.get_data())

@app.after_request
def log_request(response):
    "Log HTTP request details"
    
    # Ignore logging for static files
    if (
        request.path == "/favicon.ico"
        or request.path.startswith("/static")
        or request.path.startswith("/admin/static")
    ):
        return response
    
    
    # This IF avoids the duplication of registry in the log,
    # since that 500 is already logged via @app.errorhandler.
    if response.status_code == 500:
        return response  
    
    # ts = strftime('%Y-%m-%d %H:%M:%S.%f')    
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    now = time.time()
    duration = round(now - g.start, 6)  # to the microsecond
    ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
    host = request.host.split(":", 1)[0]
    params = dict(request.args)
    x_request_id = request.headers.get("X-Request-ID", "")
    req_ctx = {}
    if session.get("ctx") is not None:
        req_ctx = session["ctx"]
    
    log_params = {
        "timestamp": ts,
        "method": request.method,
        "path": request.path,
        "status": response.status_code,
        "duration": duration,
        "ip": ip_address,
        "host": host,
        "params": params,
        "request_id": x_request_id,
        "request_ctx": req_ctx
    }
    
    app.logger.debug("Complete request: \n%s\nResponse body:\n%s",  json.dumps(log_params), response.get_data())    
    
    return response


# start Flask app
if __name__=="__main__":
    app.run(host='0.0.0.0', debug=True)
import os
import logging
import subprocess
import bugsnag
from flask_cors import CORS
from bugsnag.flask import handle_exceptions
from flask import Flask, jsonify
from .support.exceptions import BECoreException
from .config import DevelopmentConfig, ProductionConfig

# Creating Flask application
app = Flask(__name__)

# Initializing config
mode = os.environ.get('FLASK_ENV', None)

if mode == 'development':
    app.config.from_object(DevelopmentConfig)
else:
    app.config.from_object(ProductionConfig)

    bugsnag.configure(
        api_key=app.config['BUGSNAG_API'],
        project_root=app.config['BUGSNAG_ROOT'],
    )
    handle_exceptions(app)

#Allow CORS
CORS(app, supports_credentials=True)

# Initialize Controllers
from .controllers.closest_locations import closest_locations

app.register_blueprint(closest_locations, url_prefix='/api/closest_locations')

# Register Error Handler
base_class_exception = Exception
if mode == 'development':
    base_class_exception = BECoreException

@app.errorhandler(base_class_exception)
def handle_swig_core_exception(error):
    status_code = 500
    payload = {'error': 'The application hit an unknown error. Please contact support.'}

    if isinstance(error, BECoreException):
        payload = error.to_dict()
        status_code = error.status_code
    elif type(error).__name__ == 'NotFound':
        status_code = 404
    else:
        bugsnag.notify(error)

    response = jsonify(payload)
    return response, status_code

# Unauthenticated heartbeat to see if this is alive
@app.route('/', methods=['GET'])
def heartbeat():
    return "Hello there."

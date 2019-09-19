from os.path import join
from flask import Blueprint, send_from_directory, current_app, Response

static_files = Blueprint('static_files', __name__)

@static_files.route('public/<path:path>')
def get_public_files(path: str):
    """
    Get public files (css/js)

    :param path: path to file
    :return: file
    """
    return send_from_directory(current_app.config['PUBLIC_PATH'], path)


@static_files.route('iframes/<path:path>')
def get_iframe_files(path: str):
    """
    Get supported iframe documents

    :param path: path to file
    :return: file
    """
    if '.env.js' in path:
        with open(join(current_app.config['IFRAME_PATH'], path)) as env_js:
            env_js_content = env_js.read()
            for env_key, value in current_app.config['IFRAME_ENV_JS'].items():
                env_js_content = env_js_content.replace(f'<{env_key}>', value)
            return Response(env_js_content, mimetype='text/javascript')
    else:
        return send_from_directory(current_app.config['IFRAME_PATH'], path)

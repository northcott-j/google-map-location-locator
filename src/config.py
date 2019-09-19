from os import environ, getcwd, path, listdir
from src.models import Location


def load_locations_from_environ():
    location_mapping = {}
    for env_key, value in environ.items():
        if 'COLLECTION_MAP_ID' in env_key:
            map_file_id = environ.get(env_key.replace('MAP_ID', 'FILE_ID'))
            location_mapping[value] = Location.load_locations_from_collection(value, file_id=map_file_id)
    return location_mapping


def iframe_env_js_vars():
    iframe_env_js = {
        'LOCATION_SERVICE_URL': environ['LOCATION_SERVICE_URL'],
        'GOOGLE_PLACES_API': environ['GOOGLE_PLACES_API']
    }
    for env_key, value in environ.items():
        if 'IFRAME_MAP_ID' in env_key:
            iframe_env_js[env_key] = value
    return iframe_env_js


class BaseConfig(object):
    DEBUG = False
    LOCATION_MAPS = load_locations_from_environ()
    SLACK_ALERTS = environ.get('SLACK_ALERTS', None)
    FLASK_ENV = environ.get('FLASK_ENV', None)
    FLASK_DEV_NAME = environ.get('FLASK_DEV_NAME', 'James Bond')
    PUBLIC_PATH = path.join(getcwd(), 'public')
    IFRAME_PATH = path.join(getcwd(), 'iframes')
    IFRAME_ENV_JS = iframe_env_js_vars()


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    HOST = '127.0.0.1'
    PORT = 5001
    HOME_URI = 'http://localhost:5001/'


class ProductionConfig(BaseConfig):
    HOST = '0.0.0.0'
    # Probably set these in your .env
    BUGSNAG_API=environ.get('BUGSNAG_API', None)
    BUGSNAG_ROOT=path.join(getcwd(), 'src')
    PORT = environ.get('PORT', None)
    HOME_URI = environ.get('HOME_URI', None)

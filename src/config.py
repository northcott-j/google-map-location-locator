from src.models import Location
from os import environ, getcwd, path


def load_locations_from_environ():
    location_mapping = {}
    for env_key, value in environ.items():
        if 'MAP_ID' in env_key:
            location_mapping[value] = Location.load_locations_from_collection(value)
    return location_mapping


class BaseConfig(object):
    DEBUG = False
    LOCATION_MAPS = load_locations_from_environ()
    SLACK_ALERTS = environ.get('SLACK_ALERTS', None)
    FLASK_ENV = environ.get('FLASK_ENV', None)
    FLASK_DEV_NAME = environ.get('FLASK_DEV_NAME', 'James Bond')


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
